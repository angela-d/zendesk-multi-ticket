#!/usr/bin/env python3
# pylint: disable=R0914
# pylint: disable=E1101
# pylint: disable=E1135
# pylint: disable=C0103
'''
Zendesk form
'''
import json
import requests
from bottle import route, get, redirect, template, run, static_file, request, response

# api config
headers = {'content-type': 'application/json'}
user = 'myagent@example.com/token'
api_token = '2zFD893XpPWQFhj235FyHV5WpNGpTcdDFKk65n'
url = 'https://example.zendesk.com/api/v2/requests.json'

# agent id
phone_agent = '001'
tech_trainer = '002'
admin_agent = '003'
email_agent = '004'
computer_agent = '005'

# nothing further to config

# redirect / to create ticket page; :80 does this via nginx
@route('/')
def redirect_to_form():
    ''' Redirect to landing page '''
    return redirect('/create_ticket')

# generate a form using the bottle framework
@route('/create_ticket', method=['GET', 'POST'])
def handle_form():
    ''' Process the form and hand the data off to Zendesk. '''
    # check if the user is already logged in to zendesk
    if 'verified_email' in request.cookies:
        ask_email = False
    else:
        ask_email = True

    # if a recent form hasn't been submitted, ask for an email
    if 'verified_email' in request.cookies:
        email = request.get_cookie('verified_email')
    else:
        email = request.forms.get('email')

    # initialize the status var
    status = ''

    # get form data
    if request.POST:
        # we build the subject off the date starting #
        subject_phone = 'PHONE - New Employee Starting ' + request.forms.get('date_starting')
        subject_email = 'EMAIL - New Employee Starting ' + request.forms.get('date_starting')
        subject_computer = 'COMPUTER - New Employee Starting ' + request.forms.get('date_starting')
        subject_admin = 'ADMIN SYSTEMS - New Employee Starting ' + request.forms.get('date_starting')
        subject_training = 'TECH TRAINING - Requested for ' + request.forms.get('tech_training')
        date_starting = request.forms.get('date_starting')
        employee_name = request.forms.get('employee_name')
        employee_username = employee_name.replace(" ", "").lower()
        voicemail = request.forms.get('voicemail')
        position_type = request.forms.get('position_type')
        phoneext = request.forms.get('phoneext')
        predecessoremail = request.forms.get('predecessoremail')
        fwdaliases = request.forms.get('fwdaliases')
        publish_email = request.forms.get('publish_email')
        admin_calendars = request.forms.get('admin_calendars')
        existing_machine = request.forms.get('existing_machine')
        os = request.forms.get('os')
        transfer_files = request.forms.get('transfer_files')
        access_type = request.forms.get('access_type')
        vpn = request.forms.get('vpn')
        tech_training = request.forms.get('tech_training')

        # previous extension can be blank
        if request.forms.get('prevext') is None:
            prevext = "-"
        else:
            prevext = request.forms.get('prevext')

        room = request.forms.get('room')

        # make system access a global, so we can append to it later
        global system_access
        system_access = ''

        if request.forms.get('folder') is not None:
            folder = "\n  - Dept network share"
        else:
            folder = ''

        if request.forms.get('specialapp1') is not None:
            specialapp1 = "\n  - Special app 1"
        else:
            specialapp1 = ''

        if request.forms.get('specialapp2') is not None:
            specialapp2 += "\n  - Special app 2"
        else:
            specialapp2 = ''

        system_access = folder + specialapp1 + specialapp2


        # reassign vpn option if supervisor doesn't approve, but retain system access var
        if vpn == 'No':
            vpn_option = 'NO'
        else:
            vpn_option = 'Yes'

        # description can be blank
        if request.forms.get('description') is None:
            description = "-"
        else:
            description = request.forms.get('description')

        # break it into readable lines so pylint doesn't complain
        details_phone = \
            'Supervisor: ' + email + "\n" \
            'Date Starting: ' + date_starting + "\n" \
            'Employee Name: ' + employee_name + "\n" \
            'Username: ' + employee_username + "\n" \
            'Access to Predecessor Voicemail: ' + voicemail + "\n" \
            'New Extension or Reuse?: ' + phoneext + "\n" \
            'Predecessor Extension (if any): ' + prevext + "\n" \
            'Office Location: ' + room + "\n" \
            'Additional Info: ' + description

        details_email = \
            'Supervisor: ' + email + "\n" \
            'Date Starting: ' + date_starting + "\n" \
            'Employee Name: ' + employee_name + "\n" \
            'Username: ' + employee_username + "\n" \
            'Access to Predecessor Email: ' + predecessoremail + "\n" \
            'FWD Predecessors Aliases?: ' + fwdaliases + "\n" \
            'Publish Email to Directory?: ' + publish_email + "\n" \
            'Admin any Calendars?: ' + admin_calendars + "\n" \
            'Additional Info: ' + description

        details_computer = \
            'Supervisor: ' + email + "\n" \
            'Date Starting: ' + date_starting + "\n" \
            'Employee Name: ' + employee_name + "\n" \
            'Username: ' + employee_username + "\n" \
            'Existing Machine?: ' + existing_machine + "\n" \
            'OS: ' + os + "\n" \
            'Transfer Predecessor Files: ' + transfer_files + "\n" \
            'Office Location: ' + room + "\n" \
            'Additional Info: ' + description

        details_admin = \
            'Supervisor: ' + email + "\n" \
            'Date Starting: ' + date_starting + "\n" \
            'Employee Name: ' + employee_name + "\n" \
            'Username: ' + employee_username + "\n" \
            'Position Type: ' + position_type + "\n" \
            'System Access Requested: ' + system_access + "\n" \
            'VPN: ' + vpn_option + "\n" \
            'Additional Info: ' + description

        details_training = \
            'Requested Technology Training Date: ' + tech_training + "\n\n" \
            '-- This is an overview of tickets already created for phone, email, computer and admin systems --:' + "\n" \
            'Supervisor: ' + email + "\n" \
            'Date Starting: ' + date_starting + "\n" \
            'Employee Name: ' + employee_name + "\n" \
            'Username: ' + employee_username + "\n" \
            'Position Type: ' + position_type + "\n" \
            'Access to Predecessor Email: ' + predecessoremail + "\n" \
            'FWD Predecessors Aliases?: ' + fwdaliases + "\n" \
            'Publish Email to Directory?: ' + publish_email + "\n" \
            'Admin any Calendars?: ' + admin_calendars + "\n" \
            'Access to Predecessor Voicemail: ' + voicemail + "\n" \
            'New Extension or Reuse?: ' + phoneext + "\n" \
            'Predecessor Extension (if any): ' + prevext + "\n" \
            'Existing Machine?: ' + existing_machine + "\n" \
            'OS: ' + os + "\n" \
            'Transfer Predecessor Files: ' + transfer_files + "\n" \
            'System Access Requested: ' + system_access + "\n" \
            'VPN: ' + vpn_option + "\n" \
            'Office location: ' + room + "\n" \
            'Additional Info: ' + description

        # collect the form data and json it for the api
        data_phone = {'request': {'assignee_id': phone_agent, 'collaborators': [tech_trainer],'subject': subject_phone, 'requester': {'locale_id': 8, 'name': email, 'email': email}, 'comment': {'body': details_phone}}}
        ticket_phone = json.dumps(data_phone)

        # Make the API request
        api = requests.post(
            url,
            data=ticket_phone,
            auth=(user, api_token),
            headers=headers
        )
        if api.status_code != 201:
            if api.status_code == 401 or 422:
                status = 'Error: Please make sure you use your company email to submit tickets.'
                ask_email = True
            else:
                status = 'Error ' + str(api.status_code)
        else:
            status = 'Your tickets have been submitted; a copy was sent to you.'
            if 'verified_email' not in request.cookies:
                response.set_cookie('verified_email', email, max_age=364*24*3600)
                ask_email = False

        # after the phone ticket passes, we'll get onto others
        # start the email ticket, now
        data_email = {'assignee_id': int(email_agent), 'collaborators': [tech_trainer], 'request': {'subject': subject_email, 'requester': {'locale_id': 8, 'name': email, 'email': email}, 'comment': {'body': details_email}}}
        ticket_email = json.dumps(data_email)

        # Make the API request
        api = requests.post(
            url,
            data=ticket_email,
            auth=(user, api_token),
            headers=headers
        )

        # start the computer
        data_computer = {'request': {'assignee_id': int(computer_agent), 'collaborators': [tech_trainer], 'subject': subject_computer, 'requester': {'locale_id': 8, 'name': email, 'email': email}, 'comment': {'body': details_computer}}}
        ticket_computer = json.dumps(data_computer)

        # Make the API request
        api = requests.post(
            url,
            data=ticket_computer,
            auth=(user, api_token),
            headers=headers
        )

        # start the computer
        data_admin = {'request': {'assignee_id': int(admin_agent), 'collaborators': [tech_trainer], 'subject': subject_admin, 'requester': {'locale_id': 8, 'name': email, 'email': email}, 'comment': {'body': details_admin}}}
        ticket_admin = json.dumps(data_admin)

        # Make the API request
        api = requests.post(
            url,
            data=ticket_admin,
            auth=(user, api_token),
            headers=headers
        )

        # start the tech training
        data_training = {'request': {'assignee_id': int(tech_trainer), 'subject': subject_training, 'requester': {'locale_id': 8, 'name': email, 'email': email}, 'comment': {'body': details_training}}}
        ticket_training = json.dumps(data_training)

        # Make the API request
        api = requests.post(
            url,
            data=ticket_training,
            auth=(user, api_token),
            headers=headers
        )

    return template('ticket_form', feedback=status, no_email=ask_email)

@route('/inc/<filename>')
def send_css(filename):
    ''' <filename> is a wildcard, so it'll pull everything - css, images, etc.'''
    return static_file(filename, root='static/inc')

# run paste server instead of default
run(server='paste', host='localhost', port=8081, debug=True)
