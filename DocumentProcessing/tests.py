from django.test import TestCase, Client
from rest_framework.test import APIClient
from AccountManagement.models import User
from DocumentProcessing.models import File, DocumentWord
from DocumentManagement.models import Document
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class FileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass1')
        self.client.login(email='test@test.com', password='testpass1')
        doc = Document.objects.create(owner_id=self.user, filename='doc', mode='TRL', language='en',
                                      trans_language='fr')
        f = File(document=doc)
        f.file = SimpleUploadedFile(name='highlight+skewed.png',
                                    content=open('media/highlight+skewed.png', 'rb').read())
        f.save()
        self.client.force_authenticate(user=self.user)

    def test_addFile(self):
        doc = Document.objects.create(owner_id=self.user, filename='doc1', mode='DEF', language='en')
        f = File(document=doc)
        f.file = SimpleUploadedFile(name='highlight+skewed.png', content=open('media/highlight+skewed.png', 'rb').read())
        f.save()
        files = File.objects.filter(document=doc)
        self.assertEqual(files.count(), 1)

    #confirm deleting doc deletes file
    def test_delDoc_delFile(self):
        doc = Document.objects.filter(owner_id=self.user).first()
        doc.delete()
        files = File.objects.filter(document=doc)
        self.assertEqual(files.count(), 0)

    def test_updateHighlightAPI(self):
        doc = Document.objects.filter(owner_id=self.user).first()
        file = File.objects.filter(document=doc)
