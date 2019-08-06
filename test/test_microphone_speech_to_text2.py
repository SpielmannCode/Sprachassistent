import unittest
from threading import Thread

import examples.microphone_speech_to_text2 as mi
from time import sleep


class Test_Mic_to_Text2(unittest.TestCase):

    def test_init(self):
        mic = mi.MicrophoneToText()

        self.assertTrue(mic.switch)
        self.assertIsNotNone(mic.resultkeywords)
        self.assertIsNotNone(mic.result)
        self.assertIsNotNone(mic.keywordsshort)
        # tests also chunk and maxbuffer
        self.assertIsNotNone(mic.q)
        self.assertIsNotNone(mic.keywords)
        self.assertIsNotNone(mic.resultkeywords)
        self.assertIsNotNone(mic.speech_to_text)
        # tests also audio, format, channel and rate
        self.assertIsNotNone(mic.stream)
        self.assertIsNotNone(mic.audio_source)

    def test_switchoff(self):
        mic = mi.MicrophoneToText()

        mic.switchoff()

        with self.assertRaises(OSError):
            mic.stream.is_active()
        self.assertFalse(mic.switch)
        self.assertFalse(mic.audio_source.is_recording)
        self.assertTrue(mic.result.closed)

    def test_analyze_text(self):

        mic = mi.MicrophoneToText()

        with open('C:/Users/RobinKaufmann/Desktop/Sprachassistent/examples/result.txt', 'w', encoding='utf-8') as f:
            f.write('x transcript": straße lautet aarbergerstraße }x\n')
            f.write('x transcript": ort lautet testort }x\n')
            f.write('x transcript": einkommen lautet testeinkommen }x\n')
            f.write('x transcript": kaufpreis lautet testkaufpreis }x\n')
            f.write('x transcript": eigenkapital lautet testkapital }x\n')

        #mic.threader()

        mic.switchoff()
        print(mic.keywords.values())
        with open('C:/Users/RobinKaufmann/Desktop/Sprachassistent/examples/result.txt', 'r', encoding='utf-8') as f:
            filestring = f.read()
            print(filestring)
            self.assertTrue(' straße lautet aarbergerstraße ' in filestring)


    def test_get_correct_keyword(self):
        mic = mi.MicrophoneToText()

        mic.keywordsshort = {'street': ['straße lautet aarbergerstraße'], 'location': ['ort lautet berlin'], 'income': ['einkommen lautet vierzigtausend']
                             , 'capital': ['eigenkapital lautet hundertfünfundzwanzigtausend'], 'price': ['kaufpreis lautet fünfhunderttausend']}

        mic.find_correct_keyword()

        self.assertEqual(mic.resultkeywords['street'], ['aarbergerstraße'])
        self.assertEqual(mic.resultkeywords['location'], ['berlin'])
        self.assertEqual(mic.resultkeywords['income'], [40000])
        self.assertEqual(mic.resultkeywords['capital'], [125000])
        self.assertEqual(mic.resultkeywords['price'], [500000])


    def test_find_word(self):
        mic = mi.MicrophoneToText()

        teststring = 'x transcript": ort lautet testort }x'

        word = mic.find_word(teststring)

        self.assertEqual(word, ' ort lautet testort ')

    def test_recognize(self):

        rec = mi.MyRecognizeCallback()
        rec.on_close()
        rec.on_connected()
        rec.on_data('"final": true truetestd')
        rec.on_error("testerror")
        rec.on_hypothesis("testh")
        rec.on_inactivity_timeout("testerrorinac")
        rec.on_listening()
        rec.on_transcription("testtr")
        self.assertIsNotNone(rec)

    def test_findcorrectkeyword(self):
        mic = mi.MicrophoneToText()

        mic.keywordsshort["street"] = ["adresse lautet amselweg", 'useless']
        mic.keywordsshort['location'] = ["der ort lautet berlin", 'useless']
        mic.keywordsshort['capital'] = ["der Kaufpreis lautet vierhunderttausend", 'useless']
        mic.keywordsshort['income'] = ["das Eigenkapital lautet 200000", 'useless']
        mic.keywordsshort['price'] = ["der kaufpreis beträgt fünfundzwanzigtausend", 'useless']

        mic.find_correct_keyword()

        self.assertEqual(mic.resultkeywords['street'], ['amselweg'])
        self.assertEqual(mic.resultkeywords['location'], ['berlin'])
        self.assertEqual(mic.resultkeywords['capital'], [400000])
        self.assertEqual(mic.resultkeywords['income'], [200000])
        self.assertEqual(mic.resultkeywords['price'], [25000])
