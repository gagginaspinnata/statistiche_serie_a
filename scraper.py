#! /usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

class Scraper:

    serie_a_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/seriea/calendario_'
    serie_a_corrente_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/seriea/index.shtml'

    premier_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/premierleague/calendario_'
    premier_corrente_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/premierleague/risultati.shtml'

    liga_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/liga/calendario_'
    liga_corrente_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/liga/risultati.shtml'

    bundes_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/bundesliga/calendario_'
    bundes_corrente_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/bundesliga/risultati.shtml'

    legue1_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/ligue1/calendario_'
    legue1_corrente_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/ligue1/risultati.shtml'



    def __init__(self, league='serie_a'):

        if(league=='serie_a'):
            self.base_url = self.serie_a_url
            self.corrente_url = self.serie_a_corrente_url
        elif (league == 'premier'):
            self.base_url = self.premier_url
            self.corrente_url = self.premier_corrente_url
        elif league == 'liga':
            self.base_url = self.liga_url
            self.corrente_url = self.liga_corrente_url
        elif league == 'bundes':
            self.base_url = self.bundes_url
            self.corrente_url = self.bundes_corrente_url
        elif league == 'legue1':
            self.base_url = self.legue1_url
            self.corrente_url = self.legue1_corrente_url


        self.squadre = self.array_squadre(self.corrente_url)

        # imposta il numero di giornate giocate
        self.giornate = self.giornata_corrente()

        self.calendario = self.calcola_giornate()

        # print json.dumps(self.squadre_senza_pareggi())



    # returna an array with the teams and from how many match they does not draw
    def squadre_senza_pareggi(self):
        ris = []
        for squadra in self.squadre:
            d = {}
            risultati = self.risultati_squadra(squadra)
            pareggio_mancante = self.pareggio_mancante_da(risultati)
            d['squadra'] = squadra
            d['x'] = pareggio_mancante

            ris.append(d)
        return ris


    # funzione che data una squadra ritorna i suoi risultati in una forma di array. p = persa, v = vinta, x = pareggiata
    # Da notare che prima di lanciare questa funzione è necessario che venga lanciata la funzione calcola_giornate()
    def risultati_squadra(self, squadra):

        risultati = []

        for giornata in self.calendario:

            for partita in giornata:

                if(partita['squadra_1'] == squadra):

                    if partita['risultato_1'] > partita['risultato_2']:
                        risultati.append('v')
                    elif partita['risultato_2'] > partita['risultato_1']:
                        risultati.append('p')
                    else:
                        risultati.append('x')

                elif (partita['squadra_2'] == squadra):

                    if partita['risultato_1'] < partita['risultato_2']:
                        risultati.append('v')
                    elif partita['risultato_2'] < partita['risultato_1']:
                        risultati.append('p')
                    else:
                        risultati.append('x')

                # if(partita['squadra_1'] == squadra or partita['squadra_2'] == squadra):

                #     print partita['squadra_1'] + ' vs ' + partita['squadra_2'] + ' ' + str(partita['risultato'])
                #     risultati.append(partita['risultato'])

        return risultati


    # ritorna da quante giornate una squadra non pareggia
    def pareggio_mancante_da(self, risultati):

        x = 0

        for ris in reversed(risultati):
            if ris != 'x':
                x = x +1
            else:
                break

        return x


    # ritorna il numero dell'ultima giornata giocata
    def giornata_corrente(self):

        soup = BeautifulSoup(self.get_source(self.corrente_url))
        return  int(soup.select('.current1')[0].string)


    # funzione che ritorna un array contenente tutti i risultati di tutte le giornate
    def calcola_giornate(self):

        calendario = []

        for giornata in range(1, self.giornate + 1):
            url =self.base_url + str(giornata) + '.shtml'
            calendario.append(self.calcola_giornata(url, giornata))

        return calendario


    # funzione che ritorna i risultati di una giornata
    def calcola_giornata(self,url, giornata):


        # Creo l'oggetto necessario a beautifulsoup
        self.soup = BeautifulSoup(self.get_source(url))

        partite = self.soup.select('.giornata-campionato > li')

        g = []

        for partita in partite:
            ris = {}
            ris['giornata'] = giornata
            ris['squadra_1'] =  partita.select('.prima_squadra > a')[0].string
            ris['squadra_2'] =  partita.select('.seconda_squadra > a')[0].string
            ris['risultato_1'] = partita.select('.primo_risultato')[0].string
            ris['risultato_2'] = partita.select('.secondo_risultato')[0].string
            ris['data'] = partita.select('.giorno')[0].string

            if(ris['risultato_1'] == ris['risultato_2']):
                ris['risultato'] = 'x'
            elif(ris['risultato_1'] > ris['risultato_2']):
                ris['risultato'] = 1
            else:
                ris['risultato'] = 2
            g.append(ris)

        return g


    # Funzione che ritorna il sorgente della pagina
    def get_source(self,url):

        r = requests.get(url)
        return r.content


    # Ritorna il sorgente, come sopra, solo che lo fa in maniera pretty (più leggibile)
    def pretty_source(self):

        source = self.get_source()
        pretty_source = BeautifulSoup(source).prettify()
        return pretty_source

    # returns an array containing all the teams from a league
    def array_squadre(self, url):

        soup = BeautifulSoup(self.get_source(url))
        result = []
        for squadra in soup.select('.prima_squadra > a'):
            result.append(squadra.string)

        for squadra in soup.select('.seconda_squadra > a'):
            result.append(squadra.string)

        return result


scraper = Scraper('legue1')
print scraper.squadre_senza_pareggi()
