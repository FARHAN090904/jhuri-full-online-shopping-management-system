from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('<int:product_id>/', ProductDetailView.as_view()),
]
