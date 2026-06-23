from django.shortcuts import render, redirect

# Create your views here.

def home_redirect(request):
    return redirect('/admin/login/')