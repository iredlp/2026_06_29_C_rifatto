import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        try:
            self._model.creaGrafo()
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            self.fillDDArtisti()
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        # ATTORE CON GRADO MAX
        artist_degree = self._model.getActorMaxDegree()
        self._view._txt_result.controls.append(
            ft.Text(f"ARTISTA con grado maggiore: {artist_degree.Name} "
                    f"(grado: {self._model._grafo.degree(artist_degree)})"))

        # C) 5 ARCHI CON PESO MAGGIORE SORT
        top = self._model.getTopArcoInc()
        if top is not None:
            attore, peso = top
            self._view._txt_result.controls.append(
                ft.Text( f"ARTISTA con somma pesi incidenti massima: "
                    f"{attore.Name} (somma: {peso})")
            )

        top10= self._model.getTop10Archi()
        self._view._txt_result.controls.append(ft.Text(f"Archi di peso maggiore", color="green"))

        for i, arco in enumerate(top10, start=1):
            a1, a2, dati = arco
            self._view._txt_result.controls.append(ft.Text(
                f"{i})  {a1.Name}   -- {a2.Name}  "
                f"(Playlist condivise: {dati['weight']})")
            )
        self._view.update_page()

    def fillDDArtisti(self):
        try:
            self._view._ddArtista.options.clear()
            attori = self._model.getAllNodes()
            for actor in attori:
                self._view._ddArtista.options.append(ft.dropdown.Option(key=actor.ArtistId,
                                                                         text=actor.Name))
        # self._view.update_page()
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero degli ARTISTI: {ex}", color="red"))

        self._view.update_page()

    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()
        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return

        k = self._view._txtInN.value
        # qui dovremmo fare i solti controlli sulla validità
        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red"))
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.create_alert(
                "La soglia deve essere un intero positivo.", color="red")
            return

        start = self._model.getProdottoById(self._view._ddArtista.value)
        #end = self._model.getProdottoById(self._view._ddProdEnd.value)
        # qui dovremmo fare i solti controlli sulla validità

        if start is None :
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire i nodi iniziali   per procedere!", color="red")
            )
            self._view.update_page()
            return

        gruppo, punteggio = self._model.getGruppoArtisti(kInt, start)
        gruppo.sort(key=lambda x: x.Name) #ORDINE ALFABETICO!
        if len(gruppo) < kInt:
            self._view._txt_result.controls.append(
                ft.Text("Non esiste una selezione valida di K artisti."))
            return

        self._view._txt_result.controls.append(
            ft.Text(f"numero totale di artisti selezionati: {len(gruppo)}"))

        for prodotto in gruppo:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{prodotto.Name} - "
                    f" che compare in {len(prodotto.list_playlist)} playlist e {len(prodotto.list_brani)} brani") )
        tot=0
        for prodotto in gruppo:
            tot+=len(prodotto.list_brani)

        self._view._txt_result.controls.append( ft.Text(
                    f"Totale di brani della soluzione ottime: {tot}"))

        self._view.update_page()