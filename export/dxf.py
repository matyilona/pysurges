from typing import Iterable, Union, Tuple, List
import shapely as sp
import shapely.geometry as shpgm
import ezdxf
from export.frozen_notebook import save_frozen_notebook

def save_dxf( shapes: Iterable[ Union[ shpgm.Polygon, shpgm.Point] ], filename: str, save_notebook: bool = False ) -> None :
    """
    Saves polygons and points in a dxf file

    Parameters
    ----------
    polys : Iterable[ Union[ shpgm.Polygon, shpgm.Point ] ]
        Iterable of shapely polygons and points to include
    fiename : str
        Filename without .dxf extension
    """

    doc = ezdxf.new( dxfversion='AC1015', setup=True )
    doc.header['$MEASUREMENT']=1
    doc.header['$INSUNITS']=13

    mps = doc.modelspace()
    doc.layers.new( name="main", dxfattribs={'linetype':'dashed','color':7} )
    for s in shapes:
        if type( s ) == shpgm.Point:
            mps.add_point( (s.x, s.y), dxfattribs = { 'layer': 'main' } )
        elif type( s ) == shpgm.Polygon:
            boundary = list( zip( *s.exterior.xy ) )
            boundary.append( boundary[0] )
            mps.add_lwpolyline( boundary, dxfattribs = { 'layer': 'main' } )
        else:
            raise TypeError( "Only points and polygons can be exported to .dxf!" )
    doc.saveas( filename+".dxf" )

    if save_notebook:
        save_frozen_notebook( filename+"-generator.ipynb" )
