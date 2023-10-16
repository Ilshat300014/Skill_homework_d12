from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *


class NoticeLists(ListView):
    model = Ad
    template_name = 'notices.html'
    context_object_name = 'ads'
    ordering = ['-createDate']
    paginate_by = 10
