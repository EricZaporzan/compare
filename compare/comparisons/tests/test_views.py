from django.test import RequestFactory

from test_plus.test import TestCase

from ..views import (
    ComparisonCreateView,
    ComparisonUpdateView,
    ComparisonDetailView,
    ComparisonListView,
    ComparisonItemCreateView
)

class BaseComparisonTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()
