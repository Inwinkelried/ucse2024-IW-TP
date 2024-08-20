from django.shortcuts import render, redirect
from django.contrib.auth import login
from forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio después del registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
 
@login_required
def protected_page(request):
    return render(request, 'protected.html')
