import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.courses.models import Course, LearningSet, Topic
from apps.tasks.expressions import ExpressionError, evaluate_to_int
from apps.tasks.models import Task, TaskOption

TASKS_DIR = Path("tasks")


class Command(BaseCommand):
    help = (
        "Load tasks from static/tasks/<course_slug>/<learning_set_slug>.json files. "
        "Creates or updates tasks (and their options) to match the files, and marks "
        "tasks missing from the files as unpublished (is_published=False) instead of "
        "deleting them."
    )

    def handle(self, *args, **options):
        tasks_dir = Path(settings.BASE_DIR) / "static" / TASKS_DIR
        if not tasks_dir.is_dir():
            self.stderr.write(f"Tasks metadata directory not found: {tasks_dir}")
            return

        seen_task_ids = set()

        for course_dir in sorted(p for p in tasks_dir.iterdir() if p.is_dir()):
            course_slug = course_dir.name
            try:
                course = Course.objects.get(slug=course_slug)
            except Course.DoesNotExist:
                self.stderr.write(f"Course '{course_slug}' not found in database, skipping folder")
                continue

            for metadata_path in sorted(course_dir.glob("*.json")):
                self._sync_learning_set_file(course, metadata_path, seen_task_ids)

        missing = Task.objects.exclude(id__in=seen_task_ids).filter(is_published=True)
        for task in missing:
            task.is_published = False
            task.save()
            self.stdout.write(
                self.style.WARNING(f"Task '{task.slug}' missing from metadata, marking unpublished")
            )

    def _sync_learning_set_file(self, course, metadata_path, seen_task_ids):
        learning_set_slug = metadata_path.stem
        try:
            learning_set = LearningSet.objects.get(course=course, slug=learning_set_slug)
        except LearningSet.DoesNotExist:
            self.stderr.write(
                f"Learning set '{course.slug}/{learning_set_slug}' not found in database, skipping file"
            )
            return

        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                task_list = json.load(f)
        except json.JSONDecodeError as e:
            self.stderr.write(f"Failed to parse {metadata_path}: {e}")
            return

        if not isinstance(task_list, list):
            self.stderr.write(f"{metadata_path} must contain a JSON list")
            return

        for order, item in enumerate(task_list, start=1):
            task = self._sync_task(course, learning_set, item, order)
            if task is not None:
                seen_task_ids.add(task.id)

    def _sync_task(self, course, learning_set, item, order):
        location = f"{course.slug}/{learning_set.slug}"
        slug = item.get("slug")
        if not slug:
            self.stderr.write(f"Skipping task in '{location}', missing slug: {item}")
            return None

        topic = None
        topic_slug = item.get("topic_slug")
        if topic_slug:
            try:
                topic = Topic.objects.get(course=course, slug=topic_slug)
            except Topic.DoesNotExist:
                self.stderr.write(
                    f"Topic '{course.slug}/{topic_slug}' not found in database, "
                    f"skipping task '{location}/{slug}'"
                )
                return None

        answer_type, answer_type_error = self._resolve_answer_type(item)

        errors = []
        if not item.get("title"):
            errors.append("title")
        if not item.get("prompt"):
            errors.append("prompt")
        if answer_type_error:
            errors.append(answer_type_error)

        options = item.get("options", [])
        if answer_type == Task.AnswerType.MULTIPLE_CHOICE and not any(
            opt.get("is_correct") for opt in options
        ):
            errors.append("options (at least one is_correct=true required)")

        expected_answer = item.get("expected_answer", "")
        if answer_type == Task.AnswerType.EQUATION and not answer_type_error:
            try:
                expected_answer = str(evaluate_to_int(expected_answer))
            except ExpressionError as e:
                errors.append(f"expected_answer (invalid equation: {e})")

        is_published = not errors
        if errors:
            self.stderr.write(
                f"Task '{location}/{slug}' missing/invalid fields: {', '.join(errors)}"
            )

        defaults = {
            "learning_set": learning_set,
            "topic": topic,
            "title": item.get("title", ""),
            "prompt": item.get("prompt", ""),
            "instructions": item.get("instructions", ""),
            "answer_type": answer_type,
            "expected_answer": expected_answer,
            "hint": item.get("hint", ""),
            "solution": item.get("solution", ""),
            "image_url": item.get("image_url", ""),
            "external_link": item.get("external_link", ""),
            "book_reference": item.get("book_reference", ""),
            "disk_reward": item.get("disk_reward", 100),
            "order": order,
            "is_published": is_published,
        }

        task, created = Task.objects.update_or_create(
            learning_set=learning_set, slug=slug, defaults=defaults
        )
        self.stdout.write(f"{'Created' if created else 'Updated'} task: {location}/{slug}")

        self._sync_options(task, options)
        return task

    def _resolve_answer_type(self, item):
        """Derive answer_type from options/expected_answer/answer_format per the metadata rules."""
        has_options = bool(item.get("options"))
        has_expected_answer = bool(item.get("expected_answer"))
        is_equation = item.get("answer_format") == "equation"

        if is_equation and (not has_expected_answer or has_options):
            return (
                Task.AnswerType.INPUT_FIELD,
                "answer_format 'equation' requires expected_answer and no options",
            )
        if not has_options and not has_expected_answer:
            return Task.AnswerType.CHECKBOX, None
        if not has_options and has_expected_answer:
            return (Task.AnswerType.EQUATION if is_equation else Task.AnswerType.INPUT_FIELD), None
        if has_options and not has_expected_answer:
            return Task.AnswerType.MULTIPLE_CHOICE, None
        return Task.AnswerType.INPUT_FIELD, "invalid combination of options and expected_answer"

    def _sync_options(self, task, options):
        task.options.all().delete()
        TaskOption.objects.bulk_create(
            TaskOption(
                task=task,
                label=option.get("label", ""),
                is_correct=option.get("is_correct", False),
                position=position,
            )
            for position, option in enumerate(options, start=1)
        )
