from django.views.generic import TemplateView
from django.shortcuts import render
from product.models import Product
from .forms import BusinessInfoForm
from .models import BusinessInfo
from django.views.generic.edit import FormView


class ProfileView(TemplateView):
    template_name='business/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        products = Product.objects.filter(creator=self.request.user).order_by('-id')
        info = BusinessInfo.objects.get(user=self.request.user)
        context.update({ "products":products, 'info':info})
        return context

class InformationUpdateView(FormView):
    template_name = 'business/update-information.html'
    form_class = BusinessInfoForm
    success_url = ('/business')

    def get_form(self):
        try:
            info = BusinessInfo.objects.get(user=self.request.user)
            return self.form_class(instance=info, **self.get_form_kwargs())
        except info.DoesNotExist:
            return self.form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(InformationUpdateView, self).form_valid(form)

from order.models import Order
import json
def sales_chart(request):
    products = Product.objects.filter(creator=request.user)
    processed_orders = Order.objects.filter(
        orderitem__product__in=products,
        status='Processed'
    ).distinct()
    labels = [order.created_at.strftime('%Y-%m-%d') for order in processed_orders]
    sales_data = [float(order.total_price) for order in processed_orders]
    print(labels)
    print(sales_data)

    context = {
        'labels': json.dumps(labels),
        'sales_data': json.dumps(sales_data),
    }

    return render(request, 'business/sales_chart.html', context)