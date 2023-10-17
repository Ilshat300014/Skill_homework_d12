from django.contrib import admin
from .models import *

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username',
#                     'email',
                    # 'choice',
                    # 'createDate',
                    # 'postRating'
                    # )
    # list_filter = ('author',
    #                'createDate',
    #                'postRating')  # добавляем примитивные фильтры в нашу админку
    # search_fields = ('author',
    #                  'postRating')  # тут всё очень похоже на фильтры из запросов в базу

# class PostCategoryAdmin(admin.ModelAdmin):
#     list_display = ('post',
#                     'category',
#                     )
#     list_filter = ('post__author',
#                    'category')  # добавляем примитивные фильтры в нашу админку

# Register your models here.
admin.site.register(Author)
admin.site.register(Ad)
admin.site.register(Reply)
