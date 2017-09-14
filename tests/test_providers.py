# -*- coding: utf-8 -*-

from providers.core import MailchimpProvider, KlaviyoProvider

import unittest


class ProvidersTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_mailchimp_invalid_api_key(self):
        with self.assertRaises(Exception) as context:
            MailchimpProvider(
                'asdf', 'lala')
        self.assertTrue('Invalid api key' in context.exception)

    def test_mailchimp_subscriber_email_not_provided(self):
        m = MailchimpProvider(
            'asdf-us13', 'asdf')
        with self.assertRaises(Exception) as context:
            m.add_subscriber({'name': 'Foteini'})
        self.assertTrue('email' in context.exception)

    def test_klaviyo_subscriber_email_not_provided(self):
        m = KlaviyoProvider(
            'asdf', 'asdf')
        with self.assertRaises(Exception) as context:
            m.add_subscriber({'name': 'Foteini'})
        self.assertTrue('email' in context.exception)


if __name__ == '__main__':
    unittest.main()
