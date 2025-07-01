import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math
from typing import List, Tuple, Optional, Union
from matplotlib.collections import PathCollection 
from matplotlib.text import Text 
from agente import *


def update(frame: int, agents: List[Agent], paths, scatters: List[PathCollection],texts: List[Text], ax: plt.Axes):
    """
        Questa funzione si occupa di aggiornare i vari frame per gli agenti al fine di garantirne la visualizzazione corretta.
        Gli argomenti della funzione sono:
        -)frame:indica il frame attuale, identificando da un intero che corrisponde all'istante di tempo attuale nei vari paths.
        -)agents: lista degli agenti
        -)paths:è la lista dei percorsi, uno per ogni agente.
        -)scatters: è la lista degli scatter necessari per la visualizzazione dinamica dei percorsi degli agenti nel tempo.
        -)texts: è la lista delle label per i vari agenti, usata per garantire maggiore chiarezza nell'animazione.
        -)ax: assi della mappa

        La funzione descrive una lista degli elementi che devono essere aggiornati da un frame all'altro.

        Si descrive brevemente il funzionamento step-by-step della funzione:
        1)Si esegue un loop per i vari percorsi:
            -)se il frame corrente è maggiore della lunghezza del percorso per un certo agente, allora significa che l'
            agente ha già raggiunto la sua posizione goal e quindi rimane fermo in quella posizione.
            -)si estraggono le coordinate x ed y dell'agente
            -)si aggiornano le label assegnate a ciascun agente
        2)Il titolo che si assegna per vedere lo scorrere dei vari frame è Time-Step, dato che ogni frame 
        corrisponde ad un'istante di tempo.
    """
    for index, path in enumerate(paths):
        if path is None or frame >= len(path):
            continue
        position = path[frame]
        y, x = position[0]
        scatters[index].set_offsets([x, y])
        texts[index].set_position((x + 0.3, y)) 
        texts[index].set_text(f"A{index+1}\nt={frame}")
    ax.set_title(f"Time-Step: {frame}") 
    return scatters + texts





def plot_animation(map:np.ndarray, agents:List[Agent], paths):
    """
        Questa funzione permette di visualizzare l'andamento dei vari agenti nella mappa rispetto ai 
        loro percorsi.
        
        Gli argomenti della funzione sono:
        -)map: un array NumPy bidimensionale le cui celle libere sono marcate con 0, le celle occupate
        da ostacoli sono invece contrassegnate dal valore 1.
        -)agents: una lista di oggetti appartenenti alla classe Agent. Ogni elemento di questa lista di agenti
        contiene le informazioni centrali dell'agente necessaria per la visualizzazione dell'algoritmo, quindi:
            -)il colore dell'agente
            -)la posizione iniziale dell'agente(che nell'animazione è rappresentata da un quadrato del medesimo colore dell'agente)
            -)la posizione finale dell'agente(che nell'animazione è rappresentata da una X del medesimo colore dell'agente)
        -)paths: una lista che corrisponde ai percorsi trovati per i vari agenti dall'algoritmo Prioritized Planning.
        Il percorso di un agente, se trovato, è descritto come una sequenza di posizioni (identificate dalle coordinate x ed y) e l'istante temporale 
        in cui l'agente si trova nella cella.

        Si riporta una breve descrizione step-by-step della funzione:
        1)si verifica che paths non sia None. Se paths è None significa che l'algoritmo 
        PP non è stato in grado di trovare una soluzione valida al problema, per tanto viene restituito un messaggio di errore
        che impedisce la generazione dell'animazione.
        2) si determina il tempo massimo di durata dell'animazione, che è pari alla lunghezza
        del percorso piu lungo trovato, assumendo che ogni arco nel percorso costi esattamente 1 time step.
        3) si inizializza la figura necessaria per l'animazione corrispondente alla mappa, e le due assi(x ed y).
        In particolare la figurà avrà per default dimensione 7x7, e per identificare gli ostacoli si utilizza il colore Nero.
        4) per ogni agente:
            -)si detetermina la posizione iniziale
            -)si determina la posizione obiettivo
            -)si marca all'interno della mappa la posizione iniziale con un quadrato
            -)si marca all'interno della mappa la posizione finale con una X
        5) si esegue un ciclo su tutti i percorsi:
            -)il percorso viene evidenziato dal colore dell'agente di quel path, al fine di avere maggiore chiarezza
            nella visualizzazione
            -)per ogni agente si inizializza una lista, line_for_agent, che contiene tutti gli archi del percorso.
            -)si aggiunge il segmento ottenuto alla lista precedentemente definita
            -)quando si ottengono tutti i segmenti necessari per mostrare il percorso dell'agente li si inserisce nella lista
            paths_for_agents.
        6) si esegue un ciclo su tutti gli agenti assegnando a ciascuno di essi il relativo scatter, centrale per la visione del 
        movimento degli agenti.
    """
    
    if paths is None:
        return "Soluzione non trovata, impossibile generare l'animazione."
    max_time:int=0
    for path in paths:
        if path:
            max_time:int = max(max_time, len(path))

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(map, cmap="Greys", origin="upper")
    ax.set_xticks(np.arange(map.shape[1]))
    ax.set_yticks(np.arange(map.shape[0]))
    ax.grid(True, which='both', color='lightgrey', linewidth=0.5)
    
    scatters: List[PathCollection] = []  
    texts: List[Text] = []             
    path_lines: List[List[plt.Line2D]] = []

    for a in agents:
        start_row, start_column = a.start_position
        goal_row, goal_column = a.goal_position
        ax.scatter(start_column, start_row, marker='s', color=a.color, s=300, edgecolors='black', zorder=6, label='Start')
        ax.scatter(goal_column, goal_row, marker='X', color=a.color, s=300, edgecolors='black', zorder=6, label='Goal')

    
    
    for index, path in enumerate(paths):
        if path is None:
            path_lines.append([])
            continue
        agent_color = agents[index].color
        lines_for_agent: List[plt.Line2D]=[]
        for i in range(1, len(path)):
            if isinstance(path[i][0], tuple): 
                (y0, x0), _ = path[i - 1]
                (y1, x1), _ = path[i]
            else: 
                y0, x0 = path[i - 1]
                y1, x1 = path[i]

            if (abs(x1 - x0), abs(y1 - y0)) in [(0, 0), (1, 0), (0, 1)]:
                l, = ax.plot([x0, x1], [y0, y1], color=agent_color, linewidth=2, alpha=0.3)
                lines_for_agent.append(l)
        path_lines.append(lines_for_agent)

    for agente in agents:
        scatter = ax.scatter([], [], s=100, color=agente.color, edgecolors='black', zorder=5)
        scatters.append(scatter)
        text = ax.text(0, 0, '', fontsize=8, color='black')
        texts.append(text)

    animation_element = animation.FuncAnimation(
        fig,
        update,
        frames=max_time,
        fargs=(agents,paths, scatters, texts,ax),
        interval=600,
        repeat=False
    )
    plt.show()
   
