import math
import heapq
import numpy as np
from queue import PriorityQueue
from agente import Agent
import time
from typing import Dict, Tuple, List, Set, Optional, Any
from numpy.typing import NDArray

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
WAIT = (0, 0)

max_iterations=100000000


def manhattan_distance(s:Tuple[int, int],g: Tuple[int, int])->int:
    """
        Questa funzione calcola la distanza di Manhattan tra 2 punti, definita come la somma tra le differenze
        assolute delle 2 celle lungo l'asse x e l'ungo l'asse y.
        Tale funzione è centrale, dato che rappresenta l'euristica che si utilizza nell'algoritmo A*,
        dato che gode di 2 proprietà centrali:
        1)admissability
        2)consisistency

        Gli argomenti della funzione sono:
        1)s: punto iniziale, definito come una tupla di 2 valori interi che corrispondono alla coordinata X e 
        alla coordinata Y.
        2)g: punto finale, definito come una tupla di 2 valori interi che corrispondono alla coordinata X e 
        alla coordinata Y.

    """
    return abs(s[0]-g[0])+abs(s[1]-g[1])

def give_new_position(action: Tuple[int,int] ,position: Tuple[int,int])->Tuple[int,int]:
    """
        Questa funzione calcola la nuova posizione che si raggiunge sulla mappa a partire da una posizione iniziale
        e applicando una certa azione.

        Gli argomenti della funzione sono:
        -)action: è l'azione che si intende eseguire, e puà essere:
            -)UP=(-1,0)
            -)DOWN=(1,0)
            -)LEFT=(0,-1)
            -)RIGHT=(0,1)
            -)WAIT=(0,0)
        -)position: è la posizione di partenza

        La posizione successiva viene calcolata sommando alla posizione corrente(position)
        l'azione scelta (action)
    """
    
    return (position[0] + action[0], position[1] + action[1])
    
def is_new_position_possible(map:NDArray[np.int_],position:Tuple[int,int])->bool:
    """
        Questa funzione verifica se la posizione dell'agente è accettabile o meno.
        Una posizione NON è accettabile( e di conseguenza non è accettabile l'azione che ha portato a tale posizione)
        se si verifica:
        1)la posizione, descritta dalle sue coordinate x ed y, è al di fuori dei limiti dimensionali della mappa
        2)la posizione,descritta dalle sue coordinate x ed y, è una cella occupata da un ostacolo.

        Gli argomenti della funzione sono:
        -)la mappa, fornita come un array NumPy 2D
        -)la posizione,definita come una tupla di due valori interi, di cui si vuole controllare l'accettabilità

        La funzione restituisce un valore booleano, in particolare:
        -)True: la posizione è accettabile e valida
        -)False: la posizione non è valida

        Si fornisce una breve descrizione della funzione:
        1)Si determinano le coordinate della posizione attuale, quindi la colonna e la riga corrispondenti.
        2)Si determinano i margini della mapa in altezza(height) e in larghezza(width)
        3)Si verifica se le coordinate della posizione sono valide, quindi interne ai limiti della mappa.
        4)Si verifica che la posizione non coincida con un ostacolo(identificato dal valore 1 nella mappa)
    """
    row, col = position
    height, width = map.shape 
    if row < 0 or row >= height or col < 0 or col >= width:
        return False
    if map[row, col] == 1:
        return False
    return True

