import unittest
from nowstagram import app


class NowstagramTest(unittest.TestCase):
    """docstring for N"""

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # def setUpClass(cls):
    #     print('setupclass')

    def tearDown(self):
        print('teardown')

    # def tearDownClass(cls):
    #     print('tearDownClass')
    def register(self, username, password):
        return self.app.post('/reg', data={'username': username, 'password': password}, follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_login_logout(self):
        self.assertEqual(self.register('helloooo', 'world').status_code, 200)
        # status_code = self.register('hello', 'world').status
        # assert status_code == '200' + ' ' + 'OK'
        self.assertEqual(self.app.get('/profile/109').status_code, 200)
        # assert '-hello' in self.app.open('/').data
        self.logout()
        # assert '-hello' not in self.app.open('/').data
        self.assertEqual(self.app.get('/profile/109').status_code, 302)
        self.login('helloooo', 'world')
        # assert '-hello' in self.app.open('/').data
        self.assertEqual(self.app.get('/profile/109').status_code, 200)


if __name__ == '__main__':
    unittest.main()
