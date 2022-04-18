from django.test import TestCase, Client

import backend
from DocumentManagement.models import Document
from AccountManagement.models import User

# Create your tests here.
class DocumentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        #this code doesn't seem to set up a user, as it should
        user = self.client.force_login(User.objects.get_or_create(email='testuser@test.com', password='testpass')[0])
        print("user", user)

    def test_addDoc(self):
        doc = Document.objects.create(owner_id_id=1, filename='test_doc', mode= 'TRL', language= 'en', trans_language= 'fr')
        self.assertEqual(doc.filename, 'test_doc')

    def test_addDocAPI(self):
        #get 401 error on test -- need to confirm how to add auth
        with open('DocumentManagement/testDocuments/highlightDEskewed.png', 'rb') as fp:
            response = self.client.post('/api/docs/add/', {'filename': 'test_doc', 'file': fp, 'mode': 'TRL',
                                                  'language': 'en', 'trans_language': 'fr'})
        self.assertEqual(response.status_code, 200)

