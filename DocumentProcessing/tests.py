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
        file = File.objects.filter(document=doc).first()
        #highlight below is for word vocabulary
        highlight = str({"lines":[{"points":[{"x":37.99220080340999,"y":312.7779029759459},{"x":37.99220080340999,"y":312.7779029759459},{"x":39.4761881389204,"y":312.34690307455134},{"x":41.351421904681985,"y":311.882816046382},{"x":43.25904066540214,"y":311.47989392985255},{"x":45.190778506149805,"y":311.1312643452154},{"x":46.16273298664404,"y":310.969545545174},{"x":47.13878819693677,"y":310.8197951980576},{"x":49.10209948409894,"y":310.56203819214556},{"x":50.08704642292273,"y":310.4427532950584},{"x":51.0742063716986,"y":310.33245875552143},{"x":52.06325572158113,"y":310.2305023493006},{"x":53.053917710290996,"y":310.13627370272343},{"x":54.04595577078665,"y":310.04920282405783},{"x":56.03377794683339,"y":309.89973872558045},{"x":58.024824295430015,"y":309.77147057278734},{"x":60.0182424943522,"y":309.661428057957},{"x":62.01340493649996,"y":309.56704389924977},{"x":64.07461467015929,"y":309.3361080550689},{"x":66.05485724334812,"y":309.1461084255895},{"x":67.04675681381131,"y":309.05828981466976},{"x":69.03436697913794,"y":308.9075386548547},{"x":70.02928881494455,"y":308.83789839717497},{"x":71.0249602959285,"y":308.77357875223595},{"x":72.021270955385,"y":308.71417818203656},{"x":73.01812655090711,"y":308.65932438899443},{"x":74.09684050537645,"y":308.52144472313427},{"x":75.08256033793161,"y":308.40521596239125},{"x":76.07038022830588,"y":308.29775656530984},{"x":78.05174199871779,"y":308.113162492539},{"x":79.04410079851709,"y":308.0278493488738},{"x":80.03758641258324,"y":307.9490316978831},{"x":82.02762422115487,"y":307.81376790924827},{"x":83.02354148590544,"y":307.7512931918845},{"x":85.01729959544328,"y":307.6441203417344},{"x":86.01474192994105,"y":307.59463349559786},{"x":87.01256222127006,"y":307.5489403438245},{"x":88.01070466709565,"y":307.5067518331473},{"x":89.00912169018335,"y":307.4678005549041},{"x":91.00670222180577,"y":307.401009231267},{"x":92.00571098593039,"y":307.3701770481392},{"x":93.00486632312408,"y":307.3417134382446},{"x":95.00357542055696,"y":307.2929117780745},{"x":96.00304657395996,"y":307.27038582327145},{"x":97.00259594218642,"y":307.2495914132302},{"x":98.00221195963168,"y":307.23039561279404},{"x":99.00188477030954,"y":307.2126756569758},{"x":100.00160597529802,"y":307.1963181805028},{"x":101.00136841744971,"y":307.1812185040962},{"x":102.0011659978808,"y":307.1672799736613},{"x":104.00085666084745,"y":307.1433845405573},{"x":105.00072993941592,"y":307.1323556314267},{"x":106.00062196278681,"y":307.1221749567046},{"x":107.00052995832652,"y":307.11277729816175},{"x":108.0004515634814,"y":307.10410244783003},{"x":109.00038476513508,"y":307.0960948239909},{"x":109.03390149982876,"y":307.09861956744135},{"x":110.02889203991087,"y":307.1677895651395},{"x":111.02462210384397,"y":307.2316743891699},{"x":112.02098271066816,"y":307.2906730077821},{"x":113.017880887077,"y":307.34515531328},{"x":114.0152373305211,"y":307.39546401574023},{"x":115.01298440951486,"y":307.44191646372064},{"x":116.01106445357975,"y":307.4848063822397},{"x":116.09470248319535,"y":307.49537677926827},{"x":117.08073661001235,"y":307.61033808424486},{"x":117.23413596699028,"y":307.64109271976866},{"x":118.1997658882237,"y":307.8195241557699},{"x":118.1997658882237,"y":307.8195241557699}],"brushColor":"#FFFF0080","brushRadius":10}],"width":794,"height":1123})
        url = '/api/files/update/' + str(file.id)
        response = self.client.post(url, {'highlight': highlight})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['word'], 'registration')
        self.assertEqual(response.data[1]['word'], 'identified')
        self.assertEqual(response.data[2]['word'], 'documents')
        self.assertEqual(response.data[3]['word'], 'vocabulary')