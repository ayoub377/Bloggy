from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from taggit.models import Tag
from Blog.models import Category, Article


# list articles in Home Page
class ArticleListView(ListView):
    context_object_name = "all_articles"
    paginate_by = 3
    queryset = Article.objects.filter(status=Article.PUBLISHED, deleted=False)
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_articles'] = Article.objects.filter(status=Article.PUBLISHED)[:3]

        return context


# list articles by their category


def Articles_by_category(request, category_slug=None):
    category = Category.objects.all().filter(slug=category_slug).get()
    articles_by_category = Article.objects.filter(category=category)
    paginator = Paginator(articles_by_category, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {'category': category,
                                                  'articles_by_category': articles_by_category,
                                                  'page_obj': page_obj})


# Get a particular article
def getArticleByid(request, pk):
    article = Article.objects.get(pk=pk)
    tags_article = article.tags.all()
    return render(request,'blog/article_detail.html',{'article':article,'tags_article':tags_article})


# search For Article

def post_search(request):
    query = None
    results = []
    query = request.GET.get('search')
    search_vector = SearchVector('title', 'body')
    search_query = SearchQuery(query)
    results = Article.objects.filter(status=Article.PUBLISHED) \
        .annotate(search=search_vector, rank=SearchRank(search_vector, search_query)). \
        filter(search=search_query)
    return render(request, 'blog/search.html',
                  {'query': query,
                   'results': results})


def post_list(request, tag_name=None):
    tag = None
    tag = get_object_or_404(Tag, name=tag_name)
    object_list = Article.objects.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    print(object_list)
    try:
        articles_bytag = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles_bytag = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        articles_bytag = paginator.page(paginator.num_pages)
    return render(request, 'blog/listArticles.html', {'page': page,
                                                      'articles': articles_bytag,
                                                      'tag': tag})
