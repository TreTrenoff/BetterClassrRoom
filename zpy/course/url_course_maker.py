import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
from django.http import HttpResponse

from db.models import Course, Chapter
from zpy.course.forms import CourseForm, ChapterForm


# -------------------------------------------------
# Permissions
# -------------------------------------------------
def teacher_or_admin(user):
    return (
        user.is_authenticated and
        (user.is_superuser or user.groups.filter(name="Teacher").exists())
    )

teacher_required = user_passes_test(teacher_or_admin)


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def chapter_template_path(course_title, chapter_title):
    """
    Retourne le chemin relatif du template Django pour un chapitre
    Exemple : media/courses/python-basics/introduction.html
    """
    return f"media/courses/{slugify(course_title)}/{slugify(chapter_title)}.html"


def ensure_chapter_template(course_title, chapter_title, content=None):
    """
    Crée le fichier template HTML du chapitre s'il n'existe pas
    """
    template_path = chapter_template_path(course_title, chapter_title)
    full_path = os.path.join(settings.TEMPLATES[0]["DIRS"][0], template_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if content is None:
        content = f"""{{% extends "base.html" %}}
{{% block content %}}

{{% block title %}}{chapter_title}{{% endblock %}}  
<p>Contenu du chapitre à écrire.</p>

{{% endblock %}}
"""

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    return template_path


# -------------------------------------------------
# Course Views
# -------------------------------------------------
@login_required
def course_list(request):
    if request.user.is_superuser:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(created_by=request.user)

    # Vérifie si c'est admin ou teacher
    can_manage = request.user.is_superuser or request.user.groups.filter(name="Teacher").exists()

    return render(request, "courses/course_list.html", {
        "courses": courses,
        "can_manage": can_manage,
    })


@login_required
@teacher_required
def course_create(request):
    """Créer un nouveau cours"""
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect("course_list")
    else:
        form = CourseForm()

    return render(request, "courses/course_form.html", {"form": form})


@login_required
@teacher_required
def course_update(request, course_id):
    """Modifier un cours"""
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)
    return render(request, "courses/course_form.html", {"form": form, "course": course})


@login_required
@teacher_required
def course_delete(request, course_id):
    """Supprimer un cours"""
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect("course_list")


# -------------------------------------------------
# Chapter Views
# -------------------------------------------------
@login_required
@teacher_required
def chapter_list(request, course_id):
    """Liste les chapitres d'un cours"""
    course = get_object_or_404(Course, id=course_id)
    chapters = Chapter.objects.filter(course=course)
    return render(request, "courses/chapter_list.html", {"course": course, "chapters": chapters})


@login_required
@teacher_required
def chapter_create(request, course_id):
    """Créer un chapitre et générer le template HTML"""
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.course = course
            chapter.save()

            ensure_chapter_template(course.title, chapter.title)

            return redirect("chapter_list", course_id=course.id)
    else:
        form = ChapterForm()
    return render(request, "courses/chapter_form.html", {"form": form, "course": course})


@login_required
@teacher_required
def manage_courses(request):
    """Page pour gérer tous les cours avec barre de recherche"""
    query = request.GET.get("q", "")  # Récupère le texte de recherche
    if request.user.is_superuser:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(created_by=request.user)

    if query:
        courses = courses.filter(title__icontains=query)

    return render(request, "courses/manage_courses.html", {
        "courses": courses,
        "query": query,
    })


@login_required
@teacher_required
def chapter_update(request, course_id, chapter_id):
    """Modifier un chapitre"""
    course = get_object_or_404(Course, id=course_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, course=course)

    if request.method == "POST":
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            ensure_chapter_template(course.title, chapter.title)
            return redirect("chapter_list", course_id=course.id)
    else:
        form = ChapterForm(instance=chapter)

    return render(request, "courses/chapter_form.html", {"form": form, "course": course, "chapter": chapter})


@login_required
@teacher_required
def chapter_delete(request, course_id, chapter_id):
    """Supprimer un chapitre"""
    course = get_object_or_404(Course, id=course_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, course=course)

    if request.method == "POST":
        chapter.delete()
        return redirect("chapter_list", course_id=course.id)

    return render(request, "courses/chapter_confirm_delete.html", {"course": course, "chapter": chapter})


@login_required
def chapter_view(request, course_id, chapter_id):
    """Afficher un chapitre"""
    course = get_object_or_404(Course, id=course_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, course=course)

    template_path = chapter_template_path(course.title, chapter.title)

    try:
        return render(request, template_path, {"course": course, "chapter": chapter})
    except:
        return render(request, "courses/chapter_not_found.html", {"course": course, "chapter": chapter})
