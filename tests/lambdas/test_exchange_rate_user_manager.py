import unittest

import lambdas.exchange_rate_user_manager as man

class TestExchangeRateUserManager(unittest.TestCase):
  def test_users(self):
    res = man.lambda_handler({}, None)
    self.assertEqual(res, {"body": [{"username": "hi@bye.com"}], "status": 200})

  def test_user(self):
    res = man.lambda_handler({"username": "guo@guo.com", "method": "GET"}, None)
    self.assertEqual(res, {"body": {"username": "guo@guo.com"}, "status": 200})

if __name__=='__main__':
  unittest.main()