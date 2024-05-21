import person_detection as pd
import unittest
from unittest.mock import patch, MagicMock, mock_open

class TestPersonDetection(unittest.TestCase):
    def test_ReadLabelFile(self):
        # Create a temporary label file for testing
        with open('temp_label_file.txt', 'w') as f:
            f.write('0 label_0\n1 label_1')
        labels = pd.ReadLabelFile('temp_label_file.txt')
        self.assertEqual(labels, {0: 'label_0', 1: 'label_1'})
        print("Read Label File test passed")
      
    # Create mock object for drawing rectangle
    @patch('cv2.rectangle')
    @patch('person_detection.MappedArray')
    
    def test_DrawRectangles(self, mock_mapped_array, mock_rectangle):
        pd.rectangles = [[10, 20, 30, 40], [50, 60, 70, 80]]
        request = MagicMock()
        
        mock_array_instance = MagicMock()
        mock_array_instance.array.shape = (480, 640, 3)  # Example shape
        mock_mapped_array.return_value.__enter__.return_value = mock_array_instance
    
        pd.DrawRectangles(request)
        # Checks if cv2.rectangle was called exactly twice which matches the number of rectangles in the pd.rectangles list
        self.assertEqual(mock_rectangle.call_count, 2)
        print("draw rectangles test passed")
    
    @patch('tflite_runtime.interpreter.Interpreter')
    @patch('cv2.cvtColor')
    @patch('cv2.resize')
    @patch('builtins.open', mock_open(read_data='0 label_0\n1 label_1'))  # Mocking open here
    def test_InferenceTensorFlow(self, mock_resize, mock_cvtColor, mock_interpreter):
        # Mocking the external calls made within InferenceTensorFlow
        mock_interpreter.return_value.get_input_details.return_value = [{'shape': [1, 300, 300, 3], 'dtype': 'uint8', 'index': 0}]
        mock_interpreter.return_value.get_output_details.return_value = [{'index': 0}, {'index': 1}, {'index': 2}, {'index': 3}]
        mock_interpreter.return_value.allocate_tensors.return_value = None
        mock_interpreter.return_value.set_tensor.return_value = None
        mock_interpreter.return_value.invoke.return_value = None
        mock_interpreter.return_value.get_tensor.side_effect = [
            [[[10, 20, 30, 40]]], # detected_boxes
            [[1]], # detected_classes
            [[0.9]], # detected_scores
            1 # num_boxes
        ]
        image = MagicMock()
        image.shape = (480, 640, 3)
        mock_cvtColor.return_value = image
        pd.InferenceTensorFlow(image, 'model.tflite', 'labels.txt', 'output_location')
        # Assert if rectangles were populated based on mock inference output
        self.assertTrue(len(pd.rectangles) > 0)
        print("inference tensor flow test passed")

    @patch('person_detection.camera.stop_preview')
    @patch('person_detection.camera.start_and_record_video')
    def test_capture_video(self, mock_start_and_record_video, mock_stop_preview):
        test_video_file = 'Tests/test.mp4'
        
        # Verify that the code quits
        with self.assertRaises(SystemExit):
            pd.capture_video(test_video_file)
        
        mock_start_and_record_video.assert_called_once_with(test_video_file, duration=5)
        mock_stop_preview.assert_called_once()
        print("capture video test passed")

if __name__ == '__main__':
    unittest.main()
