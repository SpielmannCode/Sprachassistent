from unittest import TestCase
from examples.convertsentence import ConvertSent

class TestConvertSent(TestCase):

    def test_init(self):
        cnv = ConvertSent()

        self.assertIsNotNone(cnv.cities)
        self.assertIsNotNone(cnv.streets)

    def test_findstreet(self):
        cnv = ConvertSent()
        text = 'adolf wohnt an der adickesstraße'
        res = cnv.find_street(text)

        self.assertEqual(res, 'adickesstraße')

        text = 'adickesstraße'
        res = cnv.find_street(text)

        self.assertEqual(res, 'adickesstraße')

        text = 'blabla bla blup'
        res = cnv.find_street(text)

        self.assertEqual(res, None)

    def test_findcity(self):
        cnv = ConvertSent()
        text = 'die falkenhagener wohnen am falkenhagener feld'
        res = cnv.find_city(text)

        self.assertEqual(res, 'falkenhagener feld')

        text = 'falkenhagener falkenhagener feld'
        res = cnv.find_city(text)

        self.assertEqual(res, 'falkenhagener feld')

        text = 'blabla blup'
        res = cnv.find_city(text)

        self.assertEqual(res, None)
