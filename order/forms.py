from django import forms

class ShippingForm(forms.Form):
    PAYMENT_CHOICES =(
    ("Cash on Delivery", "Cash on Delivery"),
    ("Credit Card", "Credit Card"),
)
    payment_method = forms.ChoiceField(choices = PAYMENT_CHOICES)
    address = forms.CharField(label="Shipping Address", max_length=255)
    phone = forms.CharField(label="Phone Number", max_length=20)


class PromoCodeForm(forms.Form):
    code = forms.CharField(max_length=20)
