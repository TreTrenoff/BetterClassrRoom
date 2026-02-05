from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================================================
# USER
# =========================================================

class User(AbstractUser):
    """
    Utilisateur étendu basé sur AbstractUser.

    Django gère déjà :
    - username
    - password hashé
    - permissions
    - groups
    - sessions

    On ajoute uniquement les champs métier spécifiques.
    """

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"
        ADMIN = "admin", "Admin"

    # Email unique → permet login par email si besoin
    email = models.EmailField(unique=True)

    # Infos profil
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    # Rôle métier simple (plus léger que Groups pour 90% des cas)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def __str__(self):
        return self.username

    # Helpers ergonomiques (lisibilité du code métier)
    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN


# =========================================================
# COURSE
# =========================================================

class Course(models.Model):
    """
    Représente un cours créé par un enseignant.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()

    # Propriétaire du cours
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================================================
# RANK / SCORE
# =========================================================

class Rank(models.Model):
    """
    Score d'un utilisateur pour un cours.
    Un utilisateur ne peut avoir qu'un seul score par cours.
    """

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
