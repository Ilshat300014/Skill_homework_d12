from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
    # permission_required = ('news.add_post',)
    template_name = 'adCreate.html'
    form_class = AdForms

    def post(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(authorUser=user)
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            ad = form.save(commit=False)
            ad.adAuthor = author
            ad.save()
        return redirect('notice_board:allAds')

class AdDetail(DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        print(username)
        context['is_author'] = context['ad'].adAuthor.authorUser.username == username
        return context

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
# class PostCreate(PermissionRequiredMixin, CreateView):
#     model = Post
#     permission_required = ('news.add_post',)
#     template_name = 'adCreate.html'
#     form_class = PostForms
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
#         author = request.POST['author']
#         today = datetime.today().date()
#         author_post_count = Post.objects.filter(author=author, createDate__date=today).count()
#         if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
#             if author_post_count < 3:
#                 form.save()
#                 return redirect('news:allNews')
#             else:
#                 return render(request, 'limit_error.html')
#
# class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
#     permission_required = ('news.change_post',)
#     template_name = 'adCreate.html'
#     form_class = PostForms
#
#     def get_object(self, **kwargs):
#         id = self.kwargs.get('pk')
#         return Post.objects.get(pk=id)
#
# class PostDelete(DeleteView):
#     template_name = 'postDelete.html'
#     queryset = Post.objects.all()
#     success_url = reverse_lazy('news:allNews')

