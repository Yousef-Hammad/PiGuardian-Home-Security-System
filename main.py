import unittest


if __name__ == '__main__':
    test_suite = unittest.TestLoader().discover('api', pattern='unit_test.py')
    test_suite1 = unittest.TestLoader().discover('person_detection', pattern='person_detection_test.py')
    test_suite2 = unittest.TestLoader().discover('person_detection', pattern='lighting_control_test.py')
    #test_suite3 = unittest.TestLoader().discover('FaceRecognition/unit_test', pattern='facial_recognition_unit_test.py')
    
    unittest.TextTestRunner().run(test_suite)
    unittest.TextTestRunner().run(test_suite1)
    unittest.TextTestRunner().run(test_suite2)
    #unittest.TextTestRunner().run(test_suite3)
