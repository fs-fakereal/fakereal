import unittest

import models.loader as loader

class TestModel(unittest.TestCase):
    true_img_paths = []
    fake_img_paths = []

    def test_loader_noimg(self):
        pred, err = loader.model_generate_prediction('')

        self.assertGreaterEqual(err, 1.0, 'Model loader did not throw error')

    def test_loader_default(self):
        img_path = ''
        pred, err = loader.model_generate_prediction(img_path)

        self.assertEqual(err, 0, 'Model loader failed to predict')
        self.assertGreaterEqual(pred, 0.0, 'Model prediction is invalid')
        self.assertLessEqual(pred, 1.0, 'Model prediction is invalid')


    def test_loader_genai(self):
        # sanity check
        img_path = ''
        pred, err = loader.model_generate_prediction(img_path, 'genai')

        self.assertEqual(err, 0, 'Model loader failed to predict')
        self.assertGreaterEqual(pred, 0.0, 'Model prediction is invalid')
        self.assertLessEqual(pred, 1.0, 'Model prediction is invalid')

    def test_loader_vgg16(self):
        img_path = ''
        pred, err = loader.model_generate_prediction(img_path, 'vgg16')

        self.assertEqual(err, 0, 'Model loader failed to predict')
        self.assertGreaterEqual(pred, 0.0, 'Model prediction is invalid')
        self.assertLessEqual(pred, 1.0, 'Model prediction is invalid')

    def test_loader_mobilenetv3small(self):
        img_path = ''
        pred, err = loader.model_generate_prediction(img_path, 'mobilenetv3small')

        self.assertEqual(err, 0, 'Model loader failed to predict')
        self.assertGreaterEqual(pred, 0.0, 'Model prediction is invalid')
        self.assertLessEqual(pred, 1.0, 'Model prediction is invalid')

    def test_accuracy_truth_genai(self):
        for path in self.true_img_paths:
            pred, err = loader.model_generate_prediction(path, 'genai')

            self.assertEqual(err, 0, 'Model loader failed to predict img')
            self.assertGreaterEqual(pred, 0.5, "Predicted True when actually False")

    def test_accuracy_fake_genai(self):
        for path in self.fake_img_paths:
            pred, err = loader.model_generate_prediction(path, 'genai')
            self.assertEqual(err, 0, 'Model loader failed to predict img')
            self.assertLess(pred, 0.5, "Predicted False when actually True")

    def test_accuracy_truth_vgg16(self):
        for path in self.true_img_paths:
            pred, err = loader.model_generate_prediction(path, 'vgg16')

            self.assertEqual(err, 0, 'Model loader failed to predict img')
            self.assertGreaterEqual(pred, 0.5, "Predicted True when actually False")

    def test_accuracy_fake_vgg16(self):
        for path in self.fake_img_paths:
            pred, err = loader.model_generate_prediction(path, 'vgg16')
            self.assertEqual(err, 0, 'Model loader failed to predict img')
            self.assertLess(pred, 0.5, "Predicted False when actually True")

    def test_accuracy_truth_mobilenetv3small(self):
        for path in self.true_img_paths:
            pred, err = loader.model_generate_prediction(path, 'mobilenetv3small')

            self.assertEqual(err, 0, 'Model loader failed to predict img')
            self.assertGreaterEqual(pred, 0.5, "Predicted True when actually False")

    def test_accuracy_fake_mobilenetv3small(self):
        for path in self.fake_img_paths:
            pred, err = loader.model_generate_prediction(path, 'mobilenetv3small')
            self.assertEqual(err, 0, 'Model loader failed to predict img')
            self.assertLess(pred, 0.5, "Predicted False when actually True")

if __name__ == '__main__':
    unittest.main()

