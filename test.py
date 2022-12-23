import unittest
import check

class TestBot(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
  def setUp(self):
    pass
  #Each test method starts with the keyword test_
  def test_SMA(self):
    self.assertEqual(check.SMA('fortest.txt', 10), 34)
  def test_priceread(self):
    self.assertEqual(check.price_read('fortest.txt', 3, 0), [5.000, 10.000, 15.000])
  def test_sig_macd(self):
    self.assertEqual(check.SIG_MACD('fortest.txt'), 32.22222222222222)
    '''
  def test_divide(self):
    self.assertEqual(self.calculator.divide(10,5), 5)'''
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
