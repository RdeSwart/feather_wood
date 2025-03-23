from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(rrp_price, quantity):
    try:
        if rrp_price is None:
            return 0
        rrp_price = float(rrp_price) 
        quantity = int(quantity) 
        return rrp_price * quantity
    except (ValueError, TypeError):
        return 0
