# users/views.py

from django.shortcuts               import render, redirect
from django.contrib.auth            import login
from django.contrib.auth.decorators import login_required
from django.contrib                import messages

# Importa aquí tu SignUpForm y ProfileForm recién creados:
from .forms                         import SignUpForm, ProfileForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def profile_update_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil actualizado.')
        return redirect('users:profile')
    return render(request, 'users/profile_edit.html', {'form': form})
