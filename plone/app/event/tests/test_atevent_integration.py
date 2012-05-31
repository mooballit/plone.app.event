import pytz
import unittest2 as unittest
from datetime import datetime
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.event.interfaces import IEventAccessor
from plone.app.event.testing import PAEventAT_INTEGRATION_TESTING


class PAEventATTest(unittest.TestCase):
    layer = PAEventAT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_event_accessor(self):
        utc = pytz.utc
        self.portal.invokeFactory('Event', 'event1',
                start=datetime(2011,11,11,11,0, tzinfo=utc),
                end=datetime(2011,11,11,12,0, tzinfo=utc),
                timezone='UTC',
                whole_day=False)
        e1 = self.portal['event1']

        # setting attributes via the accessor
        acc = IEventAccessor(e1)
        acc.end = datetime(2011,11,13,10,0)
        acc.timezone = 'CET'

        cet = pytz.timezone('CET')

        # accessor should return end datetime in the event's timezone
        self.assertTrue(acc.end == datetime(2011,11,13,11,0, tzinfo=cet))

        # end datetime is stored in utc on the content object
        self.assertTrue(e1.end == datetime(2011,11,13,10,0, tzinfo=utc))

        # timezone should be the same on the event object and accessor
        self.assertTrue(e1.timezone == acc.timezone)
