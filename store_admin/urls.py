from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('categories/', views.all_categories, name='all_categories'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/update/<slug:slug>', views.category_update, name='category_update'),
    path('category/delete/', views.category_delete, name='category_delete'),
    path('items/', views.all_items, name='all_items'),
    path('item/add/', views.item_add, name='item_add'),
    path('item/update/', views.item_update, name='item_update'),
    path('item/delete/', views.item_delete, name='item_delete'),
    path('orders/', views.view_orders, name='view_orders'),
]
