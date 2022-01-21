from taggit.models import Tag

from Blog.models import Category, Article


def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def get_tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}
