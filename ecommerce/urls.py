from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('storeapp.urls')),
    path('user/', include('UserProfile.urls', namespace='UserProfile')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('orders/', include('order.urls', namespace='order')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
