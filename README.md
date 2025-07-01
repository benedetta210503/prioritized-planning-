# prioritized-planning for solving MAPF-
Questa repository contiene il codice implementato per il problema di Prioritized Planning per risolvere istanze del problema Multi-Agent PathFindinng(MAPF).
L’algoritmo prioritizza la pianificazione dei percorsi degli agenti in modo sequenziale, garantendo la generazione di soluzioni collision-free in maniera efficiente.
I conflitti di cui si è tenuto conto sono il vertex conflict(quando due agenti si trovano nella stessa cella nello stesso istante di tempo) e lo swapping conflict(quando due agenti percorrono lo stesso arco in due direzioni opposte).
Oltre a questo algoritmo è presente anche il codice per eseguire l'animazione dei percorsi trovati per i vari agenti nei vari istanti di tempo.
Gli agenti appariranno colorati con diversi colori e avranno lo stesso colore del relativo Starting Point(la posizione iniziale di partenza)che nell' animazione apparirà sottoforma quadrato, e della posizione terminante, che nell'animazione apparirà come una X.
Sono poi mantenute alcune dei principali AI benchmarks per verificare l'efficienza dell'algoritmo e le soluzioni trovate.
In particolare, l'obiettivo è valutare le performance e la scalabilità dell’algoritmo al variare del numero di agenti.

## Requisiti
Vengono qui elencate le librerie necessarie per garantire il corretto funzionamento del progetto.
- Python 3.7 o superiore
- Librerie Python:
  - numpy
  - matplotlib
  - argparse
    
E' possibile installare le suddette librerie tramite il comando:

 ```bash
pip install numpy matplotlib argparse
---
## Utilizzo
Per poter lanciare gli esperimenti è necessario eseguire il comando:
 ```bash
python main.py --map_path path/to/map.file --agent_counts 1,2,3 --show_map --show_animation

Viene fornita ora una spiegazione del comando:
-)--map_path: si deve specificare il percorso della mappa che si intende testare
-)--agent_counts: è una lista di valori interi che indica i vari agenti che si vogliono testare(nell'esempio 1, 2 e 3)
-)--show_map: è un flag opzionale per visualizzare la mappa
-)--show_animation: è un flag opzionale per visualizzare l'animazione, quindi il movimento degli agenti nel tempo



