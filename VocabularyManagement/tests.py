from django.test import TestCase
from rest_framework.test import APIClient
from VocabularyManagement.models import StudySet, StudySetWord
from AccountManagement.models import User
from DocumentManagement.models import Document
# Create your tests here.

class VocabularyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username = 'testuser', email = 'test@test.com', password = 'testpass1')
        self.client.login(email='test@test.com', password='testpass1')
        self.client.force_authenticate(user=self.user)

        with open('media/highlightDEskewed.png', 'rb') as fp:
            response = self.client.post('/api/docs/add/', {'filename': 'test_doc', 'file': fp, 'mode': 'TRL',
                                                       'language': 'en', 'trans_language': 'fr'})

    def test_getSetsAPI(self):
        response = self.client.get('/api/vocab/sets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_getSetsByDocIDAPI(self):
        doc = Document.objects.filter(owner_id=self.user).first().id
        url = '/api/vocab/sets/fromDoc/' + str(doc)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_getWordsBySetIDAPI(self):
        set = StudySet.objects.filter(owner_id=self.user).first().id
        url = '/api/vocab/sets/' + str(set) + '/words'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_getAllWordsAPI(self):
        url = '/api/vocab/allWords'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_updateRankingAPI(self):
        word = StudySetWord.objects.filter(owner_id=self.user).first().id
        self.assertEqual(word.ranking, 2)
        url = '/api/vocab/sets/words/update/' + str(word)
        response = self.client.post(url, 3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(word.ranking, 3)


