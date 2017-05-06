from numpy._distributor_init import NUMPY_MKL
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os

class CozmoNeuralNet :
	def __init__( self ) :
		print("TOMAS IS ALIVE")
		rawImages = []
		features = []
		labels = []

		for i in range( 1, 1001 ) : #1001
			number = str( i );
			if i <= 500 : #500
				label = True;

			else :
				label = False;

			# Update path as needed
			path = "C:\\Users\Amandas\Desktop\OpenCV\Examples\cozmo-python-sdk\cozmoDrives\Team-Awsomesauce\Training_Data\\train" + number + ".png";
			image = cv2.imread( path );

			pixels = self.image_to_feature_vector(image)
			hist = self.extract_color_histogram(image)

			# update the raw images, features, and labels matricies,
			# respectively
			rawImages.append(pixels)
			features.append(hist)
			labels.append(label)

		# show some information on the memory consumed by the raw images
		# matrix and features matrix
		rawImages = np.array(rawImages)
		features = np.array(features)
		labels = np.array(labels)

		# partition the data into training and testing splits, using 75%
		# of the data for training and the remaining 25% for testing
		(trainRI, testRI, trainRL, testRL) = train_test_split(
			rawImages, labels, test_size=0.25, random_state=42)
		(trainFeat, testFeat, trainLabels, testLabels) = train_test_split(
			features, labels, test_size=0.25, random_state=42)

		# train and evaluate a k-NN classifer on the histogram
		# representations
		print("[INFO] evaluating histogram accuracy...")
		self.model = KNeighborsClassifier(n_neighbors=10,
			n_jobs=-1)
		self.model.fit(trainFeat, trainLabels)
		acc = self.model.score(testFeat, testLabels)
		print("[INFO] histogram accuracy: {:.2f}%".format(acc * 100))

	def image_to_feature_vector(self, image, size=(32, 32)):
		return cv2.resize(image, size).flatten()

	def extract_color_histogram(self, image, bins=(8, 8, 8)):
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		hist = cv2.calcHist([hsv], [0, 1, 2], None, bins,
			[0, 180, 0, 256, 0, 256])

		if imutils.is_cv2():
			hist = cv2.normalize(hist)

		else:
			cv2.normalize(hist, hist)

		return hist.flatten()




# if __name__ == "__main__" :
# 	cnn = CozmoNeuralNet();
#
# 	for i in range( 1, 30 ) :
# 		path = "C:\\Users\Amandas\Desktop\OpenCV\Examples\cozmo-python-sdk\cozmoDrives\Team-Awsomesauce\Test Data\\test" + str( i ) + ".png";
# 		image = cv2.imread( path );
#
# 		hist = cnn.extract_color_histogram(image)
# 		result = cnn.model.predict( [hist] )[ 0 ]
#
# 		print( "result", i, ":", result );
#
# 		cv2.imshow( "sample", image );
# 		cv2.waitKey();
