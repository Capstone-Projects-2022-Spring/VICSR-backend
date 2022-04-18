from django.test import TestCase, Client
from rest_framework.test import APIClient
from DocumentManagement.models import Document
from AccountManagement.models import User
from rest_framework.authtoken.models import Token


# Create your tests here.
class DocumentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user  = User.objects.create_user(username='testuser', email='test@test.com', password='testpass1')
        Document.objects.create(owner_id=self.user, filename='doc', mode= 'TRL', language= 'en',
                                trans_language= 'fr')
        Document.objects.create(owner_id=self.user, filename='doc2', mode='DEF', language='en')
        self.client.login(email='test@test.com', password='testpass1')


    def test_getDocs(self):
        docs = Document.objects.filter(owner_id=self.user)
        self.assertEqual(docs.count(), 2)

    def test_addDoc(self):
        doc = Document.objects.create(owner_id=self.user, filename='test_doc', mode= 'TRL', language= 'en', trans_language= 'fr')
        self.assertEqual(doc.filename, 'test_doc')
        docs = Document.objects.filter(owner_id=self.user)
        self.assertEqual(docs.count(), 3)

    def test_addDocAPI(self):
        self.client.force_authenticate(user=self.user)
        with open('DocumentManagement/testDocuments/highlightDEskewed.png', 'rb') as fp:
            response = self.client.post('/api/docs/add/', {'filename': 'test_doc', 'file': fp, 'mode': 'TRL',
                                                  'language': 'en', 'trans_language': 'fr'})
        self.assertEqual(response.status_code, 200)
        docs = Document.objects.filter(owner_id=self.user)
        self.assertEqual(docs.count(), 3)

    def test_getDocsAPI(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/docs/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)