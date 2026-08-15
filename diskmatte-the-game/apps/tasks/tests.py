from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.courses.models import Course, LearningSet, Topic
from .models import Task, TaskOption


class TaskDetailTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="student",
            password="test-password",
        )
        self.client.login(username="student", password="test-password")
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
            answer_type=Task.AnswerType.INPUT_FIELD,
            expected_answer="2",
            order=1,
            is_published=True,
        )

    def task_url(self, task=None):
        task = task or self.task
        return reverse(
            "tasks:task-detail",
            kwargs={
                "course_slug": self.course.slug,
                "learning_set_slug": self.learning_set.slug,
                "topic_slug": task.topic.slug,
                "slug": task.slug,
            },
        )

    def test_task_detail_page_renders_task_content(self):
        response = self.client.get(
            reverse(
                "tasks:task-detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "learning_set_slug": self.learning_set.slug,
                    "topic_slug": self.topic.slug,
                    "slug": self.task.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solve for x")
        self.assertContains(response, "Solve 2x + 3 = 7.")

    def test_task_detail_requires_login(self):
        self.client.logout()

        response = self.client.get(self.task_url())

        self.assertRedirects(response, f"/accounts/login/?next={self.task_url()}")

    def test_input_field_answer_is_validated(self):
        response = self.client.post(self.task_url(), {"answer": "2"})
        self.assertContains(response, "Rätt svar!")

        response = self.client.post(self.task_url(), {"answer": "3"})
        self.assertContains(response, "Det svaret blev fel. Försök igen.")

    def test_checkbox_answer_is_validated(self):
        task = Task.objects.create(
            learning_set=self.learning_set,
            topic=self.topic,
            title="Confirm the proof",
            slug="confirm-the-proof",
            prompt="Have you checked the proof?",
            answer_type=Task.AnswerType.CHECKBOX,
            is_published=True,
        )

        response = self.client.post(self.task_url(task), {"answer": "on"})
        self.assertContains(response, "Rätt svar!")

    def test_multiple_choice_answer_is_validated(self):
        task = Task.objects.create(
            learning_set=self.learning_set,
            topic=self.topic,
            title="Pick the answer",
            slug="pick-the-answer",
            prompt="Which answer is correct?",
            answer_type=Task.AnswerType.MULTIPLE_CHOICE,
            is_published=True,
        )
        correct_option = TaskOption.objects.create(task=task, label="Correct", is_correct=True)
        wrong_option = TaskOption.objects.create(task=task, label="Wrong", is_correct=False)

        response = self.client.post(self.task_url(task), {"answer": wrong_option.pk})
        self.assertContains(response, "Det svaret blev fel. Försök igen.")

        response = self.client.post(self.task_url(task), {"answer": correct_option.pk})
        self.assertContains(response, "Rätt svar!")


class TaskModelTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="student",
            password="test-password",
        )
        self.client.login(username="student", password="test-password")
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

    def test_task_defaults_to_input_field_answer_type(self):
        task = Task.objects.create(
            learning_set=self.learning_set,
            title="State whether the proof is complete",
            slug="proof-complete",
            prompt="Mark the task as done when you have checked the proof.",
        )

        self.assertEqual(task.answer_type, Task.AnswerType.INPUT_FIELD)

    def test_multiple_choice_options_are_returned_in_position_order(self):
        task = Task.objects.create(
            learning_set=self.learning_set,
            title="Pick the derivative",
            slug="pick-the-derivative",
            prompt="Which option is the derivative of x^2?",
            answer_type=Task.AnswerType.MULTIPLE_CHOICE,
        )
        TaskOption.objects.create(task=task, label="2x", is_correct=True, position=2)
        TaskOption.objects.create(task=task, label="x", is_correct=False, position=1)

        self.assertEqual(list(task.options.values_list("label", flat=True)), ["x", "2x"])

    def test_task_detail_page_renders_multiple_choice_options(self):
        topic = Topic.objects.create(
            course=self.course,
            title="Derivatives",
            slug="derivatives",
            description="Derivative basics.",
            order=1,
            is_active=True,
        )
        task = Task.objects.create(
            learning_set=self.learning_set,
            topic=topic,
            title="Pick the derivative",
            slug="pick-the-derivative",
            prompt="Which option is the derivative of x^2?",
            answer_type=Task.AnswerType.MULTIPLE_CHOICE,
            is_published=True,
        )
        TaskOption.objects.create(task=task, label="x", position=1)
        TaskOption.objects.create(task=task, label="2x", position=2, is_correct=True)

        response = self.client.get(
            reverse(
                "tasks:task-detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "learning_set_slug": self.learning_set.slug,
                    "topic_slug": topic.slug,
                    "slug": task.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pick the derivative")
        self.assertContains(response, "x")
        self.assertContains(response, "2x")
