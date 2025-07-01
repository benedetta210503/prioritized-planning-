import matplotlib.pyplot as plt
from typing import List
from agente import *
def genera_grafici(agents: List[Agent], expanded_nodes: List[int], running_time: List[float], costo: List[int],map_name:str)->None:
    """
        Questa funzione genera tre grafici che evidenziano l'andamento delle prestazioni 
        dell'algoritmo Prioritizied Planning al variare del numero numero di agenti.
        I 3 grafici sono, in ordine:
        1)Numero nodi espansi al variare del numero di agenti(blu)
        2)Running time al variare del numero di agenti(verde)
        3)Costo della soluzione trovata al variare del numero di agenti(rosso)

        Gli argomenti della funzione sono:
        -)agents (List[int]): Lista con il numero di agenti per ogni esperimento.
        -)expanded_nodes (List[int]): Lista del numero di nodi espansi in ciascun esperimento.
        -)running_time (List[float]): Lista dei tempi di esecuzione in secondi.
        -)costo (List[int]): Lista dei costi totali dei percorsi generati.
        -)map_name: nome della mappa che si intende testare


    """
    plt.figure(figsize=(18, 5)) 

    plt.subplot(1, 3, 1)
    plt.plot(agents, expanded_nodes, marker='o', color='blue')
    plt.title('Nodi Espansi vs Numero di Agenti')
    plt.xlabel('Numero di Agenti')
    plt.ylabel('Nodi Espansi')
    plt.grid(True)

   
    plt.subplot(1, 3, 2)
    plt.plot(agents, running_time, marker='o', color='green')
    plt.title('Tempo vs Numero di Agenti')
    plt.xlabel('Numero di Agenti')
    plt.ylabel('Tempo (s)')
    plt.grid(True)

    
    plt.subplot(1, 3, 3)
    plt.plot(agents, costo, marker='o', color='red')
    plt.title('Costo vs Numero di Agenti')
    plt.xlabel('Numero di Agenti')
    plt.ylabel('Costo')
    plt.grid(True)

   
    plt.tight_layout()
    plt.savefig(f"grafici_risultati_{map_name}.png")

    plt.close()

def genera_percentuali(num_agents:int,num_failure:int,num_success:int,map_name:str):
    """
        Questa funzione genera un grafico a barre che mostra il conteggio dei successi e fallimenti 
        degli esperimenti per un dato numero di agenti.

        Gli argomenti della funzione sono:
        -)num_agent:il numero degli agenti
        -)num_failure:il numero di fallimenti, cioè di volte in cui PP non è in grado di trovare una soluzione valida
        -)num_success:il numero di successi di PP
        -)map_name:nome della mappa che si intende testare
    """
    labels = ['Successi', 'Fallimenti']
    values = [num_success, num_failure]
    colors = ['green', 'red']

    plt.figure(figsize=(6,4))
    plt.bar(labels, values, color=colors)
    plt.title('Conteggio Successi e Fallimenti')
    plt.ylabel('Numero Esperimenti')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"percentuali_successi_{map_name}.png")
    plt.close()
