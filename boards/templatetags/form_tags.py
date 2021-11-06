from django import template

register = template.Library()

# ye input class me field check krta h agr error field password vala nhi h to invalid btayega qki password invalid ka apn ko kya pta
@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
            """
            password me kbhi error return nhi aata so hme bs ye check krna h agr error nhi h to sb valid.
            agr form.errors h to konse field me h agr password field k alava kisi me h tb to invalid qki uska to aata hi nhi
            lekin form me error h apn valid class add krenge password vale ko chhod kr.
            """
        elif field_type(bound_field) != 'PasswordInput': # else if mean else check this part and run if cond, stisfies.
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)

