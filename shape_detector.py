import cv2;
from copy import deepcopy;
import numpy as np;

def isLeftPentagon( hull ) :
    eps = 4;

    lx = abs( hull[ 1 ][ 0 ] - hull[ 2 ][ 0 ] );
    rx = abs( hull[ 3 ][ 0 ] - hull[ 4 ][ 0 ] );

    ly = abs( hull[ 1 ][ 1 ] - hull[ 2 ][ 1 ] );
    ry = abs( hull[ 3 ][ 1 ] - hull[ 4 ][ 1 ] );

    ymid = ( hull[ 1 ][ 1 ] + hull[ 2 ][ 1 ] ) / 2;

    # print( "LEFT:", lx, rx, ly, ry, ymid );

    return abs( lx - rx ) <= eps and abs( ly - ry ) <= eps and abs( ymid - hull[ 0 ][ 1 ] ) < eps;

def isRightPentagon( hull ) :
    eps = 4;

    lx = abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] );
    rx = abs( hull[ 2 ][ 0 ] - hull[ 3 ][ 0 ] );

    ly = abs( hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    ry = abs( hull[ 2 ][ 1 ] - hull[ 3 ][ 1 ] );

    ymid = ( hull[ 2 ][ 1 ] + hull[ 3 ][ 1 ] ) / 2;

    # print( "RIGHT:", lx, rx, ly, ry, ymid );

    return abs( lx - rx ) <= eps and abs( ly - ry ) <= eps and abs( ymid - hull[ 4 ][ 1 ] ) < eps;

def isValidPentagon( hull ) :
    # print( hull );
    hull.sort();
    # print( hull );

    if isLeftPentagon( hull ) :    
        print( "Left Pentagon!" );
        return True;

    if isRightPentagon( hull ) :
        print( "Right Pentagon!" );
        return True;

    return False;

def hullToList( hull ) :
    return [ ( vertex[ 0 ][ 0 ], vertex[ 0 ][ 1 ] ) for vertex in hull ];

def getSignReadings( img ) :
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY );

    blur = cv2.blur( gray, ( 3, 5 ) );
    blurInvert = ( 255 - blur );

    lower = np.array( [ 235 ] );
    upper = np.array( [ 255 ] );

    shapeMask = cv2.inRange( blurInvert, lower, upper );
    masked = cv2.bitwise_and( blurInvert, blurInvert, mask = shapeMask );
    maskedInvert = cv2.bitwise_not( masked );

    ret, thresh = cv2.threshold( maskedInvert, 35, 255, 1 );
    cv2.imshow( "aksjdksja", thresh );
    contourImg, contours, hierarchy = cv2.findContours( thresh, 1, 2 );

    signs = [];

    for contour in contours :
        if cv2.contourArea( contour ) < 300 :
            continue;

        contourVertices = cv2.approxPolyDP( contour, 0.03 * cv2.arcLength( contour, True ), True );
        hullVertices = cv2.convexHull( contourVertices );

        if len( contourVertices ) != len( hullVertices ) :
            continue;

        sides = len( hullVertices );

        if sides == 3 :
            cv2.drawContours( img, [ hullVertices ], 0, ( 0, 255, 0 ), -1)
            signs.append( "triangle" );

        elif sides == 4 :
            cv2.drawContours( img, [ hullVertices ], 0, ( 0, 0, 255 ), 3 );
            signs.append( "square" );

        elif sides == 5 and isValidPentagon( hullToList( hullVertices ) ) :
            cv2.drawContours( img, [ hullVertices ], 0, 255, -1 );
            signs.append( "pentagon" );

        elif sides == 8 :
            cv2.drawContours( img, [ hullVertices ], 0, ( 0, 0, 255 ), 3 );
            signs.append( "octagon" );

        elif sides >= 15 :
            cv2.drawContours( img, [ hullVertices ], 0, ( 0, 255, 255 ), 3 );
            signs.append( "circle" );


    print( signs );
    cv2.imshow( "text", img );
    cv2.waitKey();

    return signs;

# Driver Code
if __name__ == "__main__" :
    for i in range( 20 ):
        print( "----------" );
        name = 'backRoad' + str(i) + '.png'
        img = cv2.imread( name );
        
        signReadings = getSignReadings( img );