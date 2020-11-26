from typing import Iterable, Union, Tuple, List
import shapely as sp
from shapely import ops
from shapely.geometry import Polygon, MultiPolygon
import fontforge

font = None

def set_font( ttf_file: str ) -> None:
    global font
    """
    Set the ttf font to be used.
    Should not have curves, other restrictions may apply.
    
    Parameters
    ----------
    ttf_file: str
        Path to the .ttf file to be loaded
    """

    font = fontforge.open( ttf_file )

def get_glyph( c: chr ) -> fontforge.glyph:
    global font
    """
    Get the fontforge glyph associated to the character, if any.

    Parameters
    ----------
    c: chr
        Character to be looked up

    Returns
    -------
    glyph: fontforge glyph
        The fontforge glyph assigned to c in the selected font
    """
    return( font[ font.findEncodingSlot( c ) ] )

def glyph_to_mp( g: fontforge.glyph )-> MultiPolygon:
    """
    Converts fontforge glyphs to shapely polygons.

    Parameters
    ----------
    g: fontforge glyph
        Glyph to be converted

    Returns
    -------
    mp: shapely MultiPolygon
        MultyPolygon representing the whole glyph
    """
    fg = g.layers[1]
    polys = MultiPolygon( [ Polygon( [ (p.x, p.y) for p in c ] ) for c in fg ] )
    mp = MultiPolygon( [ polys[0] ] )
    if len(polys) > 1:
        for h in polys[1:]:
            if mp.contains( h ):
                mp = mp.difference( h )
            else:
                mp = MultiPolygon( [ *mp, h ] )
    if type( mp ) == Polygon:
        mp = MultiPolygon( [mp] )
    return( mp )

def str_to_mp( s: str, xoff: float = .1, space: float = .5, height = None, start = None )->MultiPolygon:
    global font
    shp = glyph_to_mp( get_glyph( s[0] ) )
    spaces = 0
    for i in s[1:]:
        if i == " ":
            spaces += 1
        else:
            shp = MultiPolygon( [ *shp, *sp.affinity.translate( glyph_to_mp( get_glyph( i ) ),
                xoff = shp.bounds[2] + (spaces*space + xoff)*font.em ) ] )
            spaces = 0
    if height:
        factor = height/(shp.bounds[3]-shp.bounds[1])
        shp = sp.affinity.scale( shp, xfact=factor, yfact=factor, origin=(0,0) )
    if start:
        shp = sp.affinity.translate( shp, xoff=start[0], yoff=start[1] )
    return( shp )
