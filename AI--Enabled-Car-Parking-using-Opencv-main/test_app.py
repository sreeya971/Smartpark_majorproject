import unittest
import cv2
import numpy as np
import pickle

# Import the function to be tested
from carpark import checkParkingSpace

class TestCheckParkingSpace(unittest.TestCase):
    def setUp(self):
        # Load the video file
        self.cap = cv2.VideoCapture('carPark.mp4')
        
        # Load the parking space positions
        with open('CarParkPos', 'rb') as f:
            self.posList = pickle.load(f)
        
    def test_checkParkingSpace(self):
        # Iterate through the video frames
        while True:
            # Read frame from video feed
            success, frame = self.cap.read()
            
            # If no more frames, break the loop
            if not success:
                break
            
            # Preprocess the frame
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_blur = cv2.GaussianBlur(frame_gray, (3, 3), 1)
            frame_threshold = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY_INV, 25, 16)
            frame_median = cv2.medianBlur(frame_threshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            frame_dilate = cv2.dilate(frame_median, kernel, iterations=1)
            
            # Call the function to be tested
            output_frame = checkParkingSpace(frame_dilate)
            
            # Ensure that the output frame has correct dimensions
            self.assertEqual(output_frame.shape, frame.shape)
            
            # Add more assertions as needed
            
        # Release the video capture
        self.cap.release()
        
if __name__ == '__main__':
    unittest.main()
