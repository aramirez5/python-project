import unittest
import sys
from flask import Flask
from flask_testing import TestCase
sys.path.append("..")

from todo import app

class AppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = self.app.test_client()
        self.tasks = []

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    def test_add_task(self):
        response = self.client.post('/add', data={'task': 'Task 1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0], 'Task 1')

    def test_add_existing_task(self):
        self.tasks.append('Task 1')
        response = self.client.post('/add', data={'task': 'Task 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.tasks), 1)
        self.assertIn('La tarea "Task 1" ya existe.', response.get_data(as_text=True))

    def test_delete_task(self):
        self.tasks.append('Task 1')
        response = self.client.post('/delete', data={'task': 'Task 1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.tasks), 0)

    def test_delete_nonexistent_task(self):
        response = self.client.post('/delete', data={'task': 'Task 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.tasks), 0)
        self.assertIn('La tarea "Task 1" no existe.', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
