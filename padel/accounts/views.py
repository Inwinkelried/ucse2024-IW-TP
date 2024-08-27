from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import JugadorRegisterForm 
from django.urls import reverse_lazy
from django.views.generic import CreateView















def JugadorRegisterView(request):
    context = {}
    if request.method == 'POST':
        form = JugadorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context['register_form'] = form
    else:
        form = JugadorRegisterForm()
        context['register_form'] = form
    return render(request, 'registration/signup.html', {'form': form})



# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"