from django.test import TestCase
from django.urls import reverse

from .models import Chapter, Course, LearningSet
from apps.tasks.models import Task


class CourseBrowsingTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Algebra",
            slug="algebra",
            description="An introductory algebra course.",
            is_active=True,
        )
        self.learning_set = LearningSet.objects.create(
            course=self.course,
            name="Course Book",
            slug="course-book",
            kind="course_book",
            description="The main course book content.",
            order=1,
            is_active=True,
        )
        self.chapter = Chapter.objects.create(
            learning_set=self.learning_set,
            title="Functions",
            slug="functions",
            description="An introduction to functions.",
            order=1,
            is_active=True,
        )
        self.task = Task.objects.create(
            learning_set=self.learning_set,
            chapter=self.chapter,
            title="Solve for x",
            slug="solve-for-x",
            prompt="Solve 2x + 3 = 7.",
            answer_type="text",
            expected_answer="2",
            order=1,
            is_published=True,
        )

    def test_course_list_displays_active_courses(self):
        response = self.client.get(reverse("courses:course-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra")

    def test_course_detail_shows_learning_sets_and_chapters(self):
        response = self.client.get(
            reverse("courses:course-detail", kwargs={"slug": self.course.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course Book")
        self.assertContains(response, "Functions")

    def test_chapter_detail_shows_tasks(self):
        response = self.client.get(
            reverse(
                "courses:chapter-detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "learning_set_slug": self.learning_set.slug,
                    "slug": self.chapter.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solve for x")
