from django.test import TestCase, SimpleTestCase, RequestFactory, TransactionTestCase
from payments.models import User
from payments.forms import SigninForm, UserForm
from django import forms, setup
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from payments.views import *
import mock
import stripe




