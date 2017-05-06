import cv2;
import math;
import numpy as np;

def isValidLeftTriangle( hull ) :
    eps = 8;
    xeps = 6;

    # print( hull );

    if abs( hull[ 1 ][ 0 ] - hull[ 2 ][ 0 ] ) > xeps :
        return False;

    rxmid = int( ( hull[ 1 ][ 0 ] + hull[ 2 ][ 0 ] ) / 2 );
    rymid = int( ( hull[ 1 ][ 1 ] + hull[ 2 ][ 1 ] ) / 2 );

    # print( rxmid, rymid );

    if abs( hull[ 0 ][ 1 ] - rymid ) > eps :
        return False;

    dist1 = math.hypot( hull[ 0 ][ 0 ] - rxmid, hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    dist2 = math.hypot( hull[ 0 ][ 0 ] - rxmid, hull[ 0 ][ 1 ] - hull[ 2 ][ 1 ] );

    # print( "LEFT TRIANGLE", dist1, dist2 )

    return abs( dist1 - dist2 ) <= eps;

def isValidRightTriangle( hull ) :
    eps = 8;
    xeps = 6;

    # print( hull );

    if abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] ) > xeps :
        return False;

    rxmid = int( ( hull[ 0 ][ 0 ] + hull[ 1 ][ 0 ] ) / 2 );
    rymid = int( ( hull[ 0 ][ 1 ] + hull[ 1 ][ 1 ] ) / 2 );

    # print( rxmid, rymid );

    if abs( hull[ 2 ][ 1 ] - rymid ) > eps :
        return False;

    dist1 = math.hypot( hull[ 2 ][ 0 ] - rxmid, hull[ 2 ][ 1 ] - hull[ 0 ][ 1 ] );
    dist2 = math.hypot( hull[ 2 ][ 0 ] - rxmid, hull[ 2 ][ 1 ] - hull[ 1 ][ 1 ] );

    # print( "RIGHT TRIANGLE", dist1, dist2 )

    return abs( dist1 - dist2 ) <= eps;

def isValidSquare( hull ) :
    eps = 5;

    lx = abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] );
    rx = abs( hull[ 2 ][ 0 ] - hull[ 3 ][ 0 ] );

    ly = abs( hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    ry = abs( hull[ 2 ][ 1 ] - hull[ 3 ][ 1 ] );

    # print( lx, rx, ly, ry );

    if abs( lx - rx ) > eps or abs( ly - ry ) > eps :
        return False;

    lxmid = int( ( hull[ 0 ][ 0 ] + hull[ 1 ][ 0 ] ) / 2 );
    rxmid = int( ( hull[ 2 ][ 0 ] + hull[ 3 ][ 0 ] ) / 2 );

    hull.sort( key = lambda x : x[ 1 ] );

    lymid = int( ( hull[ 0 ][ 1 ] + hull[ 1 ][ 1 ] ) / 2 );
    rymid = int( ( hull[ 2 ][ 1 ] + hull[ 3 ][ 1 ] ) / 2 );

    print( hull );
    print( lxmid, rxmid, lymid, rymid );

    dx = abs( lxmid - rxmid );
    dy = abs( lymid - rymid );

    # print( dx, dy );

    return abs( dx - dy ) <= eps;

def isValidLeftPentagon( hull ) :
    eps = 4;

    lx = abs( hull[ 1 ][ 0 ] - hull[ 2 ][ 0 ] );
    rx = abs( hull[ 3 ][ 0 ] - hull[ 4 ][ 0 ] );

    ly = abs( hull[ 1 ][ 1 ] - hull[ 2 ][ 1 ] );
    ry = abs( hull[ 3 ][ 1 ] - hull[ 4 ][ 1 ] );

    ymid = ( hull[ 1 ][ 1 ] + hull[ 2 ][ 1 ] ) / 2;

    # print( "LEFT:", lx, rx, ly, ry, ymid );

    return abs( lx - rx ) <= eps and abs( ly - ry ) <= eps and abs( ymid - hull[ 0 ][ 1 ] ) < eps;

def isValidRightPentagon( hull ) :
    eps = 4;

    lx = abs( hull[ 0 ][ 0 ] - hull[ 1 ][ 0 ] );
    rx = abs( hull[ 2 ][ 0 ] - hull[ 3 ][ 0 ] );

    ly = abs( hull[ 0 ][ 1 ] - hull[ 1 ][ 1 ] );
    ry = abs( hull[ 2 ][ 1 ] - hull[ 3 ][ 1 ] );

    ymid = ( hull[ 2 ][ 1 ] + hull[ 3 ][ 1 ] ) / 2;

    # print( "RIGHT:", lx, rx, ly, ry, ymid );

    return abs( lx - rx ) <= eps and abs( ly - ry ) <= eps and abs( ymid - hull[ 4 ][ 1 ] ) < eps;

def hullToList( hull ) :
    return [ ( vertex[ 0 ][ 0 ], vertex[ 0 ][ 1 ] ) for vertex in hull ];

def distanceFromHull( width, shape ) :
    knownWidth, focalLength = distanceConstants[ shape ];

    return 25.4 * knownWidth * focalLength / width;

# ------ FIX THIS ------
# ------ FIX THIS ------
# ------ FIX THIS ------
def getWidthCircle( hull ) :
    return -1;
# ------ FIX THIS ------
# ------ FIX THIS ------
# ------ FIX THIS ------

def getWidthSquare( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );
    rx = int( ( sign[ 2 ][ 0 ] + sign[ 3 ][ 0 ] ) / 2 );

    return rx - lx;

def getWidthLeftPentagon( sign ) :
    rx = int( ( sign[ 3 ][ 0 ] + sign[ 4 ][ 0 ] ) / 2 );

    return rx - sign[ 0 ][ 0 ];

def getWidthRightTriangle( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );

    return sign[ 2 ][ 0 ] - lx;

def getWidthRightPentagon( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );

    return sign[ 4 ][ 0 ] - lx;

def getWidthHexagon( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );
    rx = int( ( sign[ 4 ][ 0 ] + sign[ 5 ][ 0 ] ) / 2 );

    return rx - lx;

def getWidthOctagon( sign ) :
    lx = int( ( sign[ 0 ][ 0 ] + sign[ 1 ][ 0 ] ) / 2 );
    rx = int( ( sign[ 6 ][ 0 ] + sign[ 7 ][ 0 ] ) / 2 );

    return rx - lx;

def getWidthLeftTriangle( sign ) :
    rx = int( ( sign[ 1 ][ 0 ] + sign[ 2 ][ 0 ] ) / 2 );

    return rx - sign[ 0 ][ 0 ];

def getSignReadings( img ) :
    # PROCESSING IMAGE
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

    # GET SIGNS FROM CONTOURS
    signs = [];

    for contour in contours :
        contourVertices = cv2.approxPolyDP( contour, 0.03 * cv2.arcLength( contour, True ), True );
        hullVertices = cv2.convexHull( contourVertices );

        if len( contourVertices ) != len( hullVertices ) :
            continue;

        if cv2.contourArea( hullVertices ) < 300 :
            continue;

        hull = hullToList( hullVertices );
        hull.sort();
        sides = len( hull );

        # cv2.imshow( "image", img );
        # cv2.waitKey();

        # print( "checking:", hull );

        if sides == 3 and isValidLeftTriangle( hull ) :
            shape = "triangle left";
            
            hull.sort();
            widthHull = getWidthLeftTriangle( hull );

        elif sides == 3 and isValidRightTriangle( hull ) :
            shape = "triangle right";
            
            hull.sort();
            widthHull = getWidthRightTriangle( hull );

        elif sides == 4 and isValidSquare( hull ) :
            shape = "square";
            
            hull.sort();
            widthHull = getWidthSquare( hull );

        elif sides == 5 and isValidLeftPentagon( hull ) :
            shape = "pentagon left";
            
            hull.sort();
            widthHull = getWidthLeftPentagon( hull );

        elif sides == 5 and isValidRightPentagon( hull ) :
            shape = "pentagon right";
            
            hull.sort();
            widthHull = getWidthRightPentagon( hull );

        elif sides == 6 :
            shape = "hexagon";

            hull.sort();
            widthHull = getWidthHexagon();

        elif sides == 8 :
            shape = "octagon";
            
            hull.sort();
            widthHull = getWidthOctagon( hull );

        else :
            continue;

        distance = distanceFromHull( widthHull, shape );
        signs.append( ( shape, distance ) );
        cv2.drawContours( img, [ hullVertices ], 0, ( 0, 255, 0 ), -1);

    # print( signs );
    # cv2.imshow( "text", img );
    # cv2.waitKey();

    return signs;

''' GET COZMO WIDTHS '''
'''
circle
cozmo
'''

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
