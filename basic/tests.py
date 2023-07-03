import os

from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings

TEST_FOLDER_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'test_folder')


@override_settings(BASE_FILE_OPERATIONS_FOLDER=TEST_FOLDER_PATH)
class BasicTestCase(TestCase):
    def setUp(self):
        self.base_folder = TEST_FOLDER_PATH
        self.file_path = os.path.join(self.base_folder, 'test_file.txt')
        self.file_path_2 = os.path.join(self.base_folder, 'test_file_2.csv')
        os.makedirs(self.base_folder, exist_ok=True)
        with open(self.file_path, 'w') as file:
            file.write('Test content')
        with open(self.file_path_2, 'w') as file:
            file.write('1,2')

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        if os.path.exists(self.file_path_2):
            os.remove(self.file_path_2)

        os.rmdir(self.base_folder)

    def test_search_files_basic(self):
        response = self.client.get(reverse('search_files'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('filepaths', data)
        file_paths = data['filepaths']
        self.assertEqual(len(file_paths), 2)
        self.assertEqual(file_paths[0], os.path.relpath(
            self.file_path, self.base_folder))
        self.assertEqual(file_paths[1], os.path.relpath(
            self.file_path_2, self.base_folder))

    def test_search_files_with_wildcard(self):
        response = self.client.get(
            reverse('search_files'), {'wildcard': '*.txt'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('filepaths', data)
        file_paths = data['filepaths']
        self.assertEqual(len(file_paths), 1)
        self.assertEqual(file_paths[0], os.path.relpath(
            self.file_path, self.base_folder))

    def test_download_files(self):
        response = self.client.get(reverse('download_files'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename="downloaded_files.zip"')

    def test_download_files_which_do_not_exist(self):
        response = self.client.get(
            reverse('download_files'), {'wildcard': '*.jpg'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)

    def test_move_file(self):
        source_path = 'test_file.txt'
        destination_path = 'new_folder/test_file.txt'
        url = reverse('move_file')
        data = {'source_path': source_path,
                'destination_path': destination_path}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(os.path.exists(self.file_path))

        new_folder_path = os.path.join(self.base_folder, 'new_folder')
        new_file_path = os.path.join(new_folder_path, 'test_file.txt')

        self.assertTrue(os.path.exists(new_file_path))

        os.remove(new_file_path)
        os.rmdir(new_folder_path)

    def test_move_file_with_invalid_source_path(self):
        source_path = 'test_file_2.txt'
        destination_path = 'new_folder/test_file.txt'
        url = reverse('move_file')
        data = {'source_path': source_path,
                'destination_path': destination_path}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_move_file_with_invalid_destination_path(self):
        source_path = 'test_file_2.txt'
        destination_path = 'new_folder'
        url = reverse('move_file')
        data = {'source_path': source_path,
                'destination_path': destination_path}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
