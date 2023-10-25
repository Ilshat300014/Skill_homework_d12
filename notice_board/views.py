from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *

class NoticeLists(ListView):
    model = Ad
    template_name = 'notices.html'
    context_object_name = 'ads'
    ordering = ['-createDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        pk_list = []
        for ad in context['ads']:
            if ad.adAuthor.authorUser.username == username:
                pk_list.append(ad.pk)
        context['pk_list'] = pk_list
        context['anonymous'] = self.request.user.is_anonymous
        return context

class AdCreate(CreateView):
    model = Ad
    template_name = 'adCreate.html'
    form_class = AdForms

    def post(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(authorUser=user)
        form = AdForms(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.adAuthor = author
            ad.save()
            return redirect('notice_board:allAds')
        else:
            form = AdForms()
        return render(request, "adCreate.html", {"form": form})

        # form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        # # print(dir(form))
        # # print(form.data['adFile'])
        # print(form.changed_data)
        # if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
        #     print('valid')
        #     ad = form.save(commit=False)
        #     ad.adAuthor = author
        #     ad.save()
        #     return redirect('notice_board:allAds')

class AdDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['is_author'] = context['ad'].adAuthor.authorUser.username == username
        try:
            context['have_file'] = bool(context['ad'].adFile.url)
            return context
        except:
            context['have_file'] = False
            return context

class AdUpdate(UpdateView):
    template_name = 'adCreate.html'
    form_class = AdForms

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

class AdDelete(DeleteView):
    template_name = 'adDelete.html'
    queryset = Ad.objects.all()
    success_url = reverse_lazy('notice_board:allAds')

class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'send_reply.html'
    form_class = RetryForm

    def post(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(authorUser=user)
        form = self.form_class(request.POST)
        print(form)
        # form = AdForms(request.POST, request.FILES)
        # if form.is_valid():
        #     ad = form.save(commit=False)
        #     ad.adAuthor = author
        #     ad.save()
        #     return redirect('notice_board:allAds')
        # else:
        #     form = AdForms()
        # return render(request, "adCreate.html", {"form": form})


# class SearchNews(ListView):
#     model = Post
#     template_name = 'search.html'
#     context_object_name = 'filter_posts'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
#         return context
#

#
#     def get_object(self, *args, **kwargs):
#         # кэш очень похож на словарь, и метод get действует также.
#         # Он забирает значение по ключу, если его нет, то забирает None.
#         obj = cache.get(f'post-{self.kwargs["pk"]}', None)
#         # если объекта нет в кэше, то получаем его и записываем в кэш
#         if not obj:
#             obj = super().get_object(queryset=self.queryset)
#         return obj
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             user = self.request.user
#             categoryModel = self.object.category.get_queryset()  # Получаем все категории поста
#             category_names = []
#             for c in categoryModel:
#                 if not user.category_set.filter(categoryName=c.categoryName).exists():
#                     context['is_not_subscr'] = True
#                     category_names.append(c.categoryName)
#             context['category_names'] = category_names
#             return context
#         except:
#             return context
#

#

#


