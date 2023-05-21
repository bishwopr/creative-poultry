from django.shortcuts import render,redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, View, DetailView
from .models import Product
from django.contrib import messages
from django.http import HttpResponseRedirect

class HomeView(ListView):
    template_name='product/home.html'
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')
    



class CreateProductView(CreateView):
    model = Product
    fields=['category','name','desc','price','discount','image']
    template_name='product/addproduct.html'

    def get_success_url(self) -> str:
        return redirect('business:profile')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return self.get_success_url()
    
class UpdateProductView(UpdateView):
    model = Product
    fields=['category','name','desc','price','discount','image']
    template_name='product/updateproduct.html'
    success_url = '/business'

    def form_valid(self, form):
      messages.success(self.request, "Product updated successfully!")
      super().form_valid(form)
      return HttpResponseRedirect(self.get_success_url())

    
class DeleteProductView(View):

    def get(self, request, **kwargs):
        pid=self.kwargs['pk']
        Product.objects.get(id=pid).delete()
        messages.success(self.request,'Product removed successfully.')
        return redirect('business:profile')


class ProductCategoryView(ListView):
    template_name='product/product-category.html'
    model = Product

    def get_queryset(self,**kwargs):
        cid=self.kwargs['pk']
        queryset = Product.objects.filter(category = cid)
        return queryset.order_by('-id')

class ProductDetailView(DetailView):
    model= Product
    template_name = 'product/product-detail.html'
    object_name = 'product'

