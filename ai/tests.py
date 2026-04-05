from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
import json

class AIChatAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('chat_api')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_method_not_allowed(self):
        # GET should return 405
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_invalid_json(self):
        # Invalid JSON body
        response = self.client.post(self.url, data="not json", content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('ai.views.OpenAI')
    @patch('ai.views.os.environ.get')
    def test_successful_anonymous_chat(self, mock_env, mock_openai):
        # Setup mock env and openai return
        mock_env.return_value = 'fake_key'
        mock_instance = mock_openai.return_value
        mock_instance.chat.completions.create.return_value.choices = [
            type('Choice', (object,), {'message': type('Message', (object,), {'content': 'Mocked answer'})()})()
        ]
        mock_instance.chat.completions.create.return_value.usage = type('Usage', (object,), {'total_tokens': 100})()

        data = {
            'messages': [{'role': 'user', 'content': 'hello'}]
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        json_resp = response.json()
        self.assertEqual(json_resp['content'], 'Mocked answer')
        self.assertEqual(json_resp['tokens_used'], 100)
        # Should be 5000 - 100
        self.assertEqual(json_resp['remaining_tokens'], 4900)

    @patch('ai.views.OpenAI')
    @patch('ai.views.os.environ.get')
    def test_successful_registered_chat(self, mock_env, mock_openai):
        self.client.login(username='testuser', password='password123')
        
        mock_env.return_value = 'fake_key'
        mock_instance = mock_openai.return_value
        mock_instance.chat.completions.create.return_value.choices = [
            type('Choice', (object,), {'message': type('Message', (object,), {'content': 'Authenticated mock answer'})()})()
        ]
        mock_instance.chat.completions.create.return_value.usage = type('Usage', (object,), {'total_tokens': 500})()

        data = {
            'messages': [{'role': 'user', 'content': 'hello authenticated'}]
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        json_resp = response.json()
        self.assertEqual(json_resp['content'], 'Authenticated mock answer')
        self.assertEqual(json_resp['tokens_used'], 500)
        # Auth users get 50000 limit, so 50000 - 500 = 49500
        self.assertEqual(json_resp['remaining_tokens'], 49500)
