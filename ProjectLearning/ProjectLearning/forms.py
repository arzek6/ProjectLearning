from django import forms
from django.contrib.auth.models import User
from .models import Project

class ProjectCreateForm(forms.ModelForm):
    invite_emails = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Введите email учеников через запятую'}),
        label='Пригласить учеников',
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'invite_emails']
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
        }

    def clean_invite_emails(self):
        emails = self.cleaned_data['invite_emails']
        email_list = [email.strip() for email in emails.split(',') if email.strip()]
        not_found = []

        found_users = []
        for email in email_list:
            try:
                user = User.objects.get(email=email)
                found_users.append(user)
            except User.DoesNotExist:
                not_found.append(email)

        if not_found:
            raise forms.ValidationError(f"Пользователи не найдены: {', '.join(not_found)}")

        return found_users
