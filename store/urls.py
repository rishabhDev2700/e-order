from django.urls import path

from store import views

urlpatterns = [
    path('', views.show_all_items, name='show_all_items'),
    path('category/<slug:slug>', views.show_by_category, name='show_by_category'),
    path('<slug:slug>', views.item_details, name='item_details'),
]
