from django.test import TestCase

from contribmap.models import Contrib


class TestDataImport(TestCase):
    fixtures = ['bottle_data.yaml']

    def test_re_save(self):
        for contrib in Contrib.objects.all():
            contrib.full_clean()
            contrib.save()
