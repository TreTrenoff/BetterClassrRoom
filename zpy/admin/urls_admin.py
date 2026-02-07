from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from datetime import timedelta

from db.models import Course, Chapter, Rank
from zpy.admin.forms import PermissionForm, GroupForm


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@superuser_required
def admin_dashboard(request):
    """
    Dashboard admin avec statistiques globales.
    """

    now = timezone.now()
    today = now.date()
    last_24h = now - timedelta(hours=24)

    # =========================
    # USERS
    # =========================
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()

    new_today = User.objects.filter(date_joined__date=today).count()
    new_24h = User.objects.filter(date_joined__gte=last_24h).count()

    latest_users = User.objects.order_by("-date_joined")[:5]

    # =========================
    # GROUPS / PERMISSIONS
    # =========================
    total_groups = Group.objects.count()
    total_permissions = Permission.objects.count()

    # =========================
    # PLATFORM DATA
    # =========================
    total_courses = Course.objects.count()
    total_chapters = Chapter.objects.count()
    total_ranks = Rank.objects.count()

    context = {
        "total_users": total_users,
        "active_users": active_users,
        "staff_users": staff_users,
        "superusers": superusers,
        "new_today": new_today,
        "new_24h": new_24h,
        "latest_users": latest_users,

        "total_groups": total_groups,
        "total_permissions": total_permissions,

        "total_courses": total_courses,
        "total_chapters": total_chapters,
        "total_ranks": total_ranks,
    }

    return render(request, "admin/dashboard.html", context)

@superuser_required
def manage_roles_permissions(request):

    groups = Group.objects.all()
    permissions = Permission.objects.all()

    group_instance = None
    perm_instance = None

    # =========================
    # MODE EDIT (GET)
    # =========================
    edit_group_id = request.GET.get("edit_group")
    edit_perm_id = request.GET.get("edit_perm")

    if edit_group_id:
        group_instance = get_object_or_404(Group, id=edit_group_id)

    if edit_perm_id:
        perm_instance = get_object_or_404(Permission, id=edit_perm_id)

    group_form = GroupForm(instance=group_instance)
    permission_form = PermissionForm(instance=perm_instance)

    # =========================
    # POST HANDLER
    # =========================
    if request.method == "POST":

        # -------- GROUPE SAVE --------
        if "save_group" in request.POST:
            group_id = request.POST.get("group_id")

            if group_id:
                instance = get_object_or_404(Group, id=group_id)
                form = GroupForm(request.POST, instance=instance)
            else:
                form = GroupForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("admin_manage_roles_permissions")

        # -------- GROUPE DELETE --------
        elif "delete_group" in request.POST:
            group_id = request.POST.get("group_id")
            if group_id:
                Group.objects.filter(id=group_id).delete()
                return redirect("admin_manage_roles_permissions")

        # -------- PERMISSION SAVE --------
        elif "save_permission" in request.POST:
            perm_id = request.POST.get("perm_id")

            if perm_id:
                instance = get_object_or_404(Permission, id=perm_id)
                form = PermissionForm(request.POST, instance=instance)
            else:
                form = PermissionForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("admin_manage_roles_permissions")

        # -------- PERMISSION DELETE --------
        elif "delete_permission" in request.POST:
            perm_id = request.POST.get("perm_id")
            if perm_id:
                Permission.objects.filter(id=perm_id).delete()
                return redirect("admin_manage_roles_permissions")

    return render(request, "admin/manage_roles_permissions.html", {
        "groups": groups,
        "permissions": permissions,
        "group_form": group_form,
        "permission_form": permission_form,
        "edit_group_id": edit_group_id,
        "edit_perm_id": edit_perm_id,
    })
