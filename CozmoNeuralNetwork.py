from numpy._distributor_init import NUMPY_MKL
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os

# Cozmo Neural Network Class for identifying situations in which
# other Cozmos are blocking its path
class CozmoNeuralNetwork :
	def __init__( self ) :
		rawImages = []
		features = []
		labels = []

		for i in range( 1, 1001 ) :
			# Get image
			path = "path/to/file/" + str( i ) + ".png";
			image = cv2.imread( path );

			# Get label
			label = True if i <= 500 else False;

			# Process Image
			pixels = self.image_to_feature_vector( image );
			hist = self.extract_color_histogram( image );

			# Update rawImages, features, and labels
			rawImages.append( pixels );
			features.append( hist );
			labels.append( label );

		# Convert rawImages, features, and labels to numpy array
		rawImages = np.array( rawImages );
		features = np.array( features );
		labels = np.array( labels );

		# Partition data into training and testing data
		( trainRI, testRI, trainRL, testRL ) = train_test_split( rawImages, labels, test_size = 0.25, random_state = 42 );
		( trainFeat, testFeat, trainLabels, testLabels ) = train_test_split( features, labels, test_size = 0.25, random_state = 42 );

		# Train neural network
		self.model = KNeighborsClassifier( n_neighbors = 5, n_jobs = -1 );
		self.model.fit( trainFeat, trainLabels );

	# Convert image to feature vector
	def image_to_feature_vector( self, image, size = ( 32, 32 ) ) :
		return cv2.resize( image, size ).flatten();

	# Get color histogram of image
	def extract_color_histogram( self, image, bins = ( 8, 8, 8 ) ) :
		hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV );
		hist = cv2.calcHist( [ hsv ], [ 0, 1, 2 ], None, bins, [ 0, 180, 0, 256, 0, 256 ] );

		if imutils.is_cv2():
			hist = cv2.normalize( hist );

		else:
			cv2.normalize( hist, hist );

		return hist.flatten()
