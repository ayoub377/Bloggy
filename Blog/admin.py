from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter

from Blog.models import Category, Profile, Article, Comment


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ['user', ]


# Registers the author profile model at the admin backend.
admin.site.register(Profile, ProfileAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'approved')
    list_filter = ('name', 'approved',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name', ]


# Registers the category model at the admin backend.
admin.site.register(Category, CategoryAdmin)


# custom filter to Filter By Category name

class CategorieFilter(SimpleListFilter):
    title = 'categories'  # or use _('country') for translated title
    parameter_name = 'categorie'

    def lookups(self, request, model_admin):
        categories = set([article.category for article in Article.objects.all()])
        return [(c.id, c.name) for c in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())
        else:
            return queryset


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'slug', 'author', 'image', 'image_credit',
                    'date_published', 'status')
    list_filter = ('status', 'date_created', 'date_published', 'author', CategorieFilter)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_published'
    ordering = ['status', '-date_created', ]
    readonly_fields = ('views', 'count_words', 'read_time')


# Registers the article model at the admin backend.
admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment', 'article', 'date_created',)
    list_filter = ('date_created', 'name',)
    search_fields = ('name', 'article', 'comment')
    date_hierarchy = 'date_created'
    ordering = ['-date_created', ]
    readonly_fields = ('name', 'email', 'comment', 'article', 'date_created', 'date_updated',)


# Registers the comment model at the admin backend.
admin.site.register(Comment, CommentAdmin)
