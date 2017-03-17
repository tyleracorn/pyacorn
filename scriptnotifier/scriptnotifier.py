#!/usr/bin/env python
# -*- coding: utf-8 -*
# public
'''scriptnotifier.py: Contains a status alert class for scripts'''
from __future__ import absolute_import, division, print_function
__author__ = 'Tyler Acorn'
__date__ = '2017'
__version__ = '1.000'


class ScriptNotifier:
    """
    Notify the user of the status of your script. If error occurred, print error message.
    Can send email or text messages with script status or error if the correct dictionaries
    are initialized

    Parameters:
        print_error (bool): print error to the current console
        email (bool): send status alerts or crash reports to email. Requires SMTP_Dict
        text (bool): send a text message to your phone using twilio account. Requires TWILIO_Dict
        SMTP_Dict (dict): A dictionary with the smtp settings required for sending an email
            from python
        TWILIO_Dict (dict): A dictionary with your TWILIO account information needed to send
            text messages to yourself using TWILIO

    Examples:
        an example of the dictionaries needed and initializing the notifier class

        >>> smtp_dict = {'from_addr': 'myless_secure_email@gmail.com',
        ...              'to_addr': 'my_email@gmail.com',
        ...              'login': 'myless_secure_email@gmail.com',
        ...              'password': 'Secr@tPa22word',
        ...              'smtpserver': 'smtp.gmail.com',
        ...              'SSL': True}
        ...
        ... twilio_dict = {'accountSID': '34characterSID',
        ...                'authToken': '32characterTOKEN',
        ...                'myNumber': '+17809995555',
        ...                'twilioNumber': '+15873334444',
        ...                'length_limit': 310}
        ...
        ... notifier = gs.ScriptNotifier(print_error=True, email=True, text=True
        ...                              SMTP_Dict=smtp_dict, TWILIO_Dict=twilio_dict)

        once the class is initialized, then crash reports can be sent to all initialized
        outputs (print_error, email, text)

        >>> if 'ERROR' in message:
        ...     notifier.crash_report(message)

        or status updates can be embedded at points in your script and they will be sent
        to all initialized outputs (print_error, email, text)

        >>> for idx in range(2000):
        ...     something = idx + something_else
        ... notifier.status_alert('finished first loop!')

        or send just an email

        >>> notifier.email_myself('finished first model', 'UPDATE')

        or send just a text

        >>> notifier.text_myself('finished 5th model', status='UPDATE')

    Note:
        GMAIL: in order to send emails with a gmail account you have to switch the
        security settings to allow access from less secure apps
    Note:
        TWILIO: you can sign up for a trial account with twilio for free. The trial account
        provides a free credit to send text messages with. You have to initialize a phonenumber
        to send them from and you lose this number when you don't send any texts for 30 days.
        It seems like if that happens though you can just initialize a new number.
    Note:
        Install TWILIO: pip install twilio

    .. codeauthor:: Tyler Acorn - February 20, 2017
    """

    def __init__(self, print_error=True, email=False, text=False, SMTP_Dict=None,
                 TWILIO_Dict=None):
        # Initialize whether you want to print to console `print_error`, email, or
        # send text messages

        self.print_error = print_error
        self.email = email
        self.text = text

        if self.email:
            # Check for required keys in the SMTP dictionary if sending an email
            requ_email_keys = ('from_addr', 'to_addr', 'login', 'password', 'smtpserver',
                               'SSL')
            if all(requ_email_keys for keys in SMTP_Dict):
                self.email_dict = SMTP_Dict
            else:
                raise KeyError('Required email server keys not found in SMTP_Dict\n', SMTP_Dict)

            # test the connection to the email server
            self.connect_email_server()
            self.email_server.close()

        if self.text:
            # Check for required keys in the TWILIO dictionary if sending a text
            requ_text_keys = ('accountSID', 'authToken', 'myNumber', 'twilioNumber', 'length_limit')
            if all(requ_text_keys for keys in TWILIO_Dict):
                self.text_dict = TWILIO_Dict
            else:
                raise KeyError('Required text server keys not found in TWILIO_Dict\n', TWILIO_Dict)

            # test the connection to the TWILIO Server
            self.connect_twilio()

    def connect_email_server(self):
        """
        setup up the email server

        .. codeauthor:: Tyler Acorn - February 20, 2017
        """
        import smtplib

        if self.email_dict['SSL'] is True:
            # Connect to a secure SMTP_SSL Server
            try:
                if 'port' in self.email_dict:
                    # use supplied port
                    self.email_server = smtplib.SMTP_SSL(self.email_dict['smtpserver'],
                                                         self.email_dict['port'])
                else:
                    # use default ports
                    self.email_server = smtplib.SMTP_SSL(self.email_dict['smtpserver'])
                self.email_server.ehlo()
                self.email_server.login(self.email_dict['login'], self.email_dict['password'])
            except:
                raise Exception('Unable to connect to email server. Check SMTP_Dict')
        else:
            # Connect to an insecure SMTP Server
            try:
                if 'port' in self.email_dict:
                    # use supplied port
                    self.email_server = smtplib.SMTP(self.email_dict['smtpserver'],
                                                     self.email_dict['port'])
                else:
                    # use default ports
                    self.email_server = smtplib.SMTP(self.email_dict['smtpserver'])
                self.email_server.ehlo()
            except:
                raise Exception('Unable to connect to email server. Check SMTP_Dict')

    def connect_twilio(self):
        """
        connect to the twilio client with the accountSID and authToken

        .. codeauthor:: Tyler Acorn - February 20, 2017
        """
        try:
            from twilio.rest import TwilioRestClient
        except:
            raise ImportError("can't find twilio module. Install using 'pip install twilio'")
        # Connect to twilio client
        self.twilio_client = TwilioRestClient(self.text_dict['accountSID'],
                                              self.text_dict['authToken'])

    def crash_report(self, errormsg):
        """
        Send an error message that the script crashed and initiate a sys.exit(). Will use whatever
        communications methods set during initialization of the class (console, text, email)

        Parameters:
            errormsg (str): the message you want sent to yourself.

        .. codeauthor:: Tyler Acorn - February 20, 2017
        """

        import sys
        # Print Error message
        if self.print_error:
            print('\nERROR: the script has crashed!')
            print('Error Message:', errormsg, '\n')
        # email Error message
        if self.email:
            self.email_myself(errormsg, 'ERROR')
        # send text message
        if self.text:
            self.text_myself(errormsg, status='ERROR: ')
        # exit process
        sys.exit(1)

    def status_alert(self, message, status='Update'):
        """
        Send yourself an update of your script status. Will use whatever communication
        method(s) set during initialization of the class (console, text, email)

        Parameters:
            message (str): the message you want sent to yourself.
            status (str): if included will be appended to the start of the text
                for example 'Update'

        .. codeauthor:: Tyler Acorn - February 20, 2017
        """

        if self.print_error:
            print(status + ': ' + message)
        if self.email:
            self.email_myself(message, status)
        if self.text:
            self.text_myself(message, status=(status + ':'))

    def email_myself(self, message, status):
        """
        send an email to yourself from python with the status of your script

        Parameters:
            message (str): the message that you want to email yourself
            status (str): the status will be included in the subject of the email.
                for example 'ERROR' will provide the subject line 'ScriptNotifier: ERROR'

        .. codeauthor:: Tyler Acorn - February 20, 2017
        """
        subject = 'ScriptNotifier: ' + str(status)

        email_string = 'From: %s\n'\
                       'To: %s\n'\
                       'Subject: %s\n'\
                       '\n'\
                       '%s' % (self.email_dict['from_addr'], self.email_dict['to_addr'],
                               subject, message)

        try:
            self.connect_email_server()
            self.email_server.sendmail(self.email_dict['from_addr'], self.email_dict['to_addr'],
                                       email_string)
            self.email_server.close()

            print('ScriptNotifier email sent')
        except:
            from .utils import printerr as printerr
            printerr('Error sending email with ScriptNotifier Class', errtype='error')

    def text_myself(self, message, status=None):
        """
        Text yourself from python using a TWILIO account

        1. Set-up a trial account at twilio, some restrictions apply:
        limited number of messages
        phone numbers that are unused for 30 days are lost

        2. Get your twilio number to text from, your SID, and authToken

        3. pip install twilio

        Parameters:
            message (str): the message you want texted to yourself
            status (str): if included will be appended to the start of the text
                for example 'ERROR:'

        Note:
            length_limit in dictionary is used to trim the message so that you
            don't send a massive sized text to yourself. This allows you to send
            the first XXX number of characters of a crash report to yourself if you
            want.
        .. codeauthor:: Warren E. Black
        """

        # accountSID = "34characterSID"
        # authToken = "32characterTOKEN"
        # myNumber = '+17809995555'
        # twilioNumber = '+15873334444'

        # if status is supplied add to start of text message
        if status:
            message = status + message
        # check length of text message and trim if needed
        if len(message) > self.text_dict['length_limit']:
            message = message[:-self.text_dict['length_limit']]

        # Connect to twilio account
        self.connect_twilio()

        # Send text message
        self.twilio_client.messages.create(body=message, from_=self.text_dict['twilioNumber'],
                                           to=self.text_dict['myNumber'])
