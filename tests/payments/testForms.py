from django.test import TestCase, SimpleTestCase, RequestFactory, TransactionTestCase
from payments.models import User, CustomerManager
from payments.forms import SigninForm, UserForm
from django import forms, setup
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from payments.views import *
import mock
import stripe
from ..utilities import FormTesterMixin




class FormTests(FormTesterMixin, SimpleTestCase):

    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', [u'This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertFormError(SigninForm,
                                 invalid_data['error'][0],
                                 invalid_data['error'][1],
                                 invalid_data["data"])

    def test_user_form_passwords_match(self):
        form = UserForm(
            {'name': 'jj',
             'email': 'j@j.com',
             'password': '1234',
             'ver_password': '1234',
             'last_4_digits': '3333',
             'stripe_token': '1'}
        )
        # Is this data valid? -- if not print out the errors
        self.assertTrue(form.is_valid(), form.errors)

        # this will throw an error if the form doesn't clean correctly
        self.assertIsNotNone(form.clean())

    def test_user_form_passwords_dont_match_throws_error(self):
        form = UserForm(
            {'name': 'jj',
             'email': 'j@j.com',
             'password': '234',
             'ver_password': '1234',
             'last_4_digits': '3333',
             'stripe_token': '1'}
        )

        # Is the data valid?
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords do not match",
                                 form.clean)