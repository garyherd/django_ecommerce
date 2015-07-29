"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from main.views import index
from django.shortcuts import render_to_response
from payments.views import sign_in, sign_out, register, edit
import mock


class MainPageTests(TestCase):

    ###########
    ## Setup ##
    ###########

    @classmethod
    def setUpClass(cls):
        super(MainPageTests, cls).setUpClass()
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    ####################
    ## Testing routes ##
    ####################

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_sign_in_resolves_to_signin_view(self):
        signin_page = resolve('/sign_in')
        self.assertEqual(signin_page.func, sign_in)

    def test_sign_out_resolves_to_signout_view(self):
        signout_page = resolve('/sign_out')
        self.assertEqual(signout_page.func, sign_out)

    def test_register_resolves_to_register_view(self):
        register_page = resolve('/register')
        self.assertEqual(register_page.func, register)

    def test_edit_resolves_to_edit_view(self):
        edit_page = resolve('/edit')
        self.assertEqual(edit_page.func, edit)

    def test_returns_appropriate_html_response_code(self):
        resp = index(self.request)
        self.assertEquals(resp.status_code, 200)

    #################################
    ## Testing templates and views ##
    #################################

    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEquals(
            resp.content,
            render_to_response("index.html").content
        )

    def test_index_handles_logged_in_user(self):
        # create a session that appears to have a logged in user
        self.request.session = {'user': "1"}

        with mock.patch('main.views.User') as user_mock:

            # Tell the mock what to do when called
            config = {'get_by_id.return_value': mock.Mock()}
            user_mock.configure_mock(**config)

            # request the index page
            resp = index(self.request)

            # ensure we return the state of the session back to normal so we
            # don't affect other tests
            self.request.session = {}

            # verify it returns the page for the logged-in user
            expectedHtml = render_to_response(
                'user.html', {'user': user_mock.get_by_id(1)})
            self.assertEquals(resp.content, expectedHtml.content)

    def test_signout_view_signs_out_user(self):
        self.request.session = {'user': '1'}
        sign_out(self.request)
        self.assertEquals({}, self.request.session)