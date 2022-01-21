from django.urls import path

from Blog import views

app_name = 'Blog'
urlpatterns = \
    [
        path('home', views.ArticleListView.as_view(), name='home'),
        path('category/<slug:category_slug>', views.Articles_by_category, name='get_category'),
        path('article/<int:pk>', views.getArticleByid, name='get_article_detail_by_number'),
        path('search', views.post_search, name='search_for_articles'),
        path('list_byTag/<str:tag_name>', views.post_list, name='listTag')

    ]
