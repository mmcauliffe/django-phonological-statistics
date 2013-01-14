from django.test import TestCase

from utils import loadinPhonoStrings,getNeighCount,getPhonotacticProb

class PhonoStringTestCase(TestCase):
    def test_index(self):
        self.assertEqual(getNeighCount('T EH1 S T'),19)
