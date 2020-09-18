import ipyparams
import nbformat
import re
from datetime import datetime

def save_frozen_notebook( filename : str ) -> None :
    nb = nbformat.read( open( ipyparams.notebook_name, "r" ), nbformat.current_nbformat )
    for cell in nb.cells:
        if cell.cell_type in ( 'code', 'markdown' ):
            cell.metadata["editable"] = False
            cell.metadata["deletable"] = False
        if cell.cell_type == 'code':
            cell["source"] = re.sub("save_notebook?\s=?\sTrue","save_notebook = False", cell["source"] )
    nbformat.write( nb, open( f"{filename}-{datetime.now().strftime('%y%m%d-%H%M%S')}-generator.ipynb", "w" ) ) 
