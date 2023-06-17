
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('products/', include('product.urls')),
    path('business/', include('business.urls')),
    path('basket/', include('cart.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('training/', include('training.urls')),
    
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Creative Poultry'                    # default: "Django Administration"
admin.site.index_title = 'Creative Poultry'                   # default: "Site administration"
admin.site.site_title = ' Creative Poultry Adminsitration' 


