from typing import Iterable, Union, Tuple, List
import shapely.geometry as shpgm
import gdstk
from export.frozen_notebook import save_frozen_notebook

def poly_to_gds( poly: shpgm.Polygon, layer: int = 0 ) -> gdstk.Polygon :
    """
    Create a gdstk polygon from a shapely Polygon

    Parameters
    ----------
    poly : shapely.geometry.Polygon
        Polygon to be converted
        Can not have any holes, only exterior is converted
    layer : int
        GDS layer to put polygon on

    Returns
    -------
    gds : gdstk.Polygon
        gds element that can be added to a gds cell
    """

    gds = gdstk.Polygon( list( zip( *poly.exterior.xy ) ) )
    gds.layer = layer
    return( gds )

def line_to_gds( line: shpgm.LineString, width: float, layer: int = 0 ) -> gdstk.FlexPath :
    """
    Create a gdst path from a shapely LineString

    Parameters
    ----------
    line : shapely.geometry.LineString
        Line to be converted
        Should be made up of straight segments only
    width : width of the line
    layer : int
        GDS layer to put element on

    Returns
    -------
    gds : gstk.FlexPath
        gds element that can be added to a gds cell
    """

    gds = gdstk.FlexPath( [*line.coords], width, layer=layer )
    return( gds )

def save_gds_polys( polys: Iterable[ gdstk.Polygon ], filename: str, save_notebook:bool = False ) -> None :
    """
    Saves gdstk polygons into file, as well as a frozen version of the current notebook

    Parameters
    ----------
    polys : Iterable[ gdstk.Polygon ]
        Polygons to save
    filename : str
        Filename without .gds extension
    save_notebook : bool
        If True, save a frozen version of the notebook along with the gds file
    """

    lib = gdstk.Library()
    cell = lib.new_cell( "Main_cell" )
    for p in polys:
        cell.add( p )
    lib.write_gds( filename+".gds" )

    if save_notebook:
        save_frozen_notebook( filename )
