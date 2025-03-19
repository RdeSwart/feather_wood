from django import template


register = template.Library()


# @register.filter(name='calc_subtotal')
# def calc_subtotal(rrp_price, quantity):
#     return rrp_price * quantity

@register.filter(name='calc_subtotal')
def calc_subtotal(rrp_price, quantity):
    try:
        if rrp_price is None:
            return 0  # Handle missing price
        rrp_price = float(rrp_price)  # Ensure it's a valid number
        quantity = int(quantity)  # Ensure it's a valid integer
        return rrp_price * quantity
    except (ValueError, TypeError):
        return 0  # Return 0 if there's an error with price or quantity
