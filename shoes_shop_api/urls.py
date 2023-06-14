"""
URL configuration for shoes_shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import UserViewSet, EmailVerificationView, EmailResendView, EmailPasswordResetView, \
    PasswordResetView
from cart.views import CartViewSet, CartItemAddView, CardItemRemoveView
from shoes.views import ShoeViewSet, BrandViewSet, HotDealsView, CarouselView

router = SimpleRouter()

router.register(r'shoe', ShoeViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'hotdeals', HotDealsView)
router.register(r'carousel', CarouselView)
router.register(r'accounts', UserViewSet, basename='accounts')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('__debug__/', include('debug_toolbar.urls')),
                  path('accounts/verify/<int:user_id>/<str:token>/', EmailVerificationView.as_view(),
                       name='verify_email'),
                  path('accounts/reset/<int:user_id>/<str:token>/', PasswordResetView.as_view(), name='reset_password'),
                  path('accounts/resend', EmailResendView.as_view(), name='resend_email'),
                  path('accounts/reset/send_email', EmailPasswordResetView.as_view(), name='reset_email'),
                  path('cart/add_item', CartItemAddView.as_view(), name='add_item'),
                  path('cart/remove_item', CardItemRemoveView.as_view(), name='remove_item'),
              ] + static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
