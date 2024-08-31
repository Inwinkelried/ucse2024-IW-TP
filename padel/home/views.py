from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def protected_page(request):
    return render(request, 'protected.html')





