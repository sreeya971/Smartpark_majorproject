import unittest
import cv2
import numpy as np
import pickle
import os

# Import the modules to be tested
from SelectingROI import mouseClick
from carpark import checkParkingSpace

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a sample image with a white rectangle (parking space)
        self.img = np.ones((480, 640, 3), dtype=np.uint8) * 255
        self.img[100:148, 100:207] = [0, 0, 0]  # Create a black rectangle (parking space)
        
        # Save the sample image
        cv2.imwrite('sample_image.png', self.img)
        
        # Simulate mouse clicks to select ROI positions
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", mouseClick)
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        
        # Load selected ROI positions
        with open('CarParkPos', 'rb') as f:
            self.posList = pickle.load(f)
        
        # Load the sample video
        self.cap = cv2.VideoCapture('sample_video.mp4')
        
    def test_integration(self):
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
        
        # Delete the temporary files
        os.remove('sample_image.png')
        os.remove('CarParkPos')
        
if __name__ == '__main__':
    unittest.main()
