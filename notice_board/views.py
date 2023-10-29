from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
import random, time

from django.core.mail import send_mail

class EmailCheckView(View):
    class CheckNumber:
        def __init__(self, number, user):
            self.number = number
            self.user = user

    def get(self, request, *args, **kwargs):
        check_number =random.randint(1000, 9999)
        try:
            user_for_check = request.user
            send_mail(
                subject=f'Подтверждение электронной почты',
                message=f'Код для подтверждения {check_number}',
                from_email='aigulapai@yandex.ru',
                recipient_list=[user_for_check.email]
            )
            self.CheckNumber.number = check_number
            self.CheckNumber.user = user_for_check
            return render(request, 'check_email.html')
        except:
            return redirect('account_signup')

    def post(self, request, *args, **kwargs):
        check_code = int(request.POST.get('code'))
        number = self.CheckNumber.number
        user = self.CheckNumber.user
        if number == check_code:
            return redirect('notice_board:allAds')
        User.objects.get(pk=user.pk).delete()
        return render(request, 'error_message.html')



class NoticeLists(ListView):
    model = Ad
    template_name = 'notices.html'
    context_object_name = 'ads'
    ordering = ['-createDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            username = self.request.user.username
            author = Author.objects.get(authorUser=self.request.user)
            pk_list = []
            replyes_list = []
            for ad in context['ads']:
                # Определяем все объявления пользователя
                if ad.adAuthor.authorUser.username == username:
                    pk_list.append(ad.pk)
                # Если объявленеи не пользователя, то можно откликнуться
                else:
                    try:
                        # Выбираем отклики пользователя на обявления
                        replyes_list.append(Reply.objects.get(replyAd=ad, replyAuthor=author).replyAd.pk)
                    except:
                        pass
            context['pk_list'] = pk_list
            context['replyes_list'] = replyes_list
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

class ReplyList(ListView):
    model = Reply
    template_name = 'replyes.html'
    ordering = ['-replyCreateDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Author.objects.get(authorUser=self.request.user)
        try:
            context['replyes'] = Reply.objects.filter(replyAd__adAuthor=user)
        except:
            context['replyes'] = False
        return context


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'send_reply.html'
    form_class = RetryForms

    def post(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(authorUser=user)
        ad_id = int(request.path.split('/')[2])
        form = RetryForms(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replyAd = Ad.objects.get(pk=ad_id)
            reply.replyAuthor = author
            reply.save()
            return redirect('notice_board:allAds')
        else:
            form = AdForms()
            return render(request, "send_reply.html", {"form": form})

class ReplyDelete(DeleteView):
    template_name = 'replyDelete.html'
    queryset = Reply.objects.all()
    success_url = reverse_lazy('notice_board:allAds')

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


