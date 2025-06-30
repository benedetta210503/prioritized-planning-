# prioritized-planning-
Questa repository contiene il codice implementato per il problema di Prioritized Planning per risolvere istanze del problema Multi-Agent PathFindinng(MAPF).
L’algoritmo prioritizza la pianificazione dei percorsi degli agenti in modo sequenziale, garantendo la generazione di soluzioni collision-free in maniera efficiente.
I conflitti di cui si è tenuto conto sono il vertex conflict(quando due agenti si trovano nella stessa cella nello stesso istante di tempo) e lo swapping conflict(quando due agenti percorrono lo stesso arco in due direzioni opposte).
Oltre a questo algoritmo è presente anche il codice per eseguire l'animazione dei percorsi trovati per i vari agenti nei vari istanti di tempo.
Gli agenti appariranno colorati con diversi colori e avranno lo stesso colore del relativo Starting Point(la posizione iniziale di partenza)che nell' animazione apparirà sottoforma quadrato, e della posizione terminante, che nell'animazione apparirà come una X.
Sono poi mantenute alcune dei principali AI benchmarks per verificare l'efficienza dell'algoritmo e le soluzioni trovate.
