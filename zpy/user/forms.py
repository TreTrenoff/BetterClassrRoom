from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from db.models import Profile  # ici le Profile avec Role

from django import forms
from django.contrib.auth import authenticate

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom", max_length=150)
    last_name = forms.CharField(label="Nom", max_length=150)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        # Crée ou met à jour le Profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = self.cleaned_data["role"]
        profile.bio = self.cleaned_data.get("bio", "")

        avatar = self.cleaned_data.get("avatar")
        if avatar:
            profile.avatar = avatar  # Django gère l'upload automatiquement
        
        profile.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur ou email")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user


# ==============================
# UPDATE USER (pré-rempli auto)
# ==============================

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


# ==============================
# UPDATE PROFILE (pré-rempli auto)
# ==============================

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]

# -------------------------------------------------
# SUPPRESSION COMPTE (avec mot de passe)
# -------------------------------------------------
class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Confirmer mot de passe")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        pwd = self.cleaned_data["password"]

        if not authenticate(username=self.user.username, password=pwd):
            raise forms.ValidationError("Mot de passe incorrect.")

        return pwd