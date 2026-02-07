from django.urls import path
from django.shortcuts import render
from zpy.course.url_course_maker import chapter_create, course_create, course_list
from zpy.user.url_user import dashboard, login_view, register_view, logout_view
from zpy.admin.urls_admin import manage_roles_permissions, admin_dashboard

def index(request):
    return render(request, "index.html")



urlpatterns = [
    path("", index, name="home"),
    path("login", login_view, name="login"),
    path("register", register_view, name="register"),
    path("logout", logout_view, name="logout"),
    path("dashboard", dashboard, name="dashboard"),
    path("admin/manage-roles-permissions/", manage_roles_permissions, name="admin_manage_roles_permissions"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("course/list/", course_list, name="course_list"),
    path("course/create/", course_create, name="course_create"),
    path('course/<int:course_id>/chapter/create/', chapter_create, name='chapter_create'),
    
]
