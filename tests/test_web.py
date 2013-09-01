#!/usr/bin/env python
#
#  Test the database model.

import sys
sys.path.append('..')
sys.path.append('../lib')

import unittest

from bottledbwrap import dbwrap
import website
import model


class Test(unittest.TestCase):
	def setUp(self):
		dbwrap.connect(connect='sqlite:///:memory:')
		dbwrap.Base.metadata.create_all()

		db = dbwrap.session()
		model.create_sample_data()
		self.db = db

		from webtest import TestApp
		from bottle import TEMPLATE_PATH
		TEMPLATE_PATH.insert(0, '../views')
		self.app = website.web_interface()
		self.harness = TestApp(self.app)

	def test_index_wsgi(self):
		'''Test of Index page.'''

		results = self.harness.get('/')
		self.assertEqual(results.status, '200 OK')
		self.assertIn('User List', results.body)

	def test_user_list(self):
		'''Test the user list page.'''

		results = self.harness.get('/users')
		self.assertEqual(results.status, '200 OK')
		self.assertIn('users/sean', results.body)

	def test_user_create(self):
		'''Create new user via WSGI interface'''

		results = self.harness.get('/new-user')
		self.assertEqual(results.status, '200 OK')

		results = self.harness.post(
				'/new-user',
				{'name': 'cray',
					'full_name': 'Seymour Cray',
					'email_address': 'cray@example.com',
					'password': 'mycray',
					'confirm': 'mycray',
					})
		self.assertEqual(results.status, '302 Found')
		self.assertTrue(results.location.endswith('users/cray'))

		cray = model.user_by_name('cray')
		self.assertNotEqual(cray, None)

		results = self.harness.get('/users/cray')
		self.assertEqual(results.status, '200 OK')
		self.assertIn('Seymour', results.body)


if __name__ == '__main__':
	print unittest.main()