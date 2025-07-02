import numpy as np
import matplotlib.pyplot as plt
import random
import time
import argparse
from prioritized_planning import *
from agente import *
from animation import *
from mappa import *
from genera_grafici import *
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path


def set_of_expirements_with_k_agents(map: np.ndarray, agents: List[Agent], total_agent_count: List[int]):
    """
        Questa funzione esegue una serie di esperimenti in cui si varia il numero k di agenti con l'algoritmo Prioritized Planning su una mappa fissa,
        (la stabilità della mappa è necessari per valutare le performance dell'algpritmo 
        al variare del numero di agenti).
        I risultati vengono poi raccolti e restituiti.
    
        Gli argomenti della funzione sono:
        -) map (np.ndarray): Mappa come array bidimensionale (0: libero, 1: ostacolo).
        -)agenti_pool (List[Any]): Lista di agenti.
        -)test_agent_counts (List[int]): Elenco dei valori di k (numero agenti) da testare.

    """
    
    results = {
        "number agents":[],
        "total cost": [],
        "running_time": [],
        "expanded_nodes": [],
        "number of success": 0,
        "number of failure":0
    }

    for k in total_agent_count:
        if k>len(agents):
            raise ValueError(
            f"Numero agenti richiesto ({k}) superiore alla dimensione del pool di agenti. "
            "Si aumenti la dimensione del pool o si riduca il numero di agenti da testare."
            "La dimensione del pool è data dal parametro max_agent(default=120)"
        )
        agents_to_test = agents[:k]
        start_time = time.time()
        pp_output = prioritized_planning(map, agents_to_test)
        end_time = time.time()
        running_time=end_time-start_time
        if pp_output is None:
            print(f"L'algoritmo PP non ha trovato nessuna soluzione valida per {k} agenti")
            results["number of failure"] += 1
        expanded_nodes,paths,cost=pp_output
       
        results["number agents"].append(k)
        results["total cost"].append(cost)
        results["running_time"].append(running_time)
        results["expanded_nodes"].append(expanded_nodes)
        results["number of success"]+=1

    return results


def parse_agent_counts(agent_counts_str: str) -> List[int]:
    """
        Questa funzione converte una stringa di numeri separati da virgola in una lista di interi.
        Tale lista rappresenta il numero degli agenti che si intende testare iterativamente.
        
        La funzione solleva un eccezione se la stringa non è nel formato corretto
        solleva un'eccezione argparse.ArgumentTypeError con un messaggio esplicativo.

    """
    try:
        return [int(x.strip()) for x in agent_counts_str.split(",") if x.strip()]
    except Exception:
        raise argparse.ArgumentTypeError("Formato agent_counts non valido. ")


def main():
    parser = argparse.ArgumentParser(description="Esegui esperimenti sul Prioritized Planning con vari agenti.")
    parser.add_argument(
        "--map_path",
        type=str,
        required=True,
        help="Percorso del file contenente la mappa"
    )
    parser.add_argument(
        "--agent_counts",
        type=parse_agent_counts,
        required=True,
        help="Lista di numeri di agenti separati da virgola che si intendono testare, ad esempio: 5,10,15"
    )
    parser.add_argument(
        "--max_agents",
        type=int,
        default=120,
        help="Numero massimo di agenti da generare nel pool (default: 120)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Seed da usare per la generazione degli agenti (default: 0)"
    )
    parser.add_argument("--show_map", action="store_true", help="Mostra la mappa statica.")
    parser.add_argument('--show_animation', action='store_true', help="Mostra l'animazione")

    args = parser.parse_args()
    map_name = Path(args.map_path).stem
    map_letta = read_map(args.map_path)
    map = create_map(map_letta)
    if args.show_map:
        plot_map(map)

    agents_pool = generate_agents(map, max_num_agents=args.max_agents, seed=0)
    
    results = set_of_expirements_with_k_agents(map, agents_pool, args.agent_counts)

    print("\nRisultati esperimenti Prioritized Planning:")
    print(f"{'Agenti':>10} | {'Costo Totale':>12} | {'Nodi Espansi':>13} | {'Tempo (s)':>10}")
    print("-" * 52)
    for k, costo, nodi, tempo in zip(results["number agents"], results["total cost"], results["expanded_nodes"], results["running_time"]):
        print(f"{k:>10} | {costo:>12.2f} | {nodi:>13} | {tempo:>10.3f}")
    
    
    genera_grafici(
        agents=results["number agents"],
        expanded_nodes=results["expanded_nodes"],
        running_time=results["running_time"],
        costo=results["total cost"],
        map_name=map_name
    )    

    genera_percentuali(
        num_agents=int(results["number agents"][-1]),
        num_failure=results["number of failure"],
        num_success=results["number of success"],
        map_name=map_name
    )
    if args.show_animation:
        last_agents = agents_pool[:args.agent_counts[-1]]
        _, paths, _ = prioritized_planning(map, last_agents)
        if paths is not None:
            plot_animation(map, last_agents, paths)
        else:
            print("Nessuna soluzione trovata, animazione non disponibile.")

if __name__ == "__main__":
    main()
