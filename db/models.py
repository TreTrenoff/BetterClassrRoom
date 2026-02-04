from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# User custom sécurisé
# =========================

class User(AbstractUser):
    """
    Étend le système d'auth Django.
    Le password reste hashé automatiquement par Django.
    """
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username


# =========================
# Course
# =========================

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# Rank / Score
# =========================

class Rank(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scores"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="scores"
    )

    score = models.IntegerField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_course_rank"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.title}: {self.score}"
