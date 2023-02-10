import numpy as np
#in questo file si crea la classe pixel necessaria al corretto funzionamento delprogramma principale, come variabili necessita la posizione del pixel, la larghezza e il valore di default di non appatenenza in "numeropixel". Presenta anche la classe numero hit inizializzata a zero e la variabile booleana hit per verificare l'effettivo impatto.
class Pixel():

    def __init__(self,pos,pix,numeropixel):
        self.posizione= pos
        self.inizio=pos*pix-pix
        self.fine=pos*pix
        self.appartenenza= numeropixel
        self.nhit=0
        self.hit= False 




