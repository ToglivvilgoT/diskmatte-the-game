import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.cosmetics.models import Skin

SKINS_STATIC_SUBPATH = "cosmetics/skins"
METADATA_FILE = "metadata.json"


class Command(BaseCommand):
    help = (
        "Load skins from metadata.json file. Creates new Skin entries from metadata "
        "with all available fields. Skins with missing required fields are created "
        "as unavailable (is_available=False) for admin review. Skins missing from "
        "metadata are marked unavailable instead of being deleted."
    )

    def handle(self, *args, **options):
        metadata_path = Path(settings.BASE_DIR) / "static" / SKINS_STATIC_SUBPATH / METADATA_FILE
        if not metadata_path.is_file():
            self.stderr.write(f"Metadata file not found: {metadata_path}")
            return

        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata_list = json.load(f)
        except json.JSONDecodeError as e:
            self.stderr.write(f"Failed to parse {metadata_path}: {e}")
            return

        if not isinstance(metadata_list, list):
            self.stderr.write("Metadata file must contain a JSON list")
            return

        created = []
        updated = []
        skipped = []
        seen_skin_slugs = set()

        for item in metadata_list:
            slug = item.get("slug")
            if not slug:
                self.stderr.write("Skipping item without slug field")
                continue
            seen_skin_slugs.add(slug)

            # Check if all required fields are present
            required_fields = {"name", "slug", "description", "price", "kind"}
            has_all_required = required_fields.issubset(item.keys())

            # Check kind-specific required fields and normalize kind to lowercase
            kind = item.get("kind", "").lower()
            if kind == "color" and "color" not in item:
                has_all_required = False
            elif kind == "image" and "image" not in item:
                has_all_required = False
            elif kind == "css_class" and "css_class" not in item:
                has_all_required = False

            # Build defaults dict, only including optional fields if present in metadata
            defaults = {
                "name": item.get("name", "Unknown"),
                "description": item.get("description", ""),
                "price": item.get("price", 0),
                "kind": kind or Skin.Kind.IMAGE,
                "image": item.get("image", ""),
                "css_class": item.get("css_class", ""),
                "is_available": has_all_required,
            }
            # Only set color if provided; otherwise use model's default
            if "color" in item:
                defaults["color"] = item["color"]

            skin, created_flag = Skin.objects.get_or_create(
                slug=slug,
                defaults=defaults,
            )

            if created_flag:
                created.append(slug)
                status = "available" if has_all_required else "unavailable (missing fields)"
                self.stdout.write(
                    self.style.SUCCESS(f"Created skin '{slug}' ({status})")
                )
            else:
                # Update existing skin if metadata has changed
                updated_fields = {}
                for key in ["name", "description", "price", "kind", "color", "image", "css_class"]:
                    # Only update color if it's explicitly in metadata
                    if key == "color":
                        if "color" in item:
                            updated_fields[key] = item[key]
                    elif key in item:
                        value = item[key]
                        # Normalize kind to lowercase
                        if key == "kind":
                            value = value.lower()
                        updated_fields[key] = value

                if updated_fields:
                    for key, value in updated_fields.items():
                        setattr(skin, key, value)
                    skin.is_available = has_all_required
                    skin.save()
                    updated.append(slug)
                    self.stdout.write(f"Updated skin: {slug}")
                else:
                    skipped.append(slug)
                    self.stdout.write(f"No changes for skin: {slug}")

        missing = Skin.objects.exclude(slug__in=seen_skin_slugs).filter(is_available=True)
        for skin in missing:
            skin.is_available = False
            skin.save(update_fields=["is_available"])
            self.stdout.write(
                self.style.WARNING(
                    f"Skin '{skin.slug}' missing from metadata, marking unavailable"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {len(created)}, updated {len(updated)}, "
                f"skipped {len(skipped)}."
            )
        )
