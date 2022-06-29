from django.test import TestCase, Client

from .models import Profile
import json

client = Client()

class SingupTest(TestCase):
    def test_signup_success(self):
        data = {
            "email":"smc5407@naver.com",
            "username":"celebrate",
            "password":"msc583446!"
        }

        response = client.post('/routine/signup/',json.dumps(data),content_type='application/json')

        self.assertEqual(response.json(),{
            "message":{
                "msg":" .",
                "status": "SIGNUP_OK"
            }
        })

    def test_signup_fail_short_password(self):
        data = {
            "email":"smc5407@naver.com",
            "username":"celebrate",
            "password":"msc583"
        }

        response = client.post('/routine/signup/',json.dumps(data),content_type='application/json')

        self.assertEqual(response.json(),{
            "message":{
                "msg":"password is too short.",
                "status": "SIGNUP_FAIL"
            }
        })

    def test_signup_fail_no_number_password(self):
        data = {
            "email":"smc5407@naver.com",
            "username":"celebrate",
            "password":"msc!!!!!!"
        }

        response = client.post('/routine/signup/',json.dumps(data),content_type='application/json')

        self.assertEqual(response.json(),{
            "message":{
                "msg":"password is not include number.",
                "status": "SIGNUP_FAIL"
            }
        })
    def test_signup_fail_no_special_words_password(self):
        data = {
            "email":"smc5407@naver.com",
            "username":"celebrate",
            "password":"msc583446"
        }

        response = client.post('/routine/signup/',json.dumps(data),content_type='application/json')

        self.assertEqual(response.json(),{
            "message":{
                "msg":"password is not include special words.",
                "status": "SIGNUP_FAIL"
            }
        })