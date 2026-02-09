import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify

from db.models import Course, Chapter
from zpy.course.forms import CourseForm, ChapterForm


# -------------------------------------------------
# Permission logic
# -------------------------------------------------

def teacher_or_admin(user):
    return (
        user.is_authenticated and
        (user.is_superuser or user.groups.filter(name="Teacher").exists())
    )


teacher_required = user_passes_test(teacher_or_admin)


# -------------------------------------------------
# Views
# -------------------------------------------------

@login_required
def course_list(request):
    if request.user.is_superuser:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(created_by=request.user)

    return render(request, "courses/course_list.html", {"courses": courses})


@login_required
@teacher_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()

            course_dir = os.path.join(
                settings.COURSES_ROOT,
                slugify(course.title)
            )

            os.makedirs(course_dir, exist_ok=True)

            return redirect("course_list")

    else:
        form = CourseForm()

    return render(request, "courses/course_form.html", {"form": form})


@login_required
@teacher_required
def chapter_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = ChapterForm(request.POST)

        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.course = course
            chapter.save()

            course_slug = slugify(course.title)
            chapter_slug = slugify(chapter.title)

            course_dir = os.path.join(settings.COURSES_ROOT, course_slug)
            os.makedirs(course_dir, exist_ok=True)

            file_path = os.path.join(course_dir, f"{chapter_slug}.html")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"<h1>{chapter.title}</h1>\n")

            return redirect("course_list")

    else:
        form = ChapterForm()

    return render(request, "courses/chapter_form.html", {
        "form": form,
        "course": course
    })
