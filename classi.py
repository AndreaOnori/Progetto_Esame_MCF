import numpy as np

class Pixel():

    def __init__(self,pos,pix,numeropixel):
        self.posizione= pos
        self.inizio=pos*pix-pix
        self.fine=pos*pix
        self.appartenenza= numeropixel
        self.nhit=0
        self.hit= False 




