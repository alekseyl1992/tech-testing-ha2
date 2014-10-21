#!/usr/bin/env python2

import sys
import unittest
from tests.restriction_suite import RestrictionSuite


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(RestrictionSuite),
        #unittest.makeSuite(WorkTimeSuite),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
