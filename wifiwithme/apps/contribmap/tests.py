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


class TestContribPrivacy(TestCase):
    def test_always_private_field(self):
        c = Contrib.objects.create(
            name='John',
            phone='010101010101',
            contrib_type=Contrib.CONTRIB_CONNECT,
        )
        self.assertEqual(c.get_public_field('phone'), None)

    def test_public_field(self):
        c = Contrib.objects.create(
            name='John',
            phone='010101010101',
            contrib_type=Contrib.CONTRIB_CONNECT,
            privacy_name=True,
        )
        self.assertEqual(c.get_public_field('name'), 'John')

    def test_private_field(self):
        c = Contrib.objects.create(
            name='John',
            phone='010101010101',
            contrib_type=Contrib.CONTRIB_CONNECT,
        )
        self.assertEqual(c.privacy_name, False)
        self.assertEqual(c.get_public_field('name'), None)


class TestDataImport(TestCase):
    fixtures = ['bottle_data.yaml']

    def test_re_save(self):
        for contrib in Contrib.objects.all():
            contrib.full_clean()
            contrib.save()
