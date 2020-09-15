from .models import Tag


def tags(request):
    """Выводит список тегов"""
    tags = Tag.objects.all()

    return {'tags': tags}
