Email Providers Integration Module Repository
========================

This is a first attempt to create a python module and learn python :)
What this module does is integrate with various popular email providers such as Mailchimp in order to add a subscriber to a given list.
---------------

This repo's structure is based on Kenneth Reitz's sample module

`Learn more <http://www.kennethreitz.org/essays/repository-structure-and-python>`_.

---------------

Usage
---------------
::

    m = MailchimpProvider('YOUR_MAILCHIMP_API_KEY', 'YOUR_MAILCHIMP_LIST_ID')

    sub1 = {'FNAME': 'Jane', 'LNAME': 'Doe', 'email': 'jane.doe@example.com'}

    m.add_subscriber(sub1)

    k = KlaviyoProvider('YOUR_KLAVIYO_API_KEY', 'YOUR_KLAVIYO_LIST_ID')

    sub2 = {'$first_name': 'Jane', '$last_name': 'Doe', 'email': 'jane.doe@example.com'}

    k.add_subscriber(sub2)



