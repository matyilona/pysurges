from IPython.display import display, SVG
from lxml import etree
from typing import Iterable, Union, Tuple, List, Optional
import shapely as sp
from shapely.geometry import Point, LineString, MultiLineString, Polygon, MultiPolygon

shapely_displayable = Union[ LineString, Polygon, MultiLineString, MultiPolygon ]

def generate_svg_grid( x: float, y: float,
                       w: float, h: float,
                       d:float,  D: float,
					   dattrib: dict = {}, Dattrib: dict = {} ) -> etree.XML:
    """
    Generates SVG grid pattern
    
    Parameters
    ----------
    x, y : float
		coordinates to center grid on
    w, h : float
		total width and height of grid
    d, D : float
		step size of minor/major grid
    dattrib, Dattrib : dict
		attributes to pass to minor/major grid
		
	Returns
	-------
	grid_svg : etree.XML
		svg node containing the minor and major grid
    """
    
    grid_svg = etree.XML(f"""
    <g>
        <defs>
            <pattern id="smallGrid" width="{d}" height="{d}" patternUnits="userSpaceOnUse">
                <path id="minorSquare" d="M {d} 0 L 0 0 0 {d}" fill="none" stroke="gray" stroke-width="0.05"/>
            </pattern>
            <pattern id="grid" width="{D}" height="{D}" patternUnits="userSpaceOnUse">
                <rect width="{D}" height="{D}" fill="url(#smallGrid)"/>
                <path id="majorSquare" d="M {D} 0 L 0 0 0 {D}" fill="none" stroke="blue" stroke-width=".1"/>
            </pattern>
        </defs>
        <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#grid)" />
    </g>
    """)
    for k in dattrib.keys():
        grid_svg.xpath("//path[@id='minorSquare']")[0].attrib[k] = dattrib[k]
    for k in Dattrib.keys():
        grid_svg.xpath("//path[@id='majorSquare']")[0].attrib[k] = Dattrib[k]
    return( grid_svg )

def nice_svg( e: shapely_displayable, attribs: dict = {"stroke-width":"0"} ) -> etree.XML:
    """
    Create nice svg path from shapely element e.
    
    Parameters
    ----------
    attribs : dict
		attributes to be overvriten/given
		
	Returns
	-------
	svg : etree.XML
		svg element containing the themed shape
    """
    
    svg = etree.XML( e.svg() )
    for k in attribs.keys():
        svg.attrib[k] = attribs[k]
    return( svg )

def display_svg( elements: Iterable[ etree.XML ], bounds: Tuple[float, float, float, float], save_filename: Optional[str] = None ) -> None:
    """
    Display list of elements as an SVG in jupyter notebook
    
    Parameters
    ----------
    elements : Itreable[ etree.XML ]
		Iterable of svg elements, such as returned by nice_svg
		and svg_grid
	bounds : Tuple[ float, float, float, float ]
		Bounds of the area to display, can be smaller of larger than
		the actual area of the drawing0
    """
    
    x1,y1,x2,y2 = bounds
    svg_root = etree.XML(f"""
    <svg viewbox='{x1} {y1} {x2-x1} {y2-y1}' transform="scale(1,-1)" >
    </svg>
    """)
    for e in elements:
        svg_root.append( e )
    if save_filename is not None:
        etree.ElementTree(svg_root).write( save_filename )
    display(SVG(etree.tostring(svg_root)))
    
