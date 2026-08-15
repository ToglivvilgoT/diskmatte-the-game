from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.progress.models import TaskCompletion
from .models import Course, LearningSet, Topic
from apps.tasks.models import Task

User = get_user_model()


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
        self.topic = Topic.objects.create(
            course=self.course,
            title="Functions",
            slug="functions",
            description="An introduction to functions.",
            order=1,
            is_active=True,
        )
        self.task = Task.objects.create(
            learning_set=self.learning_set,
            topic=self.topic,
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

    def test_course_detail_links_to_learning_sets(self):
        response = self.client.get(
            reverse("courses:course-detail", kwargs={"slug": self.course.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course Book")
        self.assertContains(
            response,
            reverse(
                "courses:learning-set-detail",
                kwargs={"course_slug": self.course.slug, "slug": self.learning_set.slug},
            ),
        )

    def test_learning_set_detail_links_to_tasks(self):
        response = self.client.get(
            reverse(
                "courses:learning-set-detail",
                kwargs={"course_slug": self.course.slug, "slug": self.learning_set.slug},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solve for x")
        self.assertContains(
            response,
            reverse(
                "tasks:task-detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "learning_set_slug": self.learning_set.slug,
                    "topic_slug": self.topic.slug,
                    "slug": self.task.slug,
                },
            ),
        )

    def test_learning_set_detail_marks_completed_tasks_for_signed_in_user(self):
        user = User.objects.create_user(username="student", password="test-password")
        TaskCompletion.objects.create(user=user, task=self.task)
        self.client.login(username="student", password="test-password")

        response = self.client.get(
            reverse(
                "courses:learning-set-detail",
                kwargs={"course_slug": self.course.slug, "slug": self.learning_set.slug},
            )
        )

        self.assertContains(response, "Completed")
        self.assertContains(response, "list-group-item-success")

    def test_topic_detail_shows_tasks(self):
        response = self.client.get(
            reverse(
                "courses:topic-detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "learning_set_slug": self.learning_set.slug,
                    "topic_slug": self.topic.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solve for x")
