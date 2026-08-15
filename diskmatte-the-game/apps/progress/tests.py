from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.courses.models import Course, LearningSet, Topic
from apps.tasks.models import Task

from .models import DiskTransaction, TaskCompletion, UserWallet


class TaskCompletionTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="student",
			password="test-password",
		)
		course = Course.objects.create(name="Algebra", slug="algebra")
		learning_set = LearningSet.objects.create(
			course=course,
			name="Course Book",
			slug="course-book",
		)
		topic = Topic.objects.create(course=course, title="Functions", slug="functions")
		self.task = Task.objects.create(
			learning_set=learning_set,
			topic=topic,
			title="Solve for x",
			slug="solve-for-x",
			prompt="Solve 2x + 3 = 7.",
			expected_answer="4",
		)

	def test_completion_is_unique_per_user_and_task(self):
		first, created = TaskCompletion.objects.get_or_create(user=self.user, task=self.task)
		second, created_again = TaskCompletion.objects.get_or_create(user=self.user, task=self.task)

		self.assertTrue(created)
		self.assertFalse(created_again)
		self.assertEqual(first.pk, second.pk)
		self.assertEqual(TaskCompletion.objects.filter(user=self.user).count(), 1)

	def test_progress_dashboard_requires_login(self):
		response = self.client.get(reverse("progress:index"))

		self.assertRedirects(response, f"/accounts/login/?next={reverse('progress:index')}")

	def test_progress_dashboard_shows_solved_task_count(self):
		UserWallet.objects.create(user=self.user, balance=100)
		TaskCompletion.objects.create(user=self.user, task=self.task)
		self.client.login(username="student", password="test-password")

		response = self.client.get(reverse("progress:index"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "100 disks")
		self.assertContains(response, "Antal lösta uppgifter: 1.")
		self.assertContains(response, "Solve for x")

	def test_completing_task_awards_configured_disks_once(self):
		self.client.login(username="student", password="test-password")
		self.task.disk_reward = 150
		self.task.save(update_fields=["disk_reward"])

		result = self.client.post(
			reverse(
				"tasks:task-detail",
				args=("algebra", "course-book", "functions", "solve-for-x"),
			),
			{"answer": "4"},
		)

		self.assertEqual(result.status_code, 200)
		self.assertEqual(UserWallet.objects.get(user=self.user).balance, 150)
		self.assertEqual(DiskTransaction.objects.filter(user=self.user).count(), 1)

		self.client.post(
			reverse(
				"tasks:task-detail",
				args=("algebra", "course-book", "functions", "solve-for-x"),
			),
			{"answer": "4"},
		)

		self.assertEqual(UserWallet.objects.get(user=self.user).balance, 150)
		self.assertEqual(DiskTransaction.objects.filter(user=self.user).count(), 1)

# Create your tests here.
