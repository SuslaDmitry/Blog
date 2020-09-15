from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.models import Permission


# Create your views here.
def register(request):
    """Регистрирует нового пользователя."""
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Обработка заполненной формы.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Присваивание пользователю прав на доступ к админ панеле и редактированию постов
            new_user.is_staff = True
            permission = Permission.objects.get(codename='change_blogpost')
            new_user.user_permissions.add(permission)
            new_user.save()
            # Выполнение входа и перенаправление на домашнюю страницу.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('blogs:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout_view(request):
    """Завершает сеанс работы с приложением."""
    logout(request)
    return HttpResponseRedirect(reverse('blogs:index'))
