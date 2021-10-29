import unittest
import os
from random import shuffle

from sfm.dataset import Dataset, VALID_EXTENSION

imageDir = '/home/common/aravind/ashley/data/cleaned_dataset'
imageDir1 = '/mnt/sfm/SfM_quality_evaluation/Benchmarking_Camera_Calibration_2008/Herz-Jesus-P25/images'

class TestDatsetInstantiation(unittest.TestCase):

    def test_create_dataset_with_none(self):
        with self.assertRaises(ValueError) as context:
            data = Dataset(None)
        self.assertEqual('image_dir Should Valid Directory or List of Images', str(context.exception))    

    def test_create_dataset_invalid_directory(self):
        invalidDir=os.path.join(imageDir,'invalidDir')
        with self.assertRaises(NotADirectoryError) as context:
            data = Dataset(invalidDir)
        self.assertEqual('image_dir Should Valid Directory', str(context.exception))

    def test_create_dataset_valid_directory_no_image(self):
        with self.assertRaises(FileNotFoundError) as context:
            data = Dataset(imageDir)
        self.assertEqual('image_dir Should Contain Images', str(context.exception))  

    def test_create_dataset_invalid_file_extension(self):
        images = [ os.path.join(imageDir, file) for file in os.listdir(imageDir)]
        with self.assertRaises(FileExistsError) as context:
            data = Dataset(images)
        self.assertEqual(f'Files Extension should be {VALID_EXTENSION}', str(context.exception))

    def test_create_dataset_with_file_not_exists(self):
        images = [ os.path.join(imageDir, file) for file in os.listdir(imageDir)]
        images.append( os.path.join(imageDir,'invalid.jpg'))
        with self.assertRaises(FileNotFoundError) as context:
            data = Dataset(images)
        self.assertEqual('All images Files should be Existing', str(context.exception))     

    def test_create_dataset_with_invalid_extesion(self):
        with self.assertRaises(ValueError) as context:
            data = Dataset(imageDir, 'csv')
        self.assertEqual('extension is not Valid', str(context.exception))   

    def test_create_dataset_with_invalid_extesion_list(self):
        with self.assertRaises(ValueError) as context:
            data = Dataset(imageDir, ['csv', 'obj', 'jpg'])
        self.assertEqual('extension is not Valid', str(context.exception)) 


class TestDatsetObject(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.dataset =  Dataset(imageDir1)

    def teardown(self):
        self.dataset = None  

    def test_length(self):
        images = [ file for file in os.listdir(imageDir1) if os.path.basename(file).split('.')[1] in VALID_EXTENSION]
        self.assertEqual(len(self.dataset), len(images))

    def test_getItem(self):
        allFilesvalid = all([os.path.exists(self.dataset[i]) for i in range(len(self.dataset))])
        self.assertEqual(allFilesvalid, True)

    def test_sorted(self):
        self.assertFalse(self.dataset.sorted)  
        images = [ file for file in os.listdir(imageDir1) if os.path.basename(file).split('.')[1] in VALID_EXTENSION]
        images = [ os.path.join(imageDir1,file) for file in images]
        shuffle((images))
        sortFunction = lambda x : int(os.path.basename(x).split('.')[0])   
        images.sort(key=sortFunction)
        self.dataset.sortImages(sortFunction)
        self.assertListEqual(images,self.dataset.getImagesList)
        self.assertTrue(self.dataset.sorted) 
        

   






if __name__ == "__main__":
    unittest.main()
