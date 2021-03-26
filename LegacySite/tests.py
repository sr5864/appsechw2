from django.test import TestCase, Client
from io import StringIO
import json
from django.core.files.uploadedfile import SimpleUploadedFile


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

        
    # def test_sqli(self):
    #     self.client = Client()
    #     # response = c.get('/use.html')
    #     # response = self.client.get('/use/', 'file':'sqlinjection.gftcrd')
    #     # print(response.content)
    #     # assert b'pass' in response.content
    #     # with open('/Users/ShiraRubin/Desktop/appsechw2/newcard (1).gftcrd') as fp:
    #     #     response = self.client.post('/use-card/', {'file': fp})
    #     #     print(response.content)
    #         # assert b'psswd' in response.content
    #     # giftcard = SimpleUploadedFile('/Part1/sqlinjection.gftcrd', b'')
    #     # self.client.post('/use/', {'file': giftcard})
    #     # print(response.content)
    #     # assert b'psswd' in response.content
    #     # f =  SimpleUploadedFile('/Part1/sqlinjection.gftcrd')
        
    #     obj = {"records": [{"signature": "'union select username || password  from LegacySite_User --"}]}
        
    #     f = StringIO(json.dumps(obj))
    #     # with open('Part1/sqlinjection.gftcrd') as f:
    #     response = self.client.post('/use.html', { 'card_fname': 'zq', 'card_supplied': True, 'card_data': f})
    #     print(response.content)
    #     self.assertRaises(KeyError)



    # def test_commandInjection(self):
    #     self.client = Client()
    #     f = StringIO()
    #     json.dump({"merchant_id": "NYU Apparel Card", "customer_id": "test", "total_value": "20202020202", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": "[ insert crypto signature here ]"}]}, f)
    #     # print(f.getvalue())
    #     #  response = self.client.post('/use.html', { 'card_fname': 'zq', 'card_supplied': True, 'card_data': f})
    #     response = self.client.post('/use', {'card_fname': '& echo hey,it worked &', 'card_supplied': True, 'card_data': f})
    #     print(response)
    #     self.assertNotContains(response.content, 'hey, my injection worked')