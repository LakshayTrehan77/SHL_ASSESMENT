from django.test import TestCase, Client

class MyTestCase(TestCase):
    def test_post_request(self):
        c = Client()
        response = c.post('/recommend', {'query': 'I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected response