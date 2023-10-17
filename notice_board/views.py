from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *


class NoticeLists(ListView):
    model = Ad
    template_name = 'notices.html'
    context_object_name = 'ads'
    ordering = ['-createDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        print(self.request.GET)
        # context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

