from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, View, DetailView
from .models import Product, ProductRating
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
    fields=['category','name','desc','price','discount','image','stock_quantity']
    template_name='product/addproduct.html'

    def get_success_url(self) -> str:
        return redirect('business:profile')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return self.get_success_url()
    
class UpdateProductView(UpdateView):
    model = Product
    fields=['category','name','desc','price','discount','image','stock_quantity']
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


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def products(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price':
        products = products.order_by('price')
    # Add more sorting options as needed
    
    context = {
        'products': products,
        'selected_category': category,
        'sort_by': sort_by,
    }
    return render(request, 'product/products.html', context)


def product_rating(request):
    if request.method == 'POST':
        user = request.user
        rating = request.POST.get('rate')
        review = request.POST.get('review')
        pid = request.POST.get('pid')
       
        product = get_object_or_404(Product, id=pid)
        ProductRating.objects.create(user=user, product=product, rating=rating, review=review)
        messages.success(request, "Thank you for giving your feedback.")
        return HttpResponseRedirect(product.get_absolute_url())
    
    messages.success(request, "Something went wrong.")
    return HttpResponseRedirect(request.path_info)








