#!/usr/bin/python

'''

CIDRTOOLS ver 1.0

 Web app to help with working with IP subnets
 Based on Flask web application framework

 Github: https://github.com/ja3600/cidrtools

'''

from secrets import token_urlsafe
from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, IntegerField, TextAreaField, validators
from flask_table import Table, Col

from .ipip import *

# App config.

# auto generate random key
SECRET_KEY = token_urlsafe(32)

# SECRET_KEY = 'm3wFUMcLUlsja33_pV-mkU4Uc2T8cxv3vuFJI3N52Ro'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# Global variables

#default subnet
working_ipv4 = "192.168.10.0"
working_prefixlen = 24

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
        validators=[validators.required()])

class SummaryForm(Form):
    ip_list = TextAreaField('ip_list', render_kw={'class': 'form-control', 'rows': '55'},
        validators=[validators.required()])


# Main Application Starts Here

@app.route('/')
@app.route('/index')
def index():
    name = 'Subnet Table'
    return render_template('index.html', title='Subnet Table')
    

@app.route("/disector", methods=['GET', 'POST'])
def disect_tool():
    form = BaseForm(request.form)
    results = []
    table_results = []

    # must use the global keyword for these global variable
    global working_ipv4
    global working_prefixlen

    print (form.errors)

    if request.method == 'POST':
        ipv4 = request.form['ipv4']
        prefixlen = request.form['prefixlen']

        if form.validate():
        # Save the comment here.
            cidr = ipv4 + '/' + str(prefixlen)

            flash('Results for ' + cidr)

            results = ip_disector(cidr)

            # Create a table from the returned dictionary of items
            table_results = TwoColTable(results)
            #print(table_results.__html__())

            #save the working address and prefix
            working_ipv4 = ipv4
            working_prefixlen = prefixlen

        else:
            flash('Error: Invalid input!')

    return render_template('base_form.html',
                            form=form,
                            results=table_results,
                            working_ipv4=working_ipv4,
                            working_prefixlen=working_prefixlen,
                            form_title='Disector')


@app.route("/subnet", methods=['GET', 'POST'])
def subnet_tool():
    form = SubnetForm(request.form)
    results = []
    table_results = []

    # must use the global keyword for these global variable
    global working_ipv4
    global working_prefixlen

    print (form.errors)

    if request.method == 'POST':
        ipv4 = request.form['ipv4']
        parentcidr = request.form['prefixlen']
        childcidr = request.form['new_prefixlen']

        if form.validate():
        # Save the comment here.
            cidr = ipv4 + '/' + str(parentcidr)

            results = ip_subnet(cidr, int(childcidr), "no csv text")

            # Create a table from the returned dictionary of items
            table_results = SubnetTable(results)
            #print(table_results.__html__())

            flash('All the /' + childcidr + ' children subnets within parent network ' + cidr + ' (records=' + str(len(results)) + ')')

            #save the working address and prefix
            working_ipv4 = ipv4
            working_prefixlen = parentcidr

        else:
            flash('Error: Invalid input!')

    return render_template('base_form.html',
                            form=form,
                            results=table_results,
                            working_ipv4=working_ipv4,
                            working_prefixlen=working_prefixlen,
                            form_title='Subnets')


@app.route("/subnet-csv", methods=['GET', 'POST'])
def subnet_csv_tool():
    form = SubnetFormCSV(request.form)
    results = []
    table_results = []

    # must use the global keyword for these global variable
    global working_ipv4
    global working_prefixlen

    print (form.errors)

    if request.method == 'POST':
        ipv4 = request.form['ipv4']
        parentcidr = request.form['prefixlen']
        childcidr = request.form['new_prefixlen']
        netbox_text = request.form['netbox_text']

        if form.validate():
        # Save the comment here.
            cidr = ipv4 + '/' + str(parentcidr)

            results = ip_subnet(cidr, int(childcidr), netbox_text)

            # Create a table from the returned dictionary of items
            table_results = SubnetTableCSV(results)
            #print(table_results.__html__())
            
            flash('All the /' + childcidr + ' children subnets within parent network ' + cidr + ' (records=' + str(len(results)) + ')')
            
            #save the working address and prefix
            working_ipv4 = ipv4
            working_prefixlen = parentcidr

        else:
            flash('Error: Invalid input!')

    return render_template('base_form.html',
                            form=form,
                            results=table_results,
                            working_ipv4=working_ipv4,
                            working_prefixlen=working_prefixlen,
                            form_title='Subnets-csv')


@app.route("/supernet", methods=['GET', 'POST'])
def supernet_tool():
    form = BaseForm(request.form)
    results = []
    table_results = []

    # must use the global keyword for these global variable
    global working_ipv4
    global working_prefixlen

    print (form.errors)

    if request.method == 'POST':
        ipv4 = request.form['ipv4']
        prefixlen = request.form['prefixlen']

        if form.validate():
        # Save the comment here.
            cidr = ipv4 + '/' + str(prefixlen)

            flash('The available (or upto 8) supernets for ' + cidr)

            results = ip_supernet(cidr)

            # Create a table from the returned dictionary of items
            table_results = TwoColTable(results)
            #print(table_results.__html__())

            #save the working address and prefix
            working_ipv4 = ipv4
            working_prefixlen = prefixlen

        else:
            flash('Error: Invalid input!')

    return render_template('base_form.html',
                            form=form,
                            results=table_results,
                            working_ipv4=working_ipv4,
                            working_prefixlen=working_prefixlen,
                            form_title='Supernets')


@app.route("/summary", methods=['GET', 'POST'])
def summary_tool():
    form = SummaryForm(request.form)
    results = []
    table_results = []

    print (form.errors)

    if request.method == 'POST':
        ip_list = request.form['ip_list']
        # print("LIST:", ip_list.split('\r\n'))


        if form.validate():
        # Save the comment here.

            flash('Summarization Results.')

            results = ip_summary(ip_list)

            print(results)
            # Create a table from the returned dictionary of items
            table_results = TwoColTable(results)
            # print(table_results.__html__())

        else:
            flash('Error: Invalid input!')

    return render_template('summary_form.html',
                            form=form,
                            results=table_results,
                            form_title='Summarization')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)