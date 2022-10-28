from django import template

register = template.Library()


@register.filter
def replace_comm(val, arg):
	if type(val) != str or ',' not in val:
		return val
	elif ',' in val:
		return val.replace(',', f' {arg} ')


@register.filter
def num_format(val):
	return '{:,}'.format(val).replace(',', ' ')
