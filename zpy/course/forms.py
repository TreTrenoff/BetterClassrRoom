from django import forms
from db.models import Course, Chapter

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ["course", "title", "content"]
