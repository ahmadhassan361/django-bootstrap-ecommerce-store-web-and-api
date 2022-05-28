from django import template
register = template.Library()

@register.simple_tag()
def discount(price, discount, *args, **kwargs):
    # you would need to do any localization of the result here
    return price - (price * discount / 100)

@register.simple_tag()
def item_total(price, discount,quantity, *args, **kwargs):
    # you would need to do any localization of the result here
    return quantity * (price - (price * discount / 100))
# register.filter('discount', discount)