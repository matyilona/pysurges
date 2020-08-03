from typing import Iterable, Union, Tuple, List
import shapely as sp
from shapely import ops
import numpy as np
from shapely.geometry import Point, LineString, MultiLineString, Polygon

def circle_segment( P: Point, r: float, a1: float = 0, a2: float = np.pi, d: int = 10, decimals = 5) -> LineString:
    """
    Generate cricle segment, made of linesegments
    
    Parameters
    ----------
    P : Point
		Center of circle
    r : float
		Radius of circle
    a1, a2 : float
		Starting/ending angles, starts at 12:00 goes clockwise
    d : float
		Number of line segments
    decimals : float
                Decimals to round to, to avoid nonequal points
	
    Returns
    -------
    circle : LineString
            LineString of the circlesegment
    """
    
    angles = np.linspace( a1, a2, d, endpoint=True )
    x = np.around( np.sin( angles )*r + P.x, decimals )
    y = np.around( np.cos( angles )*r + P.y, decimals )
    return( LineString( zip( x, y ) ) )

def box( P: Point, a: float, b: float ) -> Polygon:
    """
    Draw a rectangle, with sides along the x and y axis
    
    Parameters
    ----------
    P : Point
		Midpoint of rectangle
    a : float
		Width (along x axis)
    b : float
		Height (along y axis)
		
	Returns
	-------
	box : Polygon
		Shapely polygon
    """

    return( Polygon([
        [P.x-a/2,P.y-b/2],
        [P.x-a/2,P.y+b/2],
        [P.x+a/2,P.y+b/2],
        [P.x+a/2,P.y-b/2],
    ]))


def square( P: Point, a: float ) -> Polygon:
    """
    Draw square
    
    Parameters
    ----------
    P : Point
		Center of square
    a : float
		Side length
    """
    
    return( box(P,a,a) )

def basic_meander_line( l: float, r: float, n: int, d: int=10 ) -> LineString:
    """
    Very basic meander line
    
    Parameters
    ----------
    l : float
		Length of straight segments
    r : float
		Radius bends
    n : int
		No. of total straight segments
	d : int
		No. of linear segments making up bends
		
	Returns
	-------
	meander : LineString
		Simple meander line, as a shapley LineString
    """
    
    #every other line has to go in the other direction for the circles to connect well
    lines = [ LineString([[0,i*2*r],[l,i*2*r]][::(1-i%2*2)]) for i in range(n) ]
    circles = [ circle_segment(
			#every other circle has to be on the other side
            Point([l*((i+1)%2),(i*2+1)*r]),
            r,
            #every other circle curves the other way
            np.pi*(1-i%2*2),0,
            d=d) for i in range(n-1) ]
    meander = []
    for i in range(n-1):
        meander.append( lines[i] )
        meander.append( circles[i] )
    #the last line has no bend at the end
    meander.append( lines[n-1] )
    return( ops.linemerge( meander ) )

def line_to_cpwg( line: Union[ LineString, MultiLineString ], s: float, w: float ) -> Tuple[ Polygon, Polygon, LineString, LineString ]:
    """
    Generate two ditches of CPWG along the given line(s)
    
    Parameters
    ----------
    line : Union[ LineString, MultiLineString ]
		Line(s) to create CPWG from, might not always work with MultiLineString
    s, w : float
		CPWG parameters
		
	Returns
	-------
	elements : Tuple[ Polygon, Polygon, LineString, LineString, LineString ]
		Tuple of shapley shapes generated, in order:
		left_ditch : left CPWG ditch
		right_ditch : right CPWG ditch
		left_line : midline of the left ditch
		right_line : midline of the right ditch		
    """

    left_line = line.parallel_offset( (s+w)/2, "left", resolution=1 )
    right_line = line.parallel_offset( (s+w)/2, "right", resolution=1 )
    left_ditch = left_line.buffer( w/2, cap_style=2, resolution=1, )
    right_ditch = right_line.buffer( w/2, cap_style=2, resolution=1 )
    return( (left_ditch, right_ditch, left_line, right_line) )
    
