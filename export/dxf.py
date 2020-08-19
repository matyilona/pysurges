from typing import Iterable, Union, Tuple, List
import shapely as sp
import shapely.geometry as shpgm
import ezdxf
from export.frozen_notebook import save_frozen_notebook

def save_dxf( polys: Iterable[ shpgm.Polygon ], filename: str, save_notebook: bool = False ) -> None :
    """
    Saves polygons in a dxf file

    Parameters
    ----------
    polys : Iterable[ shpgm.Polygon ]
        Iterable of shapely polygons to include
    fiename : str
        Filename without .dxf extension
    """

    doc = ez.new( setup=True )
    mps = doc.modelspace()
    for p in polys:
        boundary = list( zip( *p.exterior.xy ) )
        boundary.append( boundary[0] )
        mps.add_lwpolyline( boundary )
    doc.saveas( filename+".dxf" )

    if save_notebook:
        save_frozen_notebook( filename+"-generator.ipynb" )
