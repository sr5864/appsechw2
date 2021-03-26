from django.test import TestCase, Client
from io import StringIO
import json
from django.core.files.uploadedfile import SimpleUploadedFile
import re

import random


# Create your tests here.

class MyTestCase(TestCase):
    fixtures = ['testdata.json']
#     def setUp(self):
#         self.client = Client()
#     def test_details(self):
#         response = self.client.get('/buy.html')
#         print(response.content)
    def test_xss(self):
        self.client = Client()
        response = self.client.get('/gift.html?director=<script>alert("I hope this works");</script>/')
        assert b'&lt;script&gt;alert(&quot;I hope this works&quot;);&lt;/script&gt' in response.content


    def test_csrf(self):
        self.client = Client()
        response = self.client.post('/attack/', {'amount': '99999', 'username': 'attacker' })
        self.assertEqual(response.status_code, 404)


    def test_sqli(self):
        payload_file = "Part1/sqlinjection.gftcrd"
        password_regex = re.compile(r"(?:\(Username: (\w+) ; Password: ([\d\$a-f]{97})\))") # (r"[\d\$a-f]{97}")
        
        c = Client()
        assert c.login(username="jerry", password="tom"),"Failed to login as user!"
		
        with open(payload_file, "rb") as f:
            uploaded_file = SimpleUploadedFile(payload_file, f.read(),"application/octet-stream")
            resp = c.post("/use.html", {"card_data": uploaded_file, "card_fname": "c", "card_supplied": True})
        if resp.status_code == 200:
            found = password_regex.findall(resp.content.decode())
            print(json.dumps(found, indent=4))
            assert not found, "IT'S WORKING!"



    # def test_commandInjection(self):
    #     self.client = Client()
    #     assert self.client.login(username="test", password="000000000000000000000000000078d2$a8dfe9d76be66382be9a0e809d087342e2aa8cc7060721784d7163ae49141143"),"Failed to login as user!"
    #     obj = {"merchant_id": "NYU Apparel Card", "customer_id": "test", "total_value": "20202020202", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": "[ insert crypto signature here ]"}]}
    #     f = StringIO(json.dumps(obj))
    #     # json.dump({"merchant_id": "NYU Apparel Card", "customer_id": "test", "total_value": "20202020202", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": "[ insert crypto signature here ]"}]}, f)
    #     # print(f.getvalue())
    #     #  response = self.client.post('/use.html', { 'card_fname': 'zq', 'card_supplied': True, 'card_data': f})
    #     response = self.client.post('/use.html', {'card_fname': '& echo hey, my injection worked &', 'card_supplied': True, 'card_data': f})
    #     print(response.content)
    #     self.assertNotContains(response.content, 'hey, my injection worked')