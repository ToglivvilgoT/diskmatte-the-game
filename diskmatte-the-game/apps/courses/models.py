from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LearningSet(models.Model):
    course = models.ForeignKey(Course, related_name="learning_sets", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    kind = models.CharField(max_length=50, default="course_book")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        unique_together = ("course", "slug")

    def __str__(self):
        return f"{self.course.name}: {self.name}"


class Chapter(models.Model):
    learning_set = models.ForeignKey(LearningSet, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        unique_together = ("learning_set", "slug")

    def __str__(self):
        return self.title
