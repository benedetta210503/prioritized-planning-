import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List
from numpy.typing import NDArray

def read_map(filename:str)-> List[List[int]]:
    """
        Questa funzione legge un file, corrispondente alla mappa che si intende testare,
        e lo converte in una griglia bidimensionale caratterizzata dai seguenti 2:
        -)valore 0: cella libera
        -)valore 1: ostacolo

        L'argomento della funzione è il filename che contiene la mappa su cui si vuole testare il
        Prioritized Planning.
        La funzione restituisce la mappa come una griglia 2 dimensionale.

        Viene fornita una breve descrizione della funzione:
        1)apre il file il cui percorso è specificato negli argomenti della funzione
        2)rimuove eventuali spazi bianchi e caratteri di newline dalle varie righe
        3)inizia la costruzione e lettura della mappa vera e propria. Tale punto di inizio è rappresentato da map_start
        4)costruisce la mappa come un'array bidimensionale verificando se una cella è libera(inserisce 0) o occupata
        (inserisce 1).
    """
    with open(filename) as f:
        lines:List[str] = [line.strip() for line in f.readlines()]
    map_start:int = lines.index("map") + 1
    map_lines: List[str] = lines[map_start:]
    map: List[List[int]] = [[0 if c == '.' else 1 for c in line] for line in map_lines]
    return map

def create_map(map:List[List[int]])-> NDArray[np.int_]:
    """
        Questa funzione converte la mappa, una griglia bidimensionale di valori interi,
        in un array NumPy

        La funzione restituisce l'array NumPy 2D necessario per la visualizzazione della mappa.
    """
    return np.array(map)

def plot_map(map: NDArray[np.int_]):
    """
        Questa funzione visualizza la mappa, un array NumPy in scala di grigi, in modo dale che a visualizzazione
        rispetti i seguenti due colori:
            colore bianco= cella vuota
            colore nero= ostacolo
        
    """
    plt.imshow(map, cmap='Greys')
    plt.title("Mappa")
    plt.xticks(np.arange(len(map[0])))
    plt.yticks(np.arange(len(map)))
    plt.show()