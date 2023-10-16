from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *

def Test(request):
    print('HOHOHOHOHOHOHOHOH')
    return render(request,'default.html')


class NoticeLists(ListView):
    model = Author
    print('VJENRVINREN')
    template_name = 'default.html'
