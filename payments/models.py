from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import django_ecommerce.settings as settings
import stripe

stripe.api_key = settings.STRIPE_SECRET



class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    # password field defined in base class
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    @classmethod
    def get_by_id(cls, uid):
        return User.objects.get(pk=uid)

    def __str__(self):
        return self.email

    # user = User(
    #     name=form.cleaned_data['name'],
    #     email=form.cleaned_data['email'],
    #     last_4_digits=form.cleaned_data['last_4_digits'],
    #     stripe_id=customer.id,
    # )
    #
    # # ensure encrypted password
    # user.set_password(form.cleaned_data['password'])
    #
    # try:
    #     user.save()

    @classmethod
    def create(cls, name, email, password, last_4_digits, stripe_id):
        new_user = cls(name=name, email=email,
                       last_4_digits=last_4_digits, stripe_id=stripe_id)
        new_user.set_password(password)

        new_user.save()
        return new_user


class CustomerManager(object):


    @classmethod
    def create(cls, data, billing_type):
        if billing_type == 'subscription':
            new_customer = stripe.Customer.create(
                email=data['email'],
                description=data['name'],
                card=data['stripe_token'],
                plan=data['plan']
            )
        elif billing_type == 'one-time':
            new_customer = stripe.Charge()
        else:
            new_customer = None
        # TODO: create some sort of error?

        return new_customer

                # customer = stripe.Customer.create(
                # email=form.cleaned_data['email'],
                # description=form.cleaned_data['name'],
                # card=form.cleaned_data['stripe_token'],
                # plan="gold",