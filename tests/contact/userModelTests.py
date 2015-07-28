"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from contact.models import ContactForm
from datetime import datetime, timedelta
import time


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(UserModelTest, cls).setUpClass()
        ContactForm(email='test@dummy.com', name='test').save()
        time.sleep(1)
        ContactForm(email='j@j.com', name='jj').save()
        time.sleep(1)
        cls.someUser = ContactForm()
        cls.someUser.email = 'first@first.com'
        cls.someUser.name = 'first'
        cls.someUser.timestamp = datetime.today() + timedelta(days=2)
        cls.someUser.save()

    def test_contactform_str_returns_email(self):
        self.assertEquals('first@first.com', str(self.someUser))

    def test_ordering(self):
        contacts = ContactForm.objects.all()
        for contact in contacts:
            print contact.name, contact.timestamp
        self.assertEquals(self.someUser, contacts[0])