def reconstruct_path(came_from, current):
    """
        Questa funzione ricostruisce il percorso ottimale calcolato dall'algoritmo A*.
        
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path 


def A_Star(map:NDArray[np.int_],agente: Agent,constraints: Set[Tuple[Tuple[int, int], int]]):
    """
        Questa funzione esegue l'algoritmo di ricerca A* per trovare il percorso orttimale per un agente, data la sua posizione di 
        partenza e la sua posizione di arrivo.
        La funzione euristica che si utilizza in questa implementazione è la distanza di Manhattan, calcolata mediante la funzione
        sopra descritta e trattata.

        Gli argomenti della funzione sono:
        -)map: array NumPy 2D con celle libere(0) e ostacoli(1)
        -)agente: agente di cui si intende trovare il percorso ottimale, la cui posizione iniziale e 
        finale è specificata come campo della classe Agent.
        -)constraints: è l'insieme dei vincoli che devono essere rispettati. Tali vincoli sono espressi come
        insiemi di tuple. I vincoli di cui si tiene conto sono:
            1)(posizione,tempo): tale vincolo impedisce all'agente di trovarsi in una determinata posizione
            in un certo istante di tempo. Tale vincolo impedisce che vi siano conflitti di vertice.
            2)((posizione_iniziale,posizione_arrivo),tempo): tale vincolo impedisce all'agente di percorrere
            un determinato arco nella direzione posizione_iniziale->posizione_arrivo. Questo vincolo permette di impedire
            eventuali Edge Conflicts.
        
        La funzione restituisce:
        -)il percorso ottimale trovato per l'agente, il numero di nodi espansi, ed il costo di tale percorso
        in caso di successo
        -)None in caso di insuccesso

        Si offre ora una descrizione della funzione:
        1)Si inizializzano a 0 le seguenti variabili:
            -)iterations(utilizzata per dare un limite all'algoritmo A*)
            -)count(utilizzata per tenere traccia dei nodi espansi)
        2)si estraggono la posizione iniziale e la posizione finale dell'agente, e si definisce
        lo stato iniziale, che contiene informazioni relative alla posizione iniziale e al time-step iniziale(ovviamente settato a 0).
        3)si inizializza la frontiera,centrale per l'algoritmo A*, che conterrà i vari stati in ordine di funzione di valutazione
        f=g+h, dove si ricorda che g=costo, h=funzione euristica.
        4)si inserisce nella frontiera lo stato iniziale.
        5)si inizializza il dizionario came_from, necessario per la ricostruzione del percorso
        dell'agente.
        6)si inizializza il dizionario g_score, che contiene il costo minore per raggiungere vari stati. Viene isnerito
        come primo elemento lo stato iniziale, ed il costo per raggiungere tale stato è banalmente 0.
        7)si inizializza open_set,un insieme che permette di verificare i nodi già presenti nella frontiera.
        8)si settano a 0 i nodi esplorati.
        9) si esegue un loop fin quando la frotniera non è vuota.
            10)si verifica se il numero di iterazioni eseguite per un agente supera il numero massimo di 
            iterazioni accettate. Questo è fondamentale per porre un time-out all'algoritmo A*.
            Se il numero massimo di iterazioni viene superato si restituisce un messsaggio di errore e il percorso trovato
            sarà None, cioè l'algoritmo non è stato in grado di trovare un percorso ottimale e valido per l'agente.
            11) si estrae dalla frontiera il nodo migliore, cioè quello caratterizzato da un valore
            della funzione di valutazione f minore, e lo si rimuove da open_set. Questo nodo verrà dunque espanso.
            12)se la posizione corrispondente al nodo scelto per l'espansione è uguale alla posizione obiettivo, allora
            si ricostruisce il percorso dallo stato iniziale allo stato di arrivo, e si calcola il costo di tale percorso.
            13)se la posizione corrispondente al nodo scelto differisce dalla posizione obiettivo allora si calcolano le nuove possibili
            posizioni applicando le varie azioni. Si verifica se tale posizione sia valida e che rispetti i vincoli.
            14) si calcola il g_score per il nodo vicino generato, e si verifica se il nuovo costo ottenuto
            per raggiungere tale nodo è minore(quindi migliore) del costo associato a tale nodo(qualora non fosse presente tale nodo allora ha di default un costo infinito).
            15)se il g_score è minore allora si aggiorna:
                -)il dizionario g_score
                -)la funzione di valutazione f
            16)si inserisce il nodo espanso in open_set.
     
    """
    
    iterations:int=0
    count:int=0

    start:Tuple[int,int]=agente.start_position
    goal:Tuple[int,int]=agente.goal_position
    start_state:Tuple[Tuple[int, int], int] = (start, 0)

    frontier:List[Tuple[float, int, Tuple[int, int], int]]= []
    heapq.heappush(frontier, (0, count, start, 0)) 

    came_from:Dict[Tuple[Tuple[int, int], int], Tuple[Tuple[int, int], int]]= {}
    g_score:Dict[Tuple[Tuple[int, int], int], float] = {start_state: 0}
    open_set:Set[Tuple[Tuple[int, int], int]] = {start_state}
   
    expanded_nodes:int=0
    
    while frontier:

        if iterations > max_iterations:
            print("Timeout A*: numero massimo di esecuzioni superato. Soluzione non trovata")
            return None
        
        iterations += 1

        _, _, current_pos, current_time = heapq.heappop(frontier)
        open_set.discard((current_pos, current_time))

        expanded_nodes+=1

        if current_pos == goal:
            path=reconstruct_path(came_from, (current_pos, current_time))
            cost=len(path)-1
            return expanded_nodes,path,cost

        for action in [UP, DOWN, LEFT, RIGHT, WAIT]:
            neighbor = give_new_position(action, current_pos)
            next_time = current_time + 1

            if not is_new_position_possible(map, neighbor):
                continue
            if (neighbor, next_time) in constraints:
                continue
            if ((current_pos,neighbor), next_time) in constraints:
                continue

            new_g_score = g_score[(current_pos, current_time)] + 1

            neighbor_state = (neighbor, next_time)

            if new_g_score < g_score.get(neighbor_state, float('inf')):
                came_from[neighbor_state] = (current_pos, current_time)
                g_score[neighbor_state] = new_g_score
                f =new_g_score + manhattan_distance(neighbor, goal)
                if neighbor_state not in open_set:
                    count += 1
                    heapq.heappush(frontier, (f, count, neighbor, next_time))
                    open_set.add(neighbor_state)
    
    return None 

def prioritized_planning(map:NDArray[np.int_],agenti:List[Agent]):
    """
        Questa funzione implementa l'algoritmo Prioritized Planning, un algoritmo
        che ricerca i percorsi per i vari agenti seguendo l'ordine di priorità assegnato.

        Gli argomenti della funzione sono:
        -)map: array NumPy 2D con celle libere(0) e ostacoli(1)
        -)agenti:lista di agenti che si considerano nell'istanza.
            Ogni agente ha come attributo, oltre alla posizione iniziale e finale, anche un valore intero che ne indica
            il livello di priorità.
        
        La funzione restituisce:
        -)None in caso di fallimento
        -)Il numero totale di nodi espansi, il costo totale per i vari percorsi e i vari percorsi trovati.

        Si offre una breve descrizione della funzione:
        1)si inizializza il numero totale di nodi espansi a 0, cosi come il costo totale.
        2)la lista dei percorsi trovati per i vari agenti viene inizializzata come lista vuota
        3)l'insieme dei vincoli è inizialmente un insieme vuoto.
        4)si esegue un ciclo sull'insieme dei vari agenti, ordinati in base allaloro priorità.
        5)si richiama l'algoritmo A* per ricercare il percorso ottimale per l'agente.
        Se tale percorso esiste, cioè non è None, allora si aggiornano i dati e si aggiorna l'insieme dei vincoli aggiungendo
        per i successivi agenti:
        1)vertex conflict: si impedisce agli agenti successivi di trovarsi nella stessa posizione nello stesso istante di tempo
        di un agente già pianificato.
        2)edge conflict: si impedisce agli agenti successivi di spostarsi lurgo un arco che in un dato istante di tempo
        viene attraversato da un agente già pianificato


    """
    total_expandend_nodes:int=0
    total_cost:int=0
    paths:List[List[Tuple[Tuple[int, int], int]]]=[]
    constraints=set()

    for agente in sorted(agenti, key=lambda a: a.priority):
        results = A_Star(map, agente, constraints=constraints.copy())
        if(results is None):
            return None
        nodes_expandend, path_for_agente,cost = results
        
        total_expandend_nodes+=nodes_expandend
        total_cost+=cost
        if path_for_agente is None:
            return None
        for posizione,tempo in path_for_agente:
            constraints.add((posizione, tempo))
        for t in range(1, len(path_for_agente)):
            prev_pos = path_for_agente[t - 1][0]
            curr_pos = path_for_agente[t][0]
            constraints.add(((curr_pos, prev_pos), t))
        paths.append(path_for_agente)

    return total_expandend_nodes,paths,total_cost