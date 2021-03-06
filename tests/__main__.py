import sys
import unittest

if __name__ == '__main__':
    all_tests = unittest.TestLoader().discover('./', pattern='*_tests.py')
    ret = unittest.TextTestRunner().run(all_tests)
    sys.exit(not ret.wasSuccessful())
