# -*- coding: utf-8 -*-

"""
providers
~~~~~~~~~~~~~~~~~

This module contains a list of email providers such as Mailchimp
 and can be used to add subscribers to a given mailing list
"""

from functools import wraps
import hashlib
from . import helpers
import json


class EmailProviderBase(object):
    """Base class that all provider classes derive from"""

    def add_subscriber(self, r):
        raise NotImplementedError('Add Subscriber not impremented.')


class MailchimpProvider(EmailProviderBase):
    """The provider integration with Mailchimp
    :param api_key: The Mailchimp api key
    :param list_id: The Mailchimp list id
    """

    def __init__(self, api_key, list_id):
        super(MailchimpProvider, self).__init__()
        self.api_key = api_key
        self.list_id = list_id
        if '-' not in api_key:
            raise Exception('Invalid api key')
        datacenter = self.api_key.split('-').pop()
        self.base_url = ''.join(
            ['https://', datacenter, '.api.mailchimp.com/3.0/'])
        self.auth = ('whatever', api_key)

    def prepare_subscriber(fn):
        @wraps(fn)
        def wrapper(self, subscriber, **kwargs):
            """
            Wrapper function to prepare a subscriber dict by modifying it's
             keys to match the Mailchimp corresponding ones.
            :param subscriber: The subscriber data
            :type subscriber: :py:class:`dict`
            :returns: fn
            """
            prepared_subscriber = {}
            """ Let it throw an error if email not provided """
            prepared_subscriber['email_address'] = subscriber['email']
            del subscriber['email']
            prepared_subscriber['merge_fields'] = {}
            for custom_field_name in subscriber:
                prepared_subscriber['merge_fields'][
                    custom_field_name] = subscriber[custom_field_name]
            return fn(self, prepared_subscriber, **kwargs)
        return wrapper

    @prepare_subscriber
    def add_subscriber(self, subscriber):
        """
        Add a subscriber to a Mailchimp list
        :param subscriber: The subscriber data to send
        :type subscriber: :py:class:`dict`
        :type subscriber: :py:class:`dict`
        :returns: The JSON output from the API or an error message
        """
        subscriber['status_if_new'] = 'subscribed'
        hash = self._get_hash(subscriber['email_address'])

        url = ''.join([self.base_url, 'lists/',
                       self.list_id, '/members/', hash])
        """
        use HTTP Method tunneling: make the call with POST,
        but include the method you intend to use in an
        X-HTTP-Method-Override header.
        """
        headers = {'x-http-method-override': 'PUT',
                   'content-type': 'application/json'}

        return helpers._make_request(**dict(
            method='POST',
            url=url,
            auth=self.auth,
            headers=headers,
            json=subscriber
        ))

    def _get_hash(self, email):
        """
        The MD5 hash of the lowercase version of the member's email.
        Used as hash
        :param email: The member's email address
        :returns: The MD5 hash in hex
        :rtype: :py:class:`str`
        """
        mh = hashlib.md5(email.lower().encode())
        return mh.hexdigest()


class KlaviyoProvider(EmailProviderBase):
    """The provider integration with Klaviyo
    :param api_key: The Klaviyo api key
    :param list_id: The Klaviyo list id
    """

    def __init__(self, api_key, list_id):
        super(KlaviyoProvider, self).__init__()
        self.api_key = api_key
        self.list_id = list_id
        self.base_url = 'https://a.klaviyo.com/api/v1/'
        self.auth = ('whatever', api_key)

    def prepare_subscriber(fn):
        @wraps(fn)
        def wrapper(self, subscriber, **kwargs):
            """
            Wrapper function to prepare a subscriber dict by modifying it's
             keys to match the Mailchimp corresponding ones.
            :param subscriber: The subscriber data
            :type subscriber: :py:class:`dict`
            :returns: fn
            """
            prepared_subscriber = {}
            """ Let it throw an error if email not provided """
            prepared_subscriber['email'] = subscriber['email']
            del subscriber['email']
            if 'confirm_optin' in subscriber:
                prepared_subscriber[
                    'confirm_optin'] = subscriber['confirm_optin']
                del subscriber['confirm_optin']
            prepared_subscriber['properties'] = {}
            for custom_field_name in subscriber:
                prepared_subscriber['properties'][
                    custom_field_name] = subscriber[custom_field_name]
            if 'properties' in prepared_subscriber:
                """ Encode properties """
                prepared_subscriber['properties'] = json.dumps(
                    prepared_subscriber['properties'])
            return fn(self, prepared_subscriber, **kwargs)
        return wrapper

    @prepare_subscriber
    def add_subscriber(self, subscriber):
        """
        Add a subscriber to a Klaviyo list
        :param subscriber: The subscriber data to send
        :type subscriber: :py:class:`dict`
        :type subscriber: :py:class:`dict`
        :returns: The JSON output from the API or an error message
        """
        url = ''.join([self.base_url, 'list/', self.list_id, '/members'])

        return helpers._make_request(**dict(
            method='POST',
            url=url,
            data=subscriber,
            params={'api_key': self.api_key}
        ))
