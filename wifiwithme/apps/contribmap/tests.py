from django.test import TestCase

from contribmap.models import Contrib


class TestContrib(TestCase):
    def test_comma_separatedcharfield(self):
        co = Contrib(name='foo', orientations=['SO', 'NE'])
        co.save()
        self.assertEqual(
            Contrib.objects.get(name='foo').orientations,
            ['SO', 'NE'])
        co.orientations = ['S']
        co.save()


class TestDataImport(TestCase):
    fixtures = ['bottle_data.yaml']

    def test_re_save(self):
        for contrib in Contrib.objects.all():
            contrib.full_clean()
            contrib.save()
