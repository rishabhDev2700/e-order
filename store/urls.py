from django.urls import path

from store import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name="home"),
    path('all/', views.show_all_items, name='show_all_items'),
    path('categories/', views.show_all_categories, name='show_all_categories'),
    path('category/<slug:slug>', views.show_by_category, name='show_by_category'),
    path('<slug:slug>', views.item_details, name='item_details'),
]
