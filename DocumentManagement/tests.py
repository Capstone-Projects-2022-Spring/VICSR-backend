from django.test import TestCase, Client
from rest_framework.test import APIClient
from DocumentManagement.models import Document
from AccountManagement.models import User


# Create your tests here.
class DocumentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user  = User.objects.create_user(username='testuser', email='test@test.com', password='testpass1')
        Document.objects.create(owner_id=self.user, filename='doc', mode= 'TRL', language= 'en',
                                trans_language= 'fr')
        Document.objects.create(owner_id=self.user, filename='doc2', mode='DEF', language='en')
        self.client.login(email='test@test.com', password='testpass1')
        self.client.force_authenticate(user=self.user)

    def test_addDocAPI(self):
        with open('DocumentManagement/testDocuments/highlightDEskewed.png', 'rb') as fp:
            response = self.client.post('/api/docs/add/', {'filename': 'test_doc', 'file': fp, 'mode': 'TRL',
                                                  'language': 'en', 'trans_language': 'fr'})
        self.assertEqual(response.status_code, 200)
        docs = Document.objects.filter(owner_id=self.user)
        self.assertEqual(docs.count(), 3)

    def test_getDocsAPI(self):
        response = self.client.get('/api/docs/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_deleteDocAPI(self):
        doc = Document.objects.filter(owner_id=self.user).first()
        url = '/api/docs/delete/' + str(doc.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 202)
        docs = Document.objects.filter(owner_id=self.user)
        self.assertEqual(len(docs), 1)

    def test_renameDocAPI(self):
        doc = Document.objects.filter(owner_id=self.user).first()
        url = '/api/docs/update/' + str(doc.id)
        response = self.client.post(url, {'filename': 'NEW_NAME'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'NEW_NAME')


