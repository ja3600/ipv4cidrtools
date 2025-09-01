from flask import Blueprint, render_template, flash, request
from .forms import BaseForm, SubnetForm, SubnetFormCSV, SummaryForm, TwoColTable, SubnetTable, SubnetTableCSV
from .ipip import ip_disector, ip_subnet, ip_supernet, ip_summary


# Global variables

#default subnet
working_ipv4 = "192.168.10.0"
working_prefixlen = 24

main = Blueprint('main', __name__)


# Main Application Starts Here

@main.route('/')
@main.route('/index')
def index():
    name = 'Subnet Table'
    return render_template('index.html', title='Subnet Table')
    

@main.route("/disector", methods=['GET', 'POST'])
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


@main.route("/subnet", methods=['GET', 'POST'])
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


@main.route("/subnet-csv", methods=['GET', 'POST'])
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


@main.route("/supernet", methods=['GET', 'POST'])
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


@main.route("/summary", methods=['GET', 'POST'])
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
