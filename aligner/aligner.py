from simeval import SimEval


class ObjectAligner:
    """Align lists of objects"""

    def __init__(self, simEval=SimEval(), gapPenalty=-1.0, nullObj=None):
        self.vect1 = []
        self.vect2 = []
        self.vect3 = []
        self.simEval = simEval
        self.gapPenalty = gapPenalty
        self.nullObj = nullObj

    def align(self, objs1, objs2):
        """
        Allinea le due stringhe secondo l'algoritmo Needleman-Wunsch
        I due parametri objs1, objs2 sono le due stringhe da allineare. In particolare, objs2 è la stringa che viene posta "sopra" la matrice,
        objs1 è la stringa che viene posta alla sinistra della matrice.

        simMatrix assegna alle cellette "interne" il valore del match o mismatch (nel caso specifico di questa implementazione viene usato un valutatore differente): 
        questa non è la matrice finale, né intera, ma viene usata per calcolare
        il valore dello spostamento in diagonale alla riga 78 (e quindi sapere, se in quella celletta, c'è stato un match o mismatch).
        matrix è invece la matrice per intera, che verrà riempita con i valori ottenuti dagli spostamenti.
        In particolare, ha un numero di righe e colonne di uno superiore al numero di caratteri
        di cui sono composte le stringhe (ecco perché viene aggiunto 1 al risultato di len(objs2) e len(objs1)).
        
        La matrice viene rappresentata come un array di array (lista di liste), esempio:

        [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]] 

        In cui possiamo riconoscere le righe e le colonne
        """
        
        # Similarity matrix
        # Crea una riga di [0.0] lunga quant'è lunga la stringa in objs2. 
        # L'operazione viene ripetuta per quant'è lunga la objs1 (forma quindi tante righe per quante colonne sono necessarie)
        simMatrix = [[0.0] * len(objs2) for i in range(len(objs1))]  
        matrix = [[0.0] * (len(objs2)+1) for i in range((len(objs1)+1))]
        for i in range(len(objs1)):
            """
            Per la lunghezza di objs1 (la stringa a sinistra della matrice), assegna un valore alla celletta di simMatrix.
            Il valore viene assegnato in base al match o mismatch.
            Dunque i ci dice a quale riga siamo (es. al primo giro del ciclo, siamo alla prima riga); j ci dice 
            a quale colonna stiamo: mentre siamo alla prima riga, dovremo calcolare il valore di diverse cellette (spostandoci quindi a confrontare
            la prima lettera di objs1 con tutte le lettere di objs2). Quante "diverse" cellette, ce lo dice j
            """
            for j in range(len(objs2)):
                simMatrix[i][j]=self.simScore(objs1[i],objs2[j])

        # usciti dal loop abbiamo la nostra simMatrix completa, con i valori calcolati per ogni celletta
        matrix[0][0] = 0.0
        # Fill matrix marginals
        for i in range(1,len(objs1)+1):
            """
            Per ogni numero i compreso fra 1 e la lunghezza della stringa a sinistra della matrice, inseriamo, di volta in volta,
            il valore i moltiplicato per il gap score. Andiamo quindi a riempire il gap score in colonna   
            """
            matrix[i][0] = i * self.gapPenalty
        for j in range(1,len(objs2)+1):
            # Facciamo lo stesso di sopra, per il gap score in riga
            matrix[0][j] = j * self.gapPenalty

        scoreDown = 0.0
        scoreRight = 0.0
        scoreDiag = 0.0
        bestScore = 0.0
        #Fill matrix
        for i in range(1, len(objs1)+1):
            for j in range(1, len(objs2)+1):
                scoreDown = matrix[i-1][j] + self.gapPenalty  # Prende il valore sopra e aggiunge il gap score
                scoreRight = matrix[i][j-1] + self.gapPenalty  # Prende il valore precedente e aggiunge il gap score
                scoreDiag = matrix[i-1][j-1] + simMatrix[i-1][j-1]  # Prende il valore in diagonale e aggiunge il valore ottenuto dalla matrice di similarità
                bestScore = max(scoreDown,scoreRight,scoreDiag)  # Prende il valore massimo fra quelli precedenti
                matrix[i][j] = bestScore  # assegna il valore massimo alla celletta presa in considerazione

        # Usciti dal ciclo, abbiamo la matrice completamente riempita dei valori migliori per ogni celletta
        # Andiamo ora a prendere i valori migliori per ogni riga, risultati dalla computazione precedente
        i = len(objs1)
        j = len(objs2)
        nullScore = 0.0
        score = 0.0
        scoreLeft = 0.0
        scoreDiagInv = 0.0
        while i > 0 and j > 0:
            score = matrix[i][j]
            scoreDiagInv = matrix[i-1][j-1]
            scoreLeft = matrix[i-1][j]  # Questo è lo score di sopra?
            
            """
            ita: "se lo score della celletta X in considerazione è uguale al punteggio ottenuto sommando
            lo score presente nella cella in alto a sinistra (in diagonale verso l'alto) + il valore di match/mismatch
            presente nella celletta X, allora viene fatto un allineamento fra i due caratteri delle stringhe.
            Il fatto che venga sottratto 1 alle variabili i e j è dovuto al fatto che il primo carattere di una stringa si trova all'indice 0.
            Non farlo, porterebbe a ciò che viene chiamato un "off by one error"
            
            es, con str1 = "casa" e gap score = -2: 
            se mettiamo casa "a sinistra della matrice", la matrice avrà all'indice 0 lo 0, all'indice 1 la C con valore -2,
            all'indice 2 la A con valore -4 ecc. Quando consideriamo la matrice per intero dunque, l'ultima A di casa si troverà
            all'indice 4. Se però consideriamo la stringa in sé per sé, come quando viene "estratto" un carattere tramite lo "slicing",
            l'ultima A si trova all'indice 3, poiché la prima C si trova all'indice 0.
            es: str1[0] sarà C, str1[1] sarà A, str1[2] sarà S, str[3] sarà A
            """
            if score == scoreDiagInv+simMatrix[i-1][j-1]:
                self.__makeAlignment(objs1[i-1], objs2[j-1], simMatrix[i-1][j-1])
                i = i-1
                j = j-1
            elif score == scoreLeft+self.gapPenalty:
                # Se lo score migliore è provenuto da uno spostamento verso l'alto, mettiamo un gap nella stringa 2
                # Diminuiamo i di uno per salire al rigo sopra, ma j rimane costante perché rimaniamo sulla stessa colonna
                self.__makeAlignment(objs1[i-1], self.nullObj, nullScore)
                i = i-1
            else:
                # In questo caso, la scelta è provenuta da uno spostamento verso sinistra, per cui mettiamo il gap nella stringa 1
                # e dimuniamo j di uno per spostarci di una colonna verso sinistra. i rimane costante perché rimaniamo sullo stesso rigo
                self.__makeAlignment(self.nullObj, objs2[j-1], nullScore)
                j = j-1

        """
        Se nel ciclo while precedente ci sono stati diversi gap, le variabili i e j non sono ancora arrivate a 0,
        ovvero, non abbiamo finito di allineare le due stringhe: se i è maggiore di 0, vuol dire che ci sono degli
        spostamenti verso l'alto da compiere (cioè bisogna inserire un gap nella seconda stringa). Al contrario, se j
        è maggiore di 0, vuol dire che dobbiamo compiere degli spostamenti verso sinistra, quindi inserire dei gap
        nella prima stringa (quella a sinistra della matrice)
        """
        while i > 0:
            self.__makeAlignment(objs1[i-1], self.nullObj, nullScore)
            i = i-1
        while j > 0:
            self.__makeAlignment(self.nullObj, objs2[j-1], nullScore)
            j = j-1
        return self.__makeResult()  # ritorniamo i risultati

    def simScore(self, obj1, obj2):
        """
        calcola lo score di similarità per ogni celletta in base al valutatore di similarità passato in __init__
        Non è strettamente necessario andare a leggere il codice di SimEval per capire questo codice.
        Il sorgente di SimEval si trova in simeval.py, in particolare riga 20 per il valutatore usato di default in run.py
        """
        return self.simEval.eval(obj1, obj2)

    def __makeAlignment(self, obj1, obj2, score):
        """
        esegue l'allineamento: i caratteri ricevuti in obj1 e obj2 vengono "appesi", cioè messi alla fine della lista chiamata vect1 e vect2.
        vect3 ci dice invece se in questo caso c'è stato un match o un mismatch
        """
        self.vect1.append(obj1)
        self.vect2.append(obj2)
        self.vect3.append(score)

    def __makeResult(self):
        """
        ritorna i tre vettori che conterranno le due stringhe allineate più lo score
        """
        self.vect1 = list(reversed(self.vect1))
        self.vect2 = list(reversed(self.vect2))
        self.vect3 = list(reversed(self.vect3))
        return (self.vect1, self.vect2, self.vect3)
