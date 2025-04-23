from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    # Название проекта
    name = models.CharField(max_length=255)

    # Полное описание проекта
    description = models.TextField()

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')

    members  = models.ManyToManyField(User, related_name='projects', blank=True)


    # Время создания и время последнего обновления
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProjectTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='project_files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)