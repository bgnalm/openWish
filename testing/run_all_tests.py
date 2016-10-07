import argparse
import sys

from general_tests.general_unit_tests import GeneralTests
from create_user_tests.create_user_unit_tests import CreateUserTests
from add_wish_tests.add_wish_unit_tests import AddWishTests
from read_wish_tests.read_wish_unit_tests import ReadWishTests
from rate_wish_tests.rate_wish_unit_tests import RateWishTests
from get_wishes_tests.get_wishes_unit_tests import GetWishesTests
from get_wish_tesets.get_wish_unit_tests import GetWishTests

import open_wish_api

import unittest

if __name__ == '__main__':
	for arg in sys.argv:
		if arg == '-v':
			open_wish_api.VERBOSE = True
			
	unittest.main()