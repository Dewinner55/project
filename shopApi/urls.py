from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from category.views import CategoryViewSet
from product.views import ProductViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/orders/', include('order.urls')),
    path('api/v1/', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
