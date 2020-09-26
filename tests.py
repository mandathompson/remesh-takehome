from app import app
from unittest import TestCase



class postsRoutesTestCase(TestCase):
    def test_index(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form method="post">', html)

    def test_new(self):
        with app.test_client() as client:
            response = client.get('/post/new', data={'form.title': 'test'})
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<div class="form-group">', html)


    # In the interest of not spending too much (more!) time on this, I have not yet experienced testing with wtforms, but 
    # did research a bit and found this post, which I would use as a starting point to do so.             
        # https://stackoverflow.com/questions/37579411/testing-a-post-that-uses-flask-wtf-validate-on-submit

    # I have also not experienced testing routes with dynamic data, like post.id before. Again, this is something that 
    # I will definitely spend the next few days looking into, but for this takehome project I know that time spent 
    # is an issue. I would be happy to receive any resources y'all may have about testing dynamic data in flask though.