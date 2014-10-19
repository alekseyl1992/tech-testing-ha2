#!/usr/bin/env python2

import sys
import unittest
from tests.test_suite import TestSuite


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(TestSuite),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
