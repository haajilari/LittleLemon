from django.urls import path
from . import views

urlpatterns = [
    # path('menu-items', views.MenuItemsView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuiItemView.as_view()),
    path('menu-items/', views.menu_items),
    path('menu-items/<int:pk>', views.single_item)
]