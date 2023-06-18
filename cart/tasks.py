from datetime import timedelta
from shoes_shop_api.celery import app
from django.utils import timezone

@app.task
def clear_expired_carts():
    thresh_hold = timedelta(hours=3)

    from shoes.models import QtySize
    from .models import Cart

    print('start')
    carts = Cart.objects.filter(last_modified__lt=timezone.now() - thresh_hold)
    for cart in carts:
        for item in cart.cartitem_set.all():
            shoe = item.shoe
            sizes = QtySize.objects.filter(shoe=shoe, size=item.user_size)[0]
            sizes.qty += item.user_qty
            sizes.save()
            shoe.save()
            item.delete()

        cart.save()

    print('end')