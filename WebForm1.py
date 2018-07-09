from app import app
from flask import Flask, render_template, request, jsonify,flash, redirect
from wtforms import Form, StringField, SubmitField, SelectField,validators, BooleanField
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import Required, Optional, DataRequired
from dbSetup import db_session
from models import Device, Host
from tables import Results, Water


#This is equivalent to the forms.py file. Linked to the app route default page
class LoginForm(FlaskForm):
    team = SelectField('What team are you apart of?', choices = ((None,''),('ST','ST'),('SI','SI'),('CPM','CPM'),('PPM','PPM'), ('HW','HW'),('HW-UK','HW-UK'), ('SW-PLT','SW-PLT'),('ASW','ASW')
    ,('CT','CT'),('SW-CORE','SW-CORE'),('PI','PI'),('PROJET','PROJET'),('VP ENGINEERING','VP ENGINEERING'),('RFIC','RFIC'),('BBIC','BBIC')),
        validators=[validators.InputRequired('Select a team')])
    #This should have an option for None because host is not always required. If none is
    #picked then the other two should no be able to be selected
    host = SelectField('Host Solution Required', choices = [], validators=[validators.InputRequired('Please select a Board')])
    quantity = StringField('Quantity of Host Solution Required', validators=[validators.InputRequired('Please state the amount of host boards you want in the textbox above')])
    finish = SelectField('Mechanical Finish Required', choices = ((None,''),('Cust','Customer'),('Eng','Engineering')))
    cat = SelectField('Category of the Device', choices = ((None,'None'),('M','M'),('1','1'),('4','4'),('CA','CA')))
    device = SelectField('Device or RF Solution Required', choices = [])
    number = StringField('Quantity of Device Required')

#This is the form for creating a new device and it is linked to the new device route
class DeviceForm(Form):
    cat = SelectField('CAT', choices = (('M','M'), ('1','1'), ('4','4'), ('CA','CA')))
    name = StringField('Name of Device')

#This is the host form for adding new hosts to the database. Linked to the new_host app route
class HostForm(Form):
    name = StringField('Name')
    customer = BooleanField('Customer')
    engineering = BooleanField('Engineering')
    extra = StringField('Extra')


@app.route('/', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    form.device.choices = [(device.id, device.name) for device in Device.query.filter_by(cat=None).all()]
    form.host.choices= [(host.id, host.name) for host in Host.query.all()]
    #if form.validate_on_submit(): To use this I will have to figure out how to validate the choices for device
    if request.method =='POST':
        device = Device.query.filter_by(id=form.device.data).first()
        host = Host.query.filter_by(id= form.host.data).first()
        #This code takes care of changing the format of the ordering link that is put into bugzilla.
        if host.name =='None' and form.cat.data == 'None':
            return '<h1> You did not order anything, please go back and fill out cat or host</h2>'
        elif host.name == 'None':
            return '<h1> ({} x {}) for {}</h1>'.format(form.number.data, device.name, form.team.data)
        elif form.cat.data == 'None':
            return '<h1> ({} x {}-{}) for {}</h1>'.format(form.quantity.data, host.name, form.finish.data, form.team.data)
        else:
            return '<h1> ({} x {}-{}) AND ({} x {}) for {}</h1>'.format(form.quantity.data, host.name, form.finish.data,
                form.number.data, device.name, form.team.data)
    return render_template('form.html', form=form)



#This takes care of the logic behind what happens at the /new_device page
@app.route('/new_device', methods = ['GET', 'POST'])
def new_device():
    """
    Add a new album
    """
    form = DeviceForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        device = Device()
        save_changes(device, form, new=True)
        flash('Album created successfully!')
        return redirect('/')
    return render_template('new_device.html', form=form)

#This takes care of the logic that happens at the new_host page
@app.route('/new_host', methods = ['GET', 'POST'])
def new_host():
    """
    Add a new album
    """
    form = HostForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        host = Host()
        save_host(host, form, new=True)
        flash('Host created successfully!')
        return redirect('/')
    return render_template('new_host.html', form=form)

#This is a helper method that is used in the new host logic.  It's use can be found in "def new_host"
# It essentially saves what was submitted in the Host Form and saves the changes to the database.
def save_host(host, form, new = False):
    host.name = form.name.data
    host.customer = form.customer.data
    host.engineering = form.engineering.data
    host.extra = form.extra.data
    if new:
        db_session.add(host)
    db_session.commit()

#Helper method that is used in the new_device method and it essentially saves the the changes made to the device database
def save_changes(device, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    device.cat = form.cat.data
    device.name = form.name.data
    if new:
        # Add the new album to the database
        db_session.add(device)

    # commit the data to the database
    db_session.commit()

#This has the same principle as the change and edit below.
@app.route('/items/<int:id>', methods=['GET'])
def delete(id):
    h = Host.query.filter_by(id=id).first()
    current_db_sessions = db_session.object_session(h)
    current_db_sessions.delete(h)
    current_db_sessions.commit()
    return redirect('/')

#Same principle as the change and edit. d for device, h for host
@app.route('/it/<int:id>', methods=['GET'])
def remove(id):
    d = Device.query.filter_by(id=id).first()
    current_db_sessions = db_session.object_session(d)
    current_db_sessions.delete(d)
    current_db_sessions.commit()
    return redirect('/')

#This shows the hosts in the database as a table
@app.route('/hosts', methods = ['GET'])
def show_hosts():
    results = []
    qry = db_session.query(Host)
    results = qry.all()
    table = Water(results)
    table.border = True
    return render_template('results.html', table = table, form = 'new_host', item = 'host')


#This shows the table of devices listed in the database
@app.route('/devices', methods = ['GET'])
def show_devices():
    results = []
    qry = db_session.query(Device)
    results = qry.all()
    table = Results(results)
    table.border = True
    return render_template('results.html', table=table, form = 'new_device', item = 'device')

#This is changes the select menu of the device based on what is chosen in the 'CAT' drop down
@app.route('/device/<cat>')
def device(cat):
    devices = Device.query.filter_by(cat=cat).all()

    deviceArray = []

    for device in devices:
        deviceObj= {}
        deviceObj['id'] = device.id
        deviceObj['name'] = device.name
        deviceArray.append(deviceObj)
    #What is this doing?
    return jsonify({'devices':deviceArray})

#This corresponds with the edit in the host table, since it says change and the value in the host table is change
# It corresponds with this method, it was important to make sure the route paths were not the same
@app.route('/ite/<int:id>', methods=['GET', 'POST'])
def change(id):
    qry = db_session.query(Host).filter(
                Host.id==id)
    host = qry.first()

    if host:
        form = HostForm(formdata=request.form, obj=host)
        if request.method == 'POST' and form.validate():
            # save edits
            save_host(host, form)
            flash('host updated successfully!')
            return redirect('/')
        return render_template('edit_host.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)



#This corresponds to the edit in the LinkCol for the Device table
@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Device).filter(
                Device.id==id)
    device = qry.first()

    if device:
        form = DeviceForm(formdata=request.form, obj=device)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(device, form)
            flash('device updated successfully!')
            return redirect('/')
        return render_template('edit_device.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)




if __name__ == "__main__":
    app.run(debug=True)
