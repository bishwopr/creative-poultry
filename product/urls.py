from django.urls import path
from .views import HomeView, CreateProductView, UpdateProductView, DeleteProductView, ProductCategoryView, ProductDetailView
app_name ='product'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('add-product',CreateProductView.as_view(),name='addproduct'),
    path('<pk>/update-product',UpdateProductView.as_view(),name='updateproduct'),
    path('<pk>/delete-product',DeleteProductView.as_view(),name='deleteproduct'),
    path('<pk>/category',ProductCategoryView.as_view(),name='category'),
    path('<pk>/detail',ProductDetailView.as_view(),name='detail'),
]