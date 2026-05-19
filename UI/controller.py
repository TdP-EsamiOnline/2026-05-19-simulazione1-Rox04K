import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._genre = None
        self._artist = None

    def fillDDGenre(self):
        generi = self._model.getGeneri()

        generiDD = list(map(lambda x: ft.dropdown.Option(
            text=x.Name,
            data=x,
            on_click=self._readGenre
        ), generi))

        self._view._ddGenre.options = generiDD

    def _readGenre(self, e):
        if e.control.data is None:
            self._genre = None
        else:
            self._genre = e.control.data
            print(self._genre)

    def handleCreaGrafo(self, e):
        genere = self._genre.GenreId
        print(genere)
        if genere is None:
            self._view.create_alert('Selezionare un genere!')
            return

        self._view._txtResult.controls.clear()
        self._model.creaGrafo(genere)
        self._view._txtResult.controls.append(ft.Text('Grafo correttamente creato:'))

        nodi, archi = self._model.getInfo()
        self._view._txtResult.controls.append(ft.Text(f'Numero di nodi: {nodi}'))
        self._view._txtResult.controls.append(ft.Text(f'Numero di archi: {archi}:'))

        artista = self._model.getArtista()
        self._view._txtResult.controls.append(ft.Text(f'Artista più influente: {artista['autore']}, con influenza: {artista['influenza']}'))

        migliori = self._model.getArchi()
        self._view._txtResult.controls.append(ft.Text('Top 5 archi:'))
        for u,v,data in migliori:
            self._view._txtResult.controls.append(ft.Text(f'{u} -> {v} : {data.get('weight')}'))

        nodes = self._model.getNodi()
        nodiDD = list(map(lambda x: ft.dropdown.Option(
            text=x.Name,
            data=x,
            on_click=self._readArtist
        ), nodes))

        self._view._ddArtist.options = nodiDD
        self._view.update_page()

    def _readArtist(self, e):
        if e.control.data is None:
            self._artist = None
        else:
            self._artist = e.control.data
            print(self._artist)

    def handleCammino(self,e):
        artist = self._artist
        if artist is None:
            self._view.create_alert('Selezionare un artista!')
            return

        self._view._txtResult.controls.clear()

        cammino = self._model.cercaCamminoLungo(artist)
        self._view._txtResult.controls.append(ft.Text(f'Ho trovato un cammino lungo {len(cammino)}'))
        for c in cammino:
            self._view._txtResult.controls.append(ft.Text(f'{c}'))

        self._view.update_page()