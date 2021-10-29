import unittest
import os

from sfm.dataset import Dataset, VALID_EXTENSION

class TestDatset(unittest.TestCase):

    def test_create_dataset_with_none(self):
        with self.assertRaises(ValueError) as context:
            data = Dataset(None)
        self.assertEqual('image_dir Should Valid Directory or List of Images', str(context.exception))    

    def test_create_dataset_invalid_directory(self):
        with self.assertRaises(NotADirectoryError) as context:
            data = Dataset('/home/common/aravind/ashley/data/cleaned_datase')
        self.assertEqual('image_dir Should Valid Directory', str(context.exception))

    def test_create_dataset_valid_directory_no_image(self):
        with self.assertRaises(FileNotFoundError) as context:
            data = Dataset('/home/common/aravind/ashley/data/cleaned_dataset')
        self.assertEqual('image_dir Should Contain Images', str(context.exception))  

    def test_create_dataset_invalid_extension(self):
        img_dir = '/home/common/aravind/ashley/data/cleaned_dataset'
        images = [ os.path.join(img_dir, file) for file in os.listdir(img_dir)]
        with self.assertRaises(FileExistsError) as context:
            data = Dataset(images)
        self.assertEqual(f'Files Extension should be {VALID_EXTENSION}', str(context.exception))

    def test_create_dataset_with_file_not_exists(self):
        img_dir = '/home/common/aravind/ashley/data/cleaned_dataset'
        images = [ os.path.join(img_dir, file) for file in os.listdir(img_dir)]
        images.append( os.path.join(img_dir,'invalid.jpg'))
        with self.assertRaises(FileNotFoundError) as context:
            data = Dataset(images)
        self.assertEqual('All images Files should be Existing', str(context.exception))                









if __name__ == "__main__":
    unittest.main()
