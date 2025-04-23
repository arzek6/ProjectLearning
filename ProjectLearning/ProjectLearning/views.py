from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Project, ProjectTask  # Добавь ProjectTask, если используешь задачи
from .forms import ProjectCreateForm
import os
from .models import ChatMessage
from django.shortcuts import get_object_or_404

from django.utils.timezone import localtime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def home(request):
    print(f'Пользователь: {request.user}, Аутентифицирован: {request.user.is_authenticated}')
    return render(request, 'ProjectLearning/Main.html')

def create_project(request):
    return render(request, 'ProjectLearning/create_project.html')

@login_required(login_url='/accounts/login/')
def create_project_view(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
        return redirect('/projects/')
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            tasks = request.POST.getlist('tasks[]')
            for task in tasks:
                if task.strip():
                    ProjectTask.objects.create(project=project, title=task.strip())

            # Обработка приглашений
            invite_emails = request.POST.getlist('invite-emails[]')
            for email in invite_emails:
                email = email.strip()
                if email:
                    try:
                        student = User.objects.get(email=email, profile__role='student')
                        project.members.add(student)
                    except User.DoesNotExist:
                        messages.error(request, f"Ученик с email {email} не найден.")

            messages.success(request, "Проект успешно создан.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectCreateForm()
    return render(request, 'ProjectLearning/create_project.html', {'form': form})


@login_required(login_url='/accounts/login/')
def all_projects_view(request):
    projects_list = Project.objects.all()
    return render(request, 'ProjectLearning/projects.html', {'projects': projects_list})

@login_required(login_url='/accounts/login/')
def projects_view(request):
    query = request.GET.get('q', '')

    if request.user.is_authenticated:
        if request.user.profile.role == 'teacher':
            projects = Project.objects.filter(creator=request.user)
        elif request.user.profile.role == 'student':
            projects = Project.objects.filter(members=request.user)
        else:
            projects = Project.objects.none()
    else:
        projects = Project.objects.none()

    # Фильтрация по запросу
    if query:
        projects = projects.filter(name__icontains=query)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'ProjectLearning/projects_list.html', {'projects': projects})

    return render(request, 'ProjectLearning/projects.html', {'projects': projects})


@login_required(login_url='/accounts/login/')
def project_detail(request, project_id):
    project = get_object_or_404(Project.objects.prefetch_related('members', 'tasks', 'files', 'chat_messages'), id=project_id)

    # ✅ Проверка доступа: пользователь должен быть либо создателем, либо участником
    if request.user != project.creator and request.user not in project.members.all():
        return redirect('/projects/')  # или просто: return redirect('/projects/')

    # Получаем только сообщения с файлами
    chat_files = project.chat_messages.filter(file__isnull=False).exclude(file='')

    return render(request, 'ProjectLearning/project_details.html', {
        'project': project,
        'chat_files': chat_files
    })


@login_required(login_url='/accounts/login/')
def get_chat_messages(request, project_id):
    project = Project.objects.get(id=project_id)
    chat_messages  = project.chat_messages.select_related('sender').order_by('timestamp')
    data = [
        {
            'sender': f"{msg.sender.first_name}" if msg.sender.first_name else msg.sender.username,
            'message': msg.message,
            'timestamp': localtime(msg.timestamp).strftime('%d.%m %H:%M'),
            'file_url': msg.file.url if msg.file and hasattr(msg.file, 'url') else None,
            'file_name': os.path.basename(msg.file.name) if msg.file else None

        }
        for msg in chat_messages
    ]
    return  JsonResponse(data, safe=False)



@csrf_exempt
@require_POST
@login_required
def post_chat_message(request, project_id):
    project = Project.objects.get(id=project_id)
    message_text = request.POST.get('message', '').strip()
    file = request.FILES.get('file')

    if not message_text and not file:
        return JsonResponse({'status': 'error', 'message': 'Пустое сообщение'}, status=400)

    # Создаём сообщение и сохраняем его в переменную
    new_msg = ChatMessage.objects.create(
        project=project,
        sender=request.user,
        message=message_text,
        file=file
    )

    return JsonResponse({
        'status': 'ok',
        'file_url': new_msg.file.url if new_msg.file else None,
        'file_name': os.path.basename(new_msg.file.name) if new_msg.file else None
    }, status=200)


@csrf_exempt  # Только для тестов, лучше CSRF токен в JS потом передавать
@require_POST
@login_required
def toggle_task_completion(request):
    task_id = request.POST.get('task_id')

    try:
        task = ProjectTask.objects.get(id=task_id)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({'status': 'ok', 'is_completed': task.is_completed})
    except ProjectTask.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Задача не найдена'}, status=404)

@require_POST
@login_required
def remove_member(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.user != project.creator:
        return JsonResponse({'status': 'error', 'message': 'Нет прав'}, status=403)

    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        project.members.remove(user)
        return JsonResponse({'status': 'ok'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'}, status=400)

@require_POST
@login_required
def invite_member(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.user != project.creator:
        return JsonResponse({'status': 'error', 'message': 'Нет прав'}, status=403)

    email = request.POST.get('email', '').strip()
    try:
        user = User.objects.get(email=email, profile__role='student')
        project.members.add(user)
        return JsonResponse({'status': 'ok'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'}, status=400)
