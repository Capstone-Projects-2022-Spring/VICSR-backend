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
        word = StudySetWord.objects.filter(owner_id=self.user).first()
        self.assertEqual(word.ranking, 2)
        url = '/api/vocab/sets/words/update/' + str(word.id)
        response = self.client.post(url, {'ranking': 3})
        self.assertEqual(response.status_code, 200)
        word = StudySetWord.objects.filter(owner_id=self.user).first()
        self.assertEqual(word.ranking, 3)

    def test_deleteSetAPI(self):
        newSet = StudySet.objects.create(owner_id=self.user, title="new set")
        sets = StudySet.objects.filter(owner_id=self.user)
        self.assertEqual(len(sets), 2)
        url = '/api/vocab/sets/delete/' + str(newSet.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 202)
        sets = StudySet.objects.filter(owner_id=self.user)
        self.assertEqual(len(sets), 1)

    def test_renameSetAPI(self):
        set = StudySet.objects.filter(owner_id=self.user).first()
        url = '/api/vocab/sets/update/' + str(set.id)
        response = self.client.post(url, {'title': 'NEW_NAME'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'NEW_NAME')

    def test_newSetAPI(self):
        url = '/api/vocab/sets/add'
        response = self.client.post(url, {'title': 'NEW_SET'})
        self.assertEqual(response.status_code, 200)
        sets = StudySet.objects.filter(owner_id=self.user)
        self.assertEqual(len(sets), 2)

    def test_addWordToSetAPI(self):

        allWords = StudySetWord.objects.filter(owner_id=self.user)
        self.assertEqual(len(allWords), 3)

        newSet = StudySet.objects.create(owner_id=self.user, title="new set")

        word = StudySetWord.objects.filter(owner_id=self.user).first()
        url = '/api/vocab/sets/addWord'
        response = self.client.post(url, {'set_id': newSet.id, 'word_id': word.id})
        self.assertEqual(response.status_code, 200)

        allWords = StudySetWord.objects.filter(owner_id=self.user)
        self.assertEqual(len(allWords), 4)