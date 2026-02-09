from django.urls import path
from django.shortcuts import render
from zpy.course.url_course_maker import (
    chapter_create, chapter_view, chapter_update, chapter_delete, chapter_list,
    course_create, course_list, course_update, course_delete, manage_courses
)
from zpy.user.url_user import dashboard, login_view, register_view, logout_view
from zpy.admin.urls_admin import manage_roles_permissions, admin_dashboard

def index(request):
    return render(request, "index.html")

urlpatterns = [
    # Pages générales
    path("", index, name="home"),
    path("login", login_view, name="login"),
    path("register", register_view, name="register"),
    path("logout", logout_view, name="logout"),
    path("dashboard", dashboard, name="dashboard"),

    # Admin
    path("admin/manage-roles-permissions/", manage_roles_permissions, name="admin_manage_roles_permissions"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),

    # Courses
    path("course/list/", course_list, name="course_list"),
    path("course/create/", course_create, name="course_create"),
    path("course/<int:course_id>/update/", course_update, name="course_update"),
    path("course/<int:course_id>/delete/", course_delete, name="course_delete"),

    # Chapters
    path('course/<int:course_id>/chapter/list/', chapter_list, name='chapter_list'),
    path('course/<int:course_id>/chapter/create/', chapter_create, name='chapter_create'),
    path('course/<int:course_id>/chapter/<int:chapter_id>/', chapter_view, name='chapter_view'),
    path('course/<int:course_id>/chapter/<int:chapter_id>/update/', chapter_update, name='chapter_update'),
    path('course/<int:course_id>/chapter/<int:chapter_id>/delete/', chapter_delete, name='chapter_delete'),
    path("course/manage/", manage_courses, name="course_manage"),

]
