from django.test import TestCase
from django.test import Client

# Create your tests here.
'''
class TextRoutes(TestCase):
    def test_home(self):
        self.client=Client()
         # Issue a GET request.
        response = self.client.get('/site/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200,"Couldn't access index site.")
        response=self.client.get("/site/blog/")
        self.assertEqual(response.status_code,200,"Couldn't access blog site!")
        response=self.client.get("/site/projects/")
        self.assertEqual(response.status_code,200,"Couldn't access blog projects!")
        response=self.client.get("/site/comments/")
        self.assertEqual(response.status_code,200,"Couldn't access blog comments!")

        #test writing as not logged in user
        response = self.client.post("/site/comments/",{"comment_text":"comment send by automated test."})
        self.assertEqual(response.status_code,200,"Couldn't send comment as not logged in user")'''