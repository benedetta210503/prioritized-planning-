import random
import matplotlib
import matplotlib.pyplot as plt
from typing import List, Tuple
import numpy as np
class Agent:
    """
        Questa classe rappresenta un agente all'interno dell'ambiente di simulazione del problema di 
        Multi-Agent Pathfinding.
        Ogni agente è caratterizzato da:
        -)una posizione di partenza
        -)una posizione obiettivo
        -)un colore
        -)un livello che ne indica la priorità
    """
    def __init__(self, start_position: Tuple[int, int], goal_position: Tuple[int, int],
                 color: Tuple[float, float, float, float], priority: int):
        """
            Questa funzione inizializza un nuovo agente.
            Gli argomenti della funzione sono:
            -)start_position: è una tupla di due valori interi che indica la posizione di partenza
            dell'agente, in particolare tale tupla definisce le coordinate x ed y , dato che si assume le mappe siano bidimensionali.
            -)goal_position:è una tupla di due valori interi che indica la posizione obiettivo che l'agente
            deve raggiungere, in particolare tale tupla definisce le coordinate x ed y , dato che si assume le mappe siano bidimensionali.
            -)color: è il colore che identifica l'agente, al fine di avere una migliore esperienza di visualizzazione dell'algoritmo.
            -)priority: indica il livello di priorità assegnato a ciascun agente, in accordo con il funzionamento dell'algoritmo
            Prioritized Planning
        """
        self.start_position=start_position
        self.goal_position=goal_position
        self.color=color
        self.priority=priority

def generate_agents(map:np.ndarray, max_num_agents:int, seed:int=0):
    """
        Questa funzione genera un insieme di agenti assegando a ciascuno di questi una posizione iniziale
        ed una posizione obiettivo che siano valide, dove con valide si intende che:
        1) siano celle libere nella mappa, quindi non corrispondenti ad ostacoli
        2)in accordo con la formulazione classica del problema MAPF, ogni agente deve avere una posizione di partenza e 
        una posizione obiettivo uniche.

        Gli argomenti della funzione sono:
        -)map: un array NumPy bidimensionale le cui celle libere sono marcate con 0, le celle occupate
        da ostacoli sono invece contrassegnate dal valore 1.
        -)max_num_agents: un valore intero che indica il numero massimo di agenti che la funzione genera
        -)seed:un valore intero settato per default a 0, che funge da generatore pesuedocasuale, 
        centrale per garantire la riproducibilità degli algoritmi. In particolare nel codice viene utilizzato
        per generare le posizioni di partenza e le posizioni finali dei vari agenti, andando ad eseguire uno shuffle delle celle libere
        presenti nella mappa considerata. Utilizzando lo stesso seed per vari esperimenti, le celel di partenza e finali dei vari agenti
        sono uguali, utilizzando invece seed diversi si hanno istanze diverse del problema garantendo posizioni iniziali e terminali
        differenti per gli agenti, al fine di osservare al meglio le prestazioni dell'algoritmo.

        La funzione, dopo aver determinato il numero di celle libere nella mappa, e quindi candidate per essere assegnate
        ai vari agenti, verifica se il numero di agenti che si intende generare è valido, ossia
        se per ogni agente si possono assegnare le 2 posizioni univoche.
        Se ci sono sufficienti celle per i vari agenti la funzione restituisce la lista degli agenti che sono stati generati.
        Qualora non ci siano abbastanza celle per generare tutti gli agenti viene sollevata un'eccezione.

        Si riporta una breve descrizione step-by-step della funzione:
        1) inizializzazione del generatore pseudocasuale di numeri
        2) definzione delle 2 dimensioni della mappa(che ricordiamo essere un array bidimensionale), 
        dunque altezza e larghezza, tramite l'attributo .shape definito nella libreria NumPy.
        3)definizione delle celle libere, identificate dal valore 0, eseguendo un ciclo su tutte le righe e le colonne
        della mappa.
        4)shuffle casuale delle celle libere.
        5)verifica dell'idoneità del numero di agenti in corrispondenza al numero di celle libere:
        Si verifica se per ogni agente sono presenti 2 celle libere univoche, ed in caso contrario viene sollevata un'eccezione.
        6)preparazione di una ColorMap che contiene tanti colori diversi quanto il numero di agenti. Tale passo
        è centrale per assegnare ad ogni agente un colore differente, per avere maggiore chiarezza durante la visione dell'animazione.
        7) generazione degli agenti:
            -)si inizializza come vuota la lista degli agenti.
            -)ad ogni agente viene assegnata la posizione di partenza  estraendola tramite la funzione .pop(),
            centrale per garantire l'unicità delle posizioni. La funzione pop(), in accordo con la documentazione,
            estrae l'ultima cella libera e la rimuove dalla lista.
            -)allo stesso modo si assegna la posizione da raggiungere ad ogni agente.
            -)si assegna ad ogni agente un livello di priorità ed un colore(grazie alla colormap precedentemente definita).
            -)si inserisce l'agente nella lista.

    """
    random.seed(seed)
    height, width = map.shape
    
    free_cells: List[Tuple[int, int]] = [(r, c) for r in range(height) for c in range(width) if map[r, c] == 0]

    random.shuffle(free_cells)

    if len(free_cells) < max_num_agents * 2:
        raise ValueError(f"Il numero di celle libere nella mappa({len(free_cells)}) non è sufficiente per generare {max_num_agents} agenti."
                        f"""Sono necessarie, per assegnare a ciascun agente una posizione di partenza
                        e una posizione obiettivo,almeno {max_num_agents * 2} celle.Si prega di inserire un numero minore di agenti.""")
    colormap = plt.cm.get_cmap('hsv', max_num_agents)
    all_agents:List[Agent] = []
    for i in range(max_num_agents):
            start = free_cells.pop()
            goal = free_cells.pop()
            agente = Agent(start_position=start, goal_position=goal,
                           color=colormap(i), priority=i+1) 
            all_agents.append(agente)
    return all_agents
