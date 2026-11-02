import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # grafo semplice
        self._idMapA = {}

    def creaGrafo(self):
        self._grafo.clear()
        self._idMapA.clear()

        artista = DAO.getAllNodes()
        for a in artista:
            self._idMapA[a.ArtistId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in artista:
            a.list_brani.clear()
            a.list_playlist.clear()
            # a.clientiPerArtista = set(DAO.getClientiPerArtista(a.ArtistId))
            a.list_brani = DAO.getBraniPerArtista(a.ArtistId)
            a.list_playlist=DAO.getPlaylistPerArtista(a.ArtistId)
           # print(a.ArtistId, a.list_playlist)
          #  a.popolarita = DAO.getPopolarita(a.ArtistId, genere)
        print("3 - Informazioni recuperate")

        for i in range(len(artista)):
            a1 = artista[i]

            for j in range(i + 1, len(artista)):
                a2 = artista[j]

                #for p in
                playlistComuni = (set(a1.list_playlist) & set(a2.list_playlist))
                #  peso = 0
                # ND: & FUNZIONA SOLO CON I SET! SE HAI LE LISTE CONSERVTILE IN SET E POI CONFRONTALE
                #  for film in  clientiComuni:
                #     incasso=DAO.getIncassiPerFilm(film)
                #    peso+=incasso[0]
                if len( playlistComuni) > 0 and a1 != a2:
                    #print(a1.ArtistId, a2.ArtistId, playlistComuni)
                    peso = len( playlistComuni)
                    self._grafo.add_edge(a1, a2, weight=peso)
        print("4 - Archi aggiunti")

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getAllNodes(self, ):
        return DAO.getAllNodes()

    def getTopArcoInc(self):
        # Attore con somma dei pesi incidenti massima
        risultati = []

        for a in self._grafo.nodes:
            grado_pesato = self._grafo.degree(a, weight="weight")
            risultati.append((a, grado_pesato))
        risultati.sort(key=lambda x: x[1], reverse=True)

        if len(risultati) == 0:
            return None
        return risultati[0]

    # GRADO MAX
    def getActorMaxDegree(self):
        if self._grafo.number_of_nodes() == 0:
            return None
        # return max(self._grafo.nodes,key=lambda a: self._grafo.degree(a)  )
        return max(self._grafo.nodes, key=lambda a: (self._grafo.degree(a)))#, a.Name))

    def getTop10Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: (x[2]["weight"] ,x[0].Name, x[1].Name),
            reverse=False  )[:10] #SE LASCIO REVERSE=TRUE ORDINO PER OORDINE ALFAB DECRESCENTE!!

    def getProdottoById(self, idP):
        return self._idMapA[int(idP)]



      #  return self._best_path, self._best_score
    def getGruppoArtisti(self, k, start_node):
        self._best_path = []
        self._best_score = float("-inf")

        parziale = [start_node]
        score = len(start_node.list_brani)

        self._ricorsione(parziale, k, score)

        return self._best_path, self._best_score

    def _ricorsione(self, parziale, k, score):
        # CASO TERMINALE
        if len(parziale) == k:
            if score > self._best_score:
                self._best_score = score
                self._best_path = list(parziale)
            return

        # CONSIDERO TUTTI I NODI
        for vicino in self._grafo.nodes:

            if vicino not in parziale:

                # Verifico che sia adiacente ad almeno un artista già selezionato
                adiacente = False

                for a in parziale:
                    if self._grafo.has_edge(a, vicino):
                        adiacente = True

                # Verifico che non ci siano archi di peso 1
                valido = True

                for a in parziale:
                    if self._grafo.has_edge(a, vicino):
                        if self._grafo[a][vicino]["weight"] == 1:
                            valido = False

                if adiacente and valido:
                    parziale.append(vicino)

                    self._ricorsione(  parziale,  k,  score + len(vicino.list_brani)
                    )

                    parziale.pop()

    def _ricorsione2(self, parziale, k,score):
        ultimo = parziale[-1]

        # Caso terminale: abbiamo raggiunto la lunghezza richiesta
        if len(parziale) == k:

            if score > self._best_score:
                self._best_score = score
                self._best_path = list(parziale)
            return

        # Se arriviamo alla destinazione troppo presto, ci fermiamo
       # if ultimo == end_node:
           # return

        # Esploro i vicini raggiungibili con un arco uscente
        for vicino in self._grafo.neighbors(ultimo):

            # Non posso visitare due volte lo stesso nodo
            if vicino not in parziale:
                # Recupero il peso dell'arco
                peso = self._grafo[ultimo][vicino]["weight"]

                # Aggiungo il vicino al percorso
                parziale.append(vicino)
                # Continuo la ricorsione aggiornando il punteggio
                self._ricorsione(parziale, k,  score + peso)
                # Tolgo il vicino per provare un'altra possibilità
                parziale.pop()
