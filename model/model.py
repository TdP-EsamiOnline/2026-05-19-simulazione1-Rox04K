import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._mapArtist = {}

        self._bestCammino = []

    def getGeneri(self):
        generi = DAO.getGeneri()
        generi.sort(key=lambda x: x.GenreId)
        return generi

    def creaGrafo(self, genere):
        self._grafo.clear()
        self._mapArtist = {}

        nodi = DAO.getNodi(genere)
        self._grafo.add_nodes_from(nodi)
        for n in nodi:
            self._mapArtist[n.ArtistId] = n

        self._addEdges(genere)

    def _addEdges(self, genere):
        popolarita = DAO.getPopolarita(self._mapArtist, genere)

        collegamenti = DAO.getArchi(self._mapArtist, genere)

        for c in collegamenti:
            u = c[0]
            v = c[1]
            p1 = popolarita[u]
            p2 = popolarita[v]
            peso = p1 + p2

            if p1 > p2:
                self._grafo.add_edge(u,v,weight=peso)
            elif p1 < p2:
                self._grafo.add_edge(v,u,weight=peso)
            else:
                self._grafo.add_edge(u,v,weight=peso)
                self._grafo.add_edge(v,u,weight=peso)

    def getInfo(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getArtista(self):
        nodi = self._grafo.nodes()
        influenza = []
        for n in nodi:
            archiEntranti = list(self._grafo.in_edges(n, data=True))
            archiUscenti = list(self._grafo.out_edges(n, data=True))

            sommaEntranti = 0
            sommaUscenti = 0

            for u,v,data in archiEntranti:
                sommaEntranti += data.get('weight')

            for u,v,data in archiUscenti:
                sommaUscenti += data.get('weight')

            inf = sommaUscenti-sommaEntranti
            influenza.append({
            'autore': n,
            'influenza': inf
            })

        influenza.sort(key=lambda x: x['influenza'], reverse=True)
        return influenza[0]

    def getArchi(self):
        archi = list(self._grafo.edges(data=True))

        archi.sort(key=lambda x: x[2]['weight'], reverse=True)
        return archi[:5]

    def getNodi(self):
        return list(self._grafo.nodes())

    def cercaCamminoLungo(self, source):
        parziale = [source]
        self._bestCammino = []

        self._ricorsione(parziale, 0)

        return self._bestCammino

    def _ricorsione(self, parziale, peso):
        source = parziale[-1]
        vicini = list(self._grafo.neighbors(parziale[-1]))

        if len(parziale) > len(self._bestCammino):
            self._bestCammino = copy.deepcopy(parziale)

        for v in vicini:
            if v not in parziale:
                pesoAttuale = self._grafo[source][v]['weight']
                if pesoAttuale > peso:
                    parziale.append(v)
                    self._ricorsione(parziale, pesoAttuale)
                    parziale.pop()
