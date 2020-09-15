from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # Домашняя страница. Вывод всех публичных постов.
    url(r'^$', views.public_posts,
        name='index'),

    # Страница для добавления нового поста
    url(r'^new_post/$', views.new_post,
        name='new_post'),

    # Страница для редактирования записи
    url(r'^edit_post/(?P<post_id>\d+)/$', views.edit_post,
        name='edit_post'),

    # Удаление поста
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post,
        name='delete_post'),

    # Страница с личными публикациями
    url(r'^owner_posts/$', views.owner_posts,
        name='owner_posts'),

    # Страница для отельного поста
    url(r'^post_details/(?P<post_id>\d+)/$', views.post_details,
        name='post_details'),

    # Публикация/приватизация поста
    url(r'^privat_public/(?P<post_id>\d+)/$', views.privat_public,
        name='privat_public'),

    # Страница для добавления нового tag
    url(r'^new_tag/$', views.new_tag,
        name='new_tag'),

    # Введет все посты, прикрепленные к этому тегу
    url(r'^tag_detail/(?P<tag_id>\d+)/$', views.tag_detail, name='tag_detail'),

    # Удаление поста
    url(r'^delete_tag/(?P<tag_id>\d+)/$', views.delete_tag,
        name='delete_tag'),

]
app_name = 'blogs'
