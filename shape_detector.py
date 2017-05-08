# Group Members : John Atti, Mark Bonadies, Tomas Carino, Aayush Shrestha, & Amanda Steidl
# Project : Final Demo : Cozmo Driving Course
# Course : CMPS 367 Robotics
# Professor : Benjamin Fine
# Date : 05.01.2016
# Main Contributor(s) of File : Mark Bonadies, Tomas Carino
# Current File : shape_detector.py

import cv2;
import math;
import numpy as np;

# Determines if sign is a valid left triangle
def isValidLeftTriangle( hull ) :
    eps = 8;
    xeps = 6;

    if abs( hull[ 1 ][ 0 ] - hull[ 2 ][ 0 ] ) > xeps :
        return False;

    rxmid = int( ( hull[ 1 ][ 0 ] + hull[ 2 ][ 0 ] ) / 2 );
    rymid = int( ( hull[ 1 ][ 1 ] + hull[ 2 ][ 1 ] ) / 2 );

    if abs( hull[ 0 ][ 1 ] - rymid ) > eps :
        return False;

    dist1 = math.hypot( hull[ 0 ][ 0 ] - rxmid, hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    dist2 = math.hypot( hull[ 0 ][ 0 ] - rxmid, hull[ 0 ][ 1 ] - hull[ 2 ][ 1 ] );

    return abs( dist1 - dist2 ) <= eps;

# Determines if sign is a valid right triangle
def isValidRightTriangle( hull ) :
    eps = 8;
    xeps = 6;

    if abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] ) > xeps :
        return False;

    rxmid = int( ( hull[ 0 ][ 0 ] + hull[ 1 ][ 0 ] ) / 2 );
    rymid = int( ( hull[ 0 ][ 1 ] + hull[ 1 ][ 1 ] ) / 2 );

    if abs( hull[ 2 ][ 1 ] - rymid ) > eps :
        return False;

    dist1 = math.hypot( hull[ 2 ][ 0 ] - rxmid, hull[ 2 ][ 1 ] - hull[ 0 ][ 1 ] );
    dist2 = math.hypot( hull[ 2 ][ 0 ] - rxmid, hull[ 2 ][ 1 ] - hull[ 1 ][ 1 ] );

    return abs( dist1 - dist2 ) <= eps;

