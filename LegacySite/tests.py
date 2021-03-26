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


    def test_sqlInjection(self):
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

    def test_commandInjection(self):
        payload_file = "Part1/regular.gftcrd"
        password_regex = re.compile(r"(?:\(Username: (\w+) ; Password: ([\d\$a-f]{97})\))") # (r"[\d\$a-f]{97}")
        
        c = Client()
        assert c.login(username="jerry", password="tom"),"Failed to login as user!"
		
        with open(payload_file, "rb") as f:
            uploaded_file = SimpleUploadedFile(payload_file, f.read(),"application/octet-stream")
            resp = c.post("/use.html", {"card_data": uploaded_file, "card_fname": "& echo hey, it worked &", "card_supplied": True})
        if resp.status_code == 200:
            found = password_regex.findall(resp.content.decode())
            print(json.dumps(found, indent=4))
            assert not found, "hey, it worked"