from django.test import TestCase, SimpleTestCase, RequestFactory, TransactionTestCase
from payments.models import User, CustomerManager
from payments.forms import SigninForm, UserForm
from django import forms, setup
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from payments.views import *
import mock
import stripe



class CustomerManagerTest(TestCase):

    def test_create_stripe_customer(self):
        # cleaned_data = {'email': 'j@j.com', 'name': 'test user',
        #                 'stripe_token': '4242', 'plan': 'gold'}
        # customer = CustomerManager.create(data=cleaned_data,
        #                                   billing_type='subscription')
        # self.assertEquals(cleaned_data['plan'], customer.plan)
        pass

    def test_create_stripe_charge(self):
        pass

