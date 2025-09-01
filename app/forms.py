from wtforms import Form, StringField, IntegerField, TextAreaField, validators
from flask_table2 import Table, Col

# Declare classes, tables/forms

class TwoColTable(Table):
    name = Col('item')
    value = Col('value')
    classes = ['table', 'table-sm']

class SubnetTable(Table):
    subid = Col('#')
    network = Col('network')
    netmask = Col('netmask')
    first_ip = Col('first IP')
    last_ip = Col('last IP')
    classes = ['table', 'table-sm']

class SubnetTableCSV(Table):
    netbox = Col('netbox import')
    classes = ['table', 'table-sm']

class BaseForm(Form):
    ipv4 = StringField('ipv4',
        validators=[validators.IPAddress(ipv4=True, ipv6=False, message='That is a strange IPv4 address.')])

    prefixlen = IntegerField('prefixlen',
        validators=[validators.NumberRange(min=2, max=32, message='Valid prefix range 2 - 32!')])

class SubnetForm(Form):
    ipv4 = StringField('ipv4',
        validators=[validators.IPAddress(ipv4=True, ipv6=False, message='That is a strange IPv4 address.')])

    prefixlen = IntegerField('prefixlen',
        validators=[validators.NumberRange(min=16, max=30, message='Valid prefix range 16 - 30!')])

    new_prefixlen = IntegerField('prefixlen',
        validators=[validators.NumberRange(min=17, max=32, message='Valid child subnet range is 17 - 32!')])

class SubnetFormCSV(Form):
    ipv4 = StringField('ipv4',
        validators=[validators.IPAddress(ipv4=True, ipv6=False, message='That is a strange IPv4 address.')])

    prefixlen = IntegerField('prefixlen',
        validators=[validators.NumberRange(min=16, max=30, message='Valid prefix range 16 - 30!')])

    new_prefixlen = IntegerField('prefixlen',
        validators=[validators.NumberRange(min=17, max=32, message='Valid child subnet range is 17 - 32!')])

    netbox_text = TextAreaField('netbox_text', render_kw={'class': 'form-control', 'rows': '55'},
        validators=[validators.data_required()])

class SummaryForm(Form):
    ip_list = TextAreaField('ip_list', render_kw={'class': 'form-control', 'rows': '55'},
        validators=[validators.data_required()])
