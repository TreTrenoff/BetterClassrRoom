# db/models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# =========================================================
# PROFILE
# =========================================================
class Profile(models.Model):
    """
    Profile étendu pour un utilisateur standard.
    Contient les champs métier spécifiques :
    - role
    - bio
    - avatar
    """
    class RoleRequestStatus(models.TextChoices):
        PENDING = "pending", "En attente"
        APPROVED = "approved", "Approuvé"
        REJECTED = "rejected", "Refusé"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - {self.role}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar # /media/avatars/xxx.png

        return settings.STATIC_URL + "default_avatar.png"

    # Propriétés pratiques
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
    Cours créé par un enseignant.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses_created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    """
    Chapitre d'un cours, correspondant à une page HTML.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(blank=True)  # Optionnel si on utilise un fichier HTML externe

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def get_html_path(self):
        """
        Retourne le chemin du fichier HTML si défini.
        """
        if self.html_file:
            return self.html_file.url
        return None


# =========================================================
# RANK / SCORE
# =========================================================
class Rank(models.Model):
    """
    Score d'un utilisateur pour un cours.
    Un utilisateur ne peut avoir qu'un seul score par cours.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_user_course_rank")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.title}: {self.score}"


# =========================================================
# SIGNAL POUR CRÉER LE PROFILE AUTOMATIQUEMENT
# =========================================================
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement un Profile à la création d'un User.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