# Determines if sign is a square
def isValidSquare( hull ) :
    eps = 5;

    lx = abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] );
    rx = abs( hull[ 2 ][ 0 ] - hull[ 3 ][ 0 ] );

    ly = abs( hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    ry = abs( hull[ 2 ][ 1 ] - hull[ 3 ][ 1 ] );

    if abs( lx - rx ) > eps or abs( ly - ry ) > eps :
        return False;

    lxmid = int( ( hull[ 0 ][ 0 ] + hull[ 1 ][ 0 ] ) / 2 );
    rxmid = int( ( hull[ 2 ][ 0 ] + hull[ 3 ][ 0 ] ) / 2 );

    hull.sort( key = lambda x : x[ 1 ] );

    lymid = int( ( hull[ 0 ][ 1 ] + hull[ 1 ][ 1 ] ) / 2 );
    rymid = int( ( hull[ 2 ][ 1 ] + hull[ 3 ][ 1 ] ) / 2 );

    dx = abs( lxmid - rxmid );
    dy = abs( lymid - rymid );

    return abs( dx - dy ) <= eps;

# Determines if sign is a valid left pentagon
def isValidLeftPentagon( hull ) :
    eps = 4;

    lx = abs( hull[ 1 ][ 0 ] - hull[ 2 ][ 0 ] );
    rx = abs( hull[ 3 ][ 0 ] - hull[ 4 ][ 0 ] );

    ly = abs( hull[ 1 ][ 1 ] - hull[ 2 ][ 1 ] );
    ry = abs( hull[ 3 ][ 1 ] - hull[ 4 ][ 1 ] );

    ymid = ( hull[ 1 ][ 1 ] + hull[ 2 ][ 1 ] ) / 2;

    return abs( lx - rx ) <= eps and abs( ly - ry ) <= eps and abs( ymid - hull[ 0 ][ 1 ] ) < eps;

# Determines if sign is a valid right pentagon
def isValidRightPentagon( hull ) :
    eps = 4;

    lx = abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] );
    rx = abs( hull[ 2 ][ 0 ] - hull[ 3 ][ 0 ] );

    ly = abs( hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    ry = abs( hull[ 2 ][ 1 ] - hull[ 3 ][ 1 ] );

    ymid = ( hull[ 2 ][ 1 ] + hull[ 3 ][ 1 ] ) / 2;

    return abs( lx - rx ) <= eps and abs( ly - ry ) <= eps and abs( ymid - hull[ 4 ][ 1 ] ) < eps;

# Convert the convex hull points to a list
def hullToList( hull ) :
    return [ ( vertex[ 0 ][ 0 ], vertex[ 0 ][ 1 ] ) for vertex in hull ];

# Calculate the distance to a given contour using the Triangle Similarity Theorem
def distanceFromHull( width, shape ) :
    knownWidth, focalLength = distanceConstants[ shape ];

    return 25.4 * knownWidth * focalLength / width;

# Calculate the width of the square
def getWidthSquare( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );
    rx = int( ( sign[ 2 ][ 0 ] + sign[ 3 ][ 0 ] ) / 2 );

    return rx - lx;

# Calculate the width of the left pentagon
def getWidthLeftPentagon( sign ) :
    rx = int( ( sign[ 3 ][ 0 ] + sign[ 4 ][ 0 ] ) / 2 );

    return rx - sign[ 0 ][ 0 ];

# Calculate the width of the right pentagon
def getWidthRightPentagon( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );

    return sign[ 4 ][ 0 ] - lx;

# Calculate the width of the left triangle
def getWidthLeftTriangle( sign ) :
    rx = int( ( sign[ 1 ][ 0 ] + sign[ 2 ][ 0 ] ) / 2 );

    return rx - sign[ 0 ][ 0 ];

# Calculate the width of the right triangle
def getWidthRightTriangle( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );

    return sign[ 2 ][ 0 ] - lx;

# Calculate the width of the hexagon
def getWidthHexagon( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );
    rx = int( ( sign[ 4 ][ 0 ] + sign[ 5 ][ 0 ] ) / 2 );

    return rx - lx;

# Calculate the width of the octagon
def getWidthOctagon( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );
    rx = int( ( sign[ 6 ][ 0 ] + sign[ 7 ][ 0 ] ) / 2 );

    return rx - lx;

# Find the distance to all valid signs in the image using noise reduction methods,
# Convex Hull generation, Euclidean Geometry, and the Pinhole Camera Model
def getSignReadings( img ) :
    # Reduce noise in the image
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY );

    blur = cv2.blur( gray, ( 3, 5 ) );
    blurInvert = ( 255 - blur );

    lower = np.array( [ 235 ] );
    upper = np.array( [ 255 ] );

    shapeMask = cv2.inRange( blurInvert, lower, upper );
    masked = cv2.bitwise_and( blurInvert, blurInvert, mask = shapeMask );
    maskedInvert = cv2.bitwise_not( masked );

    ret, thresh = cv2.threshold( maskedInvert, 35, 255, 1 );
    contourImg, contours, hierarchy = cv2.findContours( thresh, 1, 2 );

    # Store signs in "signs" list
    signs = [];

    for contour in contours :
        contourVertices = cv2.approxPolyDP( contour, 0.03 * cv2.arcLength( contour, True ), True );
        hullVertices = cv2.convexHull( contourVertices );

        # If the contour is not its own convex hull, discard it
        if len( contourVertices ) != len( hullVertices ) :
            continue;

        # If the contour is too small, discard it
        if cv2.contourArea( hullVertices ) < 300 :
            continue;

        # Sort the contour's points based on their x-coordinate
        hull = hullToList( hullVertices );
        hull.sort();
        sides = len( hull );

        # Check if contour corresponds to an optional left turn
        if sides == 3 and isValidLeftTriangle( hull ) :
            shape = "triangle left";
            
            hull.sort();
            widthHull = getWidthLeftTriangle( hull );

        # Check if contour corresponds to a optional right turn
        elif sides == 3 and isValidRightTriangle( hull ) :
            shape = "triangle right";
            
            hull.sort();
            widthHull = getWidthRightTriangle( hull );

        # Check if contour corresponds to a speed up sign
        elif sides == 4 and isValidSquare( hull ) :
            shape = "square";
            
            hull.sort();
            widthHull = getWidthSquare( hull );

        # Check if contour corresponds to a mandatory left turn
        elif sides == 5 and isValidLeftPentagon( hull ) :
            shape = "pentagon left";
            
            hull.sort();
            widthHull = getWidthLeftPentagon( hull );

        # Check if contour corresponds to a mandatory right turn
        elif sides == 5 and isValidRightPentagon( hull ) :
            shape = "pentagon right";
            
            hull.sort();
            widthHull = getWidthRightPentagon( hull );

        # Check if contour corresponds to a slow down
        elif sides == 6 :
            shape = "hexagon";

            hull.sort();
            widthHull = getWidthHexagon();

        # Check if contour corresponds to a stop sign
        elif sides == 8 :
            shape = "octagon";
            
            hull.sort();
            widthHull = getWidthOctagon( hull );

        # If the contour does not correspond to a valid sign, discard it
        else :
            continue;

        # Calculate distance to sign and append to "signs"
        distance = distanceFromHull( widthHull, shape );
        signs.append( ( shape, distance ) );

    return signs;

# Constants for calculating distance to signs
distanceConstants = {'hexagon': (4, 85.5), 'square': (1, 264.0), 'pentagon left': (4, 136.5), 'triangle right': (5, 75.599999999999994), 'pentagon right': (4, 135.0), 'octagon': (4, 109.5), 'triangle left': (5, 76.799999999999997)}

# Driver Code
if __name__ == "__main__" :
    for i in range( 0, 20 ):
        print( "----------" );
        name = 'Hexagon6_' + str(i) + '.png'
        img = cv2.imread( name );

        signReadings = getSignReadings( img );
        print( signReadings );        
        cv2.imshow( "image", img );
        cv2.waitKey();
