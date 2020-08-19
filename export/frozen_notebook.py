import ipyparams
import nbformat

def save_frozen_notebook( filename : str ) -> None :
    nb = nbformat.read( open( ipyparams.notebook_name, "r" ), nbformat.current_nbformat )
    for cell in nb.cells:
        if cell.cell_type in ( 'code', 'markdown' ):
            cell.metadata["editable"] = False
            cell.metadata["deletable"] = False
    nbformat.write( nb, open( filename, "w" ) ) 
