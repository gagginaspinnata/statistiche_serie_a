#! /usr/bin/env python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

class Scraper:

    base_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/seriea/calendario_'
    corrente_url = 'http://www.gazzetta.it/speciali/risultati_classifiche/2014/calcio/seriea/index.shtml'

    def __init__(self):
        
        # imposta il numero di giornate giocate
        self.giornate = int(self.giornata_corrente())

        calendario = self.calcola_giornate()

        print json.dumps(calendario)


    # ritorna il numero dell'ultima giornata giocata
    def giornata_corrente(self):

        soup = BeautifulSoup(self.get_source(self.corrente_url))
        return  soup.select('.current1')[0].string


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


scraper = Scraper()