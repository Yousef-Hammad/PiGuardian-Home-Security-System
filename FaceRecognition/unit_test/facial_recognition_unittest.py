import unittest
from save_faces import encode_known_face
from compare_faces import retrieve_known_encodings, retrieve_known_names, encode_unknown_face, compare

class TestSaveFaces(unittest.TestCase):
    
    def test_encode_face(self):
        print("Testing Known Face Encoding")
        known_face_path = "/home/bisher/face_recog_test/known_faces/bisher1.jpg"
        self.assertTrue(encode_known_face(known_face_path))
        print("Known Face Encoding Test Passed")
    
    def test_retrieve_known_encodings(self):
        print("Testing Retrieving Encodings")
        self.assertTrue(retrieve_known_encodings())
        print("Retrieving Encodings Test Passed")
        
    def test_retrieve_known_names(self):
        print("Testing Retrieving Names")
        self.assertTrue(retrieve_known_names())
        print("Retrieving Names Test Passed")
    
    def test_encode_unknown_face(self):
        unknown_face_path = "/home/bisher/face_recog_test/known_faces/bisher1.jpg"
        print("Testing Unknown Face Encoding")
        self.assertIsNotNone(encode_unknown_face(unknown_face_path))
        print("Unknown Face Encoding Test Passed")
        
    def test_compare(self):
        print("Testing Comparision")
        test_face_path = "/home/bisher/face_recog_test/known_faces/bisher1.jpg"
        self.assertTrue(compare(test_face_path))
        print("Compare Test Passed")
            
        

if __name__ == '__main__':
    unittest.main()
