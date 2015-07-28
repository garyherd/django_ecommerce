from django.test import TestCase, SimpleTestCase, RequestFactory, TransactionTestCase
from payments.models import User, CustomerManager
from payments.forms import SigninForm, UserForm
from django import forms, setup
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from payments.views import *
import mock
import stripe

class ViewTesterMixin(object):

    # noinspection PyPep8Naming
    @classmethod
    def setupViewTester(cls, url, view_func, expected_html,
                        status_code=200, session={}):
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolves_to_correct_view(self):
        test_view = resolve(self.url)
        self.assertEqual(test_view.func, self.view_func)

    def test_returns_appropriate_response_code(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.content, self.expected_html)


class SignInPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        super(SignInPageTests,cls).setUpClass()
        html = render_to_response(
            'sign_in.html',
            {
                'form': SigninForm(),
                'user': None
            }
        )

        ViewTesterMixin.setupViewTester(
            '/sign_in',
            sign_in,
            html.content
        )

    @classmethod
    def tearDownClass(cls):
        super(SignInPageTests, cls).tearDownClass()


class SignOutPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        super(SignOutPageTests, cls).setUpClass()
        setup()
        ViewTesterMixin.setupViewTester(
            '/sign_out',
            sign_out,
            b"",  # a redirect will return no html
            status_code=302,
            session={'user': 'dummy'}
        )

    @classmethod
    def tearDownClass(cls):
        # super(SignOutPageTests, cls).tearDownClass()
        pass
    def setUp(self):
        self.request.session = {'user': 'dummy'}


class RegisterPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        super(RegisterPageTests, cls).setUpClass()
        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': list(range(1, 13)),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': list(range(2011, 2036)),
            }
        )
        ViewTesterMixin.setupViewTester(
            '/register',
            register,
            html.content,
        )

    @classmethod
    def tearDownClass(cls):
        super(RegisterPageTests, cls).tearDownClass()

    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    def test_invalid_form_returns_registration_page(self):

        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False

            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEqual(resp.content, self.expected_html)

            # make sure that we did indeed call our is_valid function
            self.assertEqual(user_mock.call_count, 1)

    @mock.patch('stripe.Customer.create')
    @mock.patch.object(User, 'create')
    def test_registering_new_user_returns_successfully(
            self, create_mock, stripe_mock
    ):

        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '4242424242424242',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # get the return values of the mocks, for our checks later
        new_user = create_mock.return_value
        new_cust = stripe_mock.return_value

        resp = register(self.request)
        self.assertEqual(resp.content, "")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.request.session['user'], new_user.pk)

        # verify the user was actually stored in the database.
        create_mock.assert_called_with(
            'pyRock', 'python@rocks.com', 'bad_password', '4242', new_cust.id
        )


    def test_registering_user_twice_cause_error_msg(self):

        # create a user with same email so we get an integrity error
        user = User(name='pyRock', email='python@rocks.com')
        user.save()

        # now create the request used to test the view
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # create our expected form
        expected_form = UserForm(self.request.POST)
        expected_form.is_valid()
        expected_form.addError('python@rocks.com is already a member')

        # create the expected html
        html = render_to_response(
            'register.html',
            {
                'form': expected_form,
                'months': list(range(1, 13)),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': list(range(2011, 2036)),
            }
        )
        # mock out stripe so we don't hit their server
        with mock.patch('stripe.Customer') as stripe_mock:
            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            # run the test
            resp = register(self.request)

            # verify that we did things correctly
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.request.session , {})
            #self.assertEquals(resp.content, html.content)
            self.maxDiff = None
            self.assertHTMLEqual(resp.content, html.content)

            # assert there is only one record in the database.
            # users = User.objects.filter(email='python@rocks.com')
            # self.assertEquals(len(users), 1)
