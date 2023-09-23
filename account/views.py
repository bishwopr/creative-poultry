from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib import messages
from .forms import CustomerRegisterForm,BusinessRegisterForm
from .models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from business.models import BusinessInfo
from cart.models import Cart

class CustomerRegisterView(CreateView):
    form_class = CustomerRegisterForm
    template_name = 'account/register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            Cart.objects.create(user=user)
            messages.success(request, 'Account successfully created.')
            return redirect('account:login')
        return render(request, self.template_name, {'form':form})
    
class BusinessRegisterView(CreateView):
    form_class = BusinessRegisterForm
    template_name = 'account/business_register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_business = True
            user.save()
            BusinessInfo.objects.create(
                    user=user,
                )
            
            
            messages.success(request, "Account requested successfully. You'll be able to login after the verification. It'll not take more than an hour.")
            return redirect('account:login')
        return render(request, self.template_name, {'form':form})
    

class SigninView(LoginView):
    template_name='account/login.html'
    success_message = "You were successfully logged in."

    def form_valid(self, form):
        user = form.get_user()
        employee = User.objects.get(email=user.email)
        if employee.is_superuser :
            auth_login(self.request, form.get_user())
            messages.success(self.request,'Logged in as a superuser.')
            return redirect('/admin/')
        elif employee.is_customer:
            auth_login(self.request, form.get_user())
            messages.success(self.request,'Logged in as {}.'.format(employee.username))
            return redirect('product:home')
        elif employee.is_approved and employee.is_business:
            auth_login(self.request, form.get_user())
            return redirect('business:profile')
        elif  employee.is_business and not employee.is_approved :
            messages.error(self.request, "Account may be under verificaton.")
            return redirect('account:login')
        else:
            messages.error(self.request, "Something went wrong.")

        return HttpResponseRedirect(self.get_success_url())
    

@login_required
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    user.save()
    messages.success(request, 'If you need to activate your account again. Reach out to us.')
    auth_logout(request)
    return redirect('/')
