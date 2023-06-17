from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect
from product.models import Product
from django.http import HttpResponseRedirect

class ProfileView(TemplateView):
    template_name='business/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        products = Product.objects.filter(creator=self.request.user).order_by('-id')
        context.update({ "products":products})
        return context


