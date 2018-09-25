from django.urls import path

from .views import AccentDetailView, AccentListView, PlayDetailView, PlayListView


urlpatterns = [
    path('plays/', PlayListView.as_view(), name='play-list'),
    path('plays/<int:play_id>/', PlayDetailView.as_view(), name='play-detail'),
    path('plays/<int:play_id>/accents/', AccentListView.as_view(), name='accent-list'),
    path('plays/<int:play_id>/accents/<int:accent_id>', AccentDetailView.as_view(), name='accent-detail'),
]