def basic_meander( l: float, r: float, n: int, s: float, w: float, d: int = 10 ) -> Tuple[ Polygon, Polygon, LineString, LineString, LineString ]:
    """
    Very basic meander CPWG
    Can't use line_to_cpwg, strange bug with parallel_offset
    
    Parameters
    ----------
    s, w : float
		CPWG parameters
	l : float
		Length of straight segments
    r : float
		Radius bends
    n : int
		No. of total straight segments
	d : int
		No. of linear segments making up bends
		
	elements : Tuple[ Polygon, Polygon, LineString, LineString, LineString ]
		Tuple of shapley shapes generated, in order:
		left_ditch : left CPWG ditch
		right_ditch : right CPWG ditch
		meander : midline of the meander
		left_line : midline of the left ditch
		right_line : midline of the right ditch		
    """
    
    line = basic_meander_line( l, r, n, d )
    left_line = line.parallel_offset( (s+w)/2, "left", resolution=1 )
    right_line = line.parallel_offset( (s+w)/2, "right", resolution=1 )
    if n%2 == 0: # wierd shapely bug
        right_line = LineString( right_line.coords[1:-1] ) #
    left_ditch = left_line.buffer( w/2, cap_style=2, resolution=1, )
    right_ditch = right_line.buffer( w/2, cap_style=2, resolution=1 )
    return( (left_ditch, right_ditch, line, left_line, right_line) )

def launcher( s: float, w: float, a: float, b: float, c: float, g: float ) -> Polygon:
    """
    Generate rectangular launcher, faces to right, line starts at (0,0)
    
    Parameters
    ----------
    s, w : float
		CPWG parameters of line to connect to
    a, b : float
		Width, height of launcher
    c : float
		Lengt of transitional triangle
    g : float
		Gap around launcher
		
	Returns
	-------
	launcher : Polygon
		Launcher as a single polygon
    """
    
    outer_launcher = box( Point(c+a/2+g/2,0), a+g, b+2*g )
    inner_launcher = box( Point(c+a/2,0), a, b )
    outer_trans = Polygon( [[0,s/2+w],[c,b/2+g],[c,-b/2-g],[0,-s/2-w]])
    inner_trans = Polygon( [[0,s/2],[c,b/2],[c,-b/2],[0,-s/2]])
    inside = ops.unary_union( [inner_trans, inner_launcher] )
    outside = ops.unary_union( [outer_trans, outer_launcher] )
    launcher = outside.difference( inside )
    return( launcher, inside, outside )

def generate_dots_sq( r: float, d: float, bounding_box: Tuple[ float, float, float, float ] ) -> List[ Polygon ]:
    """
    Generate square lattice of round dots
    
    Parameters
    ----------
    r : float
		Radius of single dot
    d : float
		Distance between centers of dots
    bounding_box : Tuple[ float, float, float, float ]	
		Bounding box to fill with the pattern
	
	Returns
	-------
	pattern : List[ Polygon ]
		List of shapely polygons
    """
    
    x1,y1,x2,y2 = bounding_box
    nx = (x2-x1)/d
    ny = (y2-y1)/d
    dots = []
    for x in range( int(nx)+1 ):
        for y in range( int(ny)+1 ):
            dots.append( Polygon(circle_segment(Point(x*d+x1,y*d+y1),r,a1=0, a2=np.pi*2 ) ) )
    return( dots )

def generate_dots_tri( r: float, d: float, bounding_box: Tuple[ float, float, float, float ] ) -> List[ Polygon ]:
    """
    Generate triangle lattice of round dots
    
    Parameters
    ----------
    r : float
		Radius of single dot
    d : float
		Distance between centers of dots
    bounding_box : Tuple[ float, float, float, float ]	
		Bounding box to fill with the pattern
		
	Returns
	-------
	pattern : List[ Polygon ]
		List of shapely polygons
    """
    
    x1,y1,x2,y2 = bounding_box
    nx = (x2-x1)/d
    ny = (y2-y1)/d*np.sqrt(2)
    dots = []
    for x in range( int(nx)+1 ):
        for y in range( int(ny)+1 ):
            dots.append(Polygon(circle_segment(
                Point((x+y%2/2)*d+x1,y*d/np.sqrt(2)+y1)
                ,r,0,np.pi*2)))
    return( dots )

def generate_squares( a: float, d: float, bounding_box: Tuple[ float, float, float, float ] ) -> List[ Polygon ]:
    """
    Generate square pattern
    
    Parameters
    ----------
    a : float
		Side length of squares
    d : float
		Distance between squares
    bounding_box : Tuple[ float, float, float, float ]
		x1,y1,x2,y2 bounds of area to generate pattern in
		
	Returns
	-------
	pattern : List[ Polygon ]
		List of shapely polygons
    """
    
    x1,y1,x2,y2 = bounding_box
    nx = (x2-x1)/d
    ny = (y2-y1)/d
    squares = []
    for x in range( int(nx)+1 ):
        for y in range( int(ny)+1 ):
            squares.append( square(Point((x+y%2/2)*d+x1,y*d+y1),a))
    return( squares )
