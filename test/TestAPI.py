import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Thiết lập trước mỗi test case
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        # Dọn dẹp sau mỗi test case
        pass

    def test_home_endpoint(self):
        # Kiểm tra endpoint "/"
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello World!', response.data)

    def test_search_without_keyword(self):
        # Kiểm tra endpoint /search với keyword rỗng
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Keyword is required', response.data)

    def test_search_with_keyword(self):
        # Kiểm tra endpoint /search với keyword không rỗng
        response = self.client.get('/search?keyword=test')
        self.assertEqual(response.status_code, 200)
        # Kiểm tra nội dung trả về bao gồm 'google' và 'coccoc'
        self.assertIn(b'google', response.data)
        self.assertIn(b'coccoc', response.data)

if __name__ == '__main__':
    unittest.main()