from django.shortcuts import render, redirect
from zpy.user.forms import LoginForm, ProfileUpdateForm, RegisterForm, DeleteAccountForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")  # page après login

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # crée la session
            return redirect("/")  # redirige vers la page d'accueil ou dashboard
    else:
        form = LoginForm()

    return render(request, "user/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")  # redirige vers login

# ================================
# LOGIQUE MÉTIER SÉPARÉE
# ================================

def process_account_delete(delete_form, request):
    """
    Supprime le compte après validation mot de passe
    """
    if delete_form.is_valid():
        request.user.delete()
        logout(request)
        return True
    return False



def process_profile_update(user_form, profile_form):
    """
    Sauvegarde les modifications utilisateur + profil
    """
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return True
    return False

# ==============================
# DASHBOARD
# ==============================

@login_required
def dashboard(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        delete_form = DeleteAccountForm(request.user, request.POST)
        # ------- UPDATE PROFILE -------
        if "save_profile" in request.POST:
            if process_profile_update(user_form, profile_form):
                return redirect("/dashboard")

        # ------- DELETE ACCOUNT -------
        elif "delete_account" in request.POST:
            if process_account_delete(delete_form, request):
                return redirect("/")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        delete_form = DeleteAccountForm(request.user)

    return render(request, "user/dashboard.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "delete_form": delete_form
    })
