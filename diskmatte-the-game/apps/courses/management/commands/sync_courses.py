import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.courses.models import Course, LearningSet, Topic

COURSES_DIR = Path("courses")


class Command(BaseCommand):
    help = (
        "Load courses, learning sets, and topics from static/courses/<course_slug>.json "
        "files. Creates or updates entries to match the files, and marks entries "
        "missing from the files as inactive (is_active=False) instead of deleting them."
    )

    def handle(self, *args, **options):
        courses_dir = Path(settings.BASE_DIR) / "static" / COURSES_DIR
        if not courses_dir.is_dir():
            self.stderr.write(f"Courses metadata directory not found: {courses_dir}")
            return

        seen_course_slugs = set()
        seen_learning_set_slugs = set()
        seen_topic_slugs = set()

        for metadata_path in sorted(courses_dir.glob("*.json")):
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    course_item = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(f"Failed to parse {metadata_path}: {e}")
                continue

            if not isinstance(course_item, dict):
                self.stderr.write(f"{metadata_path} must contain a JSON object")
                continue

            course = self._sync_course(metadata_path.stem, course_item)
            if course is None:
                continue
            seen_course_slugs.add(course.slug)

            for order, ls_item in enumerate(course_item.get("learning_sets", []), start=1):
                learning_set = self._sync_learning_set(course, ls_item, order)
                if learning_set is not None:
                    seen_learning_set_slugs.add((course.slug, learning_set.slug))

            for order, topic_item in enumerate(course_item.get("topics", []), start=1):
                topic = self._sync_topic(course, topic_item, order)
                if topic is not None:
                    seen_topic_slugs.add((course.slug, topic.slug))

        self._deactivate_missing(
            Course.objects.exclude(slug__in=seen_course_slugs),
            lambda c: f"Course '{c.slug}' missing from metadata, marking inactive",
        )
        self._deactivate_missing(
            [
                ls
                for ls in LearningSet.objects.select_related("course")
                if (ls.course.slug, ls.slug) not in seen_learning_set_slugs
            ],
            lambda ls: f"Learning set '{ls.course.slug}/{ls.slug}' missing from metadata, marking inactive",
        )
        self._deactivate_missing(
            [
                t
                for t in Topic.objects.select_related("course")
                if (t.course.slug, t.slug) not in seen_topic_slugs
            ],
            lambda t: f"Topic '{t.course.slug}/{t.slug}' missing from metadata, marking inactive",
        )

    def _deactivate_missing(self, queryset, message_fn):
        for obj in queryset:
            if obj.is_active:
                obj.is_active = False
                obj.save()
            self.stdout.write(self.style.WARNING(message_fn(obj)))

    def _sync_course(self, slug, item):
        name = item.get("name")
        if not name:
            self.stderr.write(f"Skipping course '{slug}', missing name: {item}")
            return None

        defaults = {
            "name": name,
            "description": item.get("description", ""),
            "is_active": True,
        }

        course, created = Course.objects.update_or_create(slug=slug, defaults=defaults)
        self.stdout.write(f"{'Created' if created else 'Updated'} course: {slug}")
        return course

    def _sync_learning_set(self, course, item, order):
        name = item.get("name")
        slug = item.get("slug")
        if not name or not slug:
            self.stderr.write(
                f"Skipping learning set on course '{course.slug}', missing name/slug: {item}"
            )
            return None

        defaults = {
            "name": name,
            "kind": item.get("kind", "course_book"),
            "description": item.get("description", ""),
            "order": order,
            "is_active": True,
        }

        learning_set, created = LearningSet.objects.update_or_create(
            course=course, slug=slug, defaults=defaults
        )
        self.stdout.write(f"{'Created' if created else 'Updated'} learning set: {course.slug}/{slug}")
        return learning_set

    def _sync_topic(self, course, item, order):
        title = item.get("title")
        slug = item.get("slug")
        if not title or not slug:
            self.stderr.write(
                f"Skipping topic on course '{course.slug}', missing title/slug: {item}"
            )
            return None

        defaults = {
            "title": title,
            "description": item.get("description", ""),
            "order": order,
            "is_active": True,
        }

        topic, created = Topic.objects.update_or_create(
            course=course, slug=slug, defaults=defaults
        )
        self.stdout.write(f"{'Created' if created else 'Updated'} topic: {course.slug}/{slug}")
        return topic
