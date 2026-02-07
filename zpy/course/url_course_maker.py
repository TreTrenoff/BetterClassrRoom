from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from db.models import Course, Chapter
from zpy.course.forms import CourseForm, ChapterForm

@login_required
def course_list(request):
    # Affiche tous les cours de l'utilisateur (ou tous les cours si admin)
    if request.user.is_superuser:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(created_by=request.user)
    return render(request, "courses/course_list.html", {"courses": courses})

@login_required
def course_create(request):
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
def chapter_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.course = course
            chapter.save()
            return redirect("course_list")
    else:
        form = ChapterForm(initial={"course": course})
    return render(request, "courses/chapter_form.html", {"form": form, "course": course})
