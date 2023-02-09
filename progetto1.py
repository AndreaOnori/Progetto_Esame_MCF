
import numpy as np
import matplotlib.pyplot as plt
import math
from classi import Pixel
#costanti e randomizzazione del seed

np.random.seed()

pix=500*pow(10,-6)
A2=500*pow(10,-6)
e=1.6*pow(10,-19)
uma=1.66*pow(10,-27)
#definizione della funzione che calcola il raggio nota la massa "m", la differenza di potenziale "V" e il campo magnetico "B"
def raggio(m,V,B): 
    return 2*math.sqrt(2*m*V/(e*B**2))
#definizione dell'array delle masse (si è aggiunto il +1 per avere un array indicizzato da 0 ma con primo elemento 1 e ultimo elemento 210 come da richiesta
m=(np.arange(210)+1)*uma

#inizializzazione array di appoggio necessari al funzionamento del programma 

vmin=np.empty(0)
bmin=np.empty(0)
radiuses=np.zeros(210)
spaces=np.empty(0)
h2=np.zeros(210)

#individuazione dei campi elettrici e magnetici utilizzabili per far funzionare l'apparecchio 
for i in range(1000000):
    volt=np.random.uniform(0,1000)
    b=np.random.uniform(0,1000)
    for j in range(len(m)):
        r=raggio(m[j],volt,b)
        radiuses[j]=r
        if (j>0)&(radiuses[j]-radiuses[j-1]<2*pix):
            break
        elif(j==209)&(radiuses[j]-radiuses[j-1]>=2*pix)&(volt not in vmin)&(b not in bmin): #la scelta di utilizzare 2 pixel di distanza
            vmin=np.append(vmin,volt)                                                       #come discriminante è stata effettuata per  
            bmin=np.append(bmin,b)                                                          #evitare la condivisione di uno stesso pixel
                                                                                            #da parte di più masse

         
#creazione della matrice contenente tutti i raggi relativi alle masse delle configuazioni possibili e di quella contenente le spaziazioni tra i raggi 
raggi=np.zeros((len(m),len(vmin)))
spazi=np.zeros((len(m),len(vmin)))
medias=np.zeros(len(vmin))
for i in range(len(vmin)):
    for j in range(len(m)):
        r=raggio(m[j],vmin[i],bmin[i])
        raggi[j][i]=r
        if j!=0:
            spazi[j][i]=raggi[j][i]-raggi[j-1][i]
        medias[i]=medias[i]+spazi[j][i]

medias=medias/len(m)

#ricerca della minima media per avere la configurazione con meno spreco di spazio
minmedias=2000
mediasindex=0

for i in range(len(medias)):
    if medias[i]<minmedias:
        minmedias=medias[i]
        mediasindex=i


plt.plot(raggi[:,mediasindex],h2,'o',color='crimson')
plt.plot(raggi[:,mediasindex]+pix/2,h2,'*',color='blue')
plt.plot(raggi[:,mediasindex]-pix/2,h2,'*',color='orange')
plt.show()

#definizione del numero di pixel necessari a raccogliere le informazioni relative al rilevatore mediante l'ausilio della classe "Pixel" Presente nel file "classi.py"

spaziotot=raggi[209][mediasindex]+pix
npixel=math.ceil(spaziotot/pix)+1
pixels=[]
for i in range(npixel):
    pixels.append(Pixel(i,pix,-1))

#inizializzazione dei pixel e assegnazione a ciascuno del numero di massa corrispondente 

for i in range(len(m)):
    for j in range(len(pixels)):
        if ((raggi[i][mediasindex]-A2/2<=pixels[j].fine)&(raggi[i][mediasindex]-A2/2>pixels[j].inizio))|((raggi[i][mediasindex]+A2/2<=pixels[j].fine)&(raggi[i][mediasindex]+A2/2>pixels[j].inizio)):
            pixels[j].appartenenza=i+1

    

partenze0=np.random.uniform(-A2/2,A2/2,len(m))
#partenze0=np.ones(len(m))*(-A2/2)
raggi0=np.zeros(len(m))
for i in range(len(m)):
    raggi0[i]=raggio(m[i],vmin[mediasindex],bmin[mediasindex])+partenze0[i]
    print(raggi0[i])
for i in range(len(raggi0)):
    for j in range(len(pixels)):
        if ((raggi0[i]<=pixels[j].fine)&(raggi0[i]>pixels[j].inizio)):
            pixels[j].hit= True
            pixels[j].nhit=pixels[j].nhit+1
bins0=[]
for i in range(len(pixels)-1):
    if (pixels[i].appartenenza==pixels[i+1].appartenenza)&(pixels[i].appartenenza!=-1):
        bins0.append(pixels[i].nhit+pixels[i+1].nhit)
print(bins0)
print(len(m),len(bins0))
#for i in range(len(pixels)):
 #   print(pixels[i].appartenenza, pixels[i].nhit, pixels[i].hit)
plt.plot(m/uma,bins0,'o')
plt.show()
#reset della conta del numero degli "hit" e della variabile "hit" che verifica, come spiegato nell'altro file, se un pixel viene colpito o meno 
           
for i in range(len(pixels)):
    pixels[i].nhit=0
    pixels[i].hit= False

#generazione degli array di masse con probabilità definite per fare i test richiesti dalla consegna 1 

probgen=np.zeros(len(m))
probgen[22]=0.5
probgen[34]=0.379
probgen[36]=0.121
mtest1=np.random.choice(m,1000,p=probgen)
partenze1=np.random.uniform(-A2/2,A2/2,len(mtest1))
raggi1=np.zeros(len(mtest1))
for i in range(len(mtest1)):
    raggi1[i]=raggio(mtest1[i],vmin[mediasindex],bmin[mediasindex])+partenze1[i]
for i in range(len(raggi1)):
    for j in range(len(pixels)):
        if ((raggi1[i]<=pixels[j].fine)&(raggi1[i]>pixels[j].inizio)):
            pixels[j].hit= True
            pixels[j].nhit=pixels[j].nhit+1

         
#funzionamento vero e proprio dello spettroscopio con i valori ottimizzati e somma degli "hit" dei pixel con lo stesso valore di massa e inserzione dei valori in una lista che comprende tutte le suddette somme 
bins1=[]
for i in range(len(pixels)-1):
    if (pixels[i].appartenenza==pixels[i+1].appartenenza)&(pixels[i].appartenenza!=-1):
        bins1.append(pixels[i].nhit+pixels[i+1].nhit)
print(bins1)
print(len(m),len(bins1))
#for i in range(len(pixels)):
 #   print(pixels[i].appartenenza, pixels[i].nhit, pixels[i].hit)
#reset della conta del numero degli "hit" e della variabile "hit" che verifica, come spiegato nell'altro file, se un pixel viene colpito o meno 

for i in range(len(pixels)):
    pixels[i].nhit=0
    pixels[i].hit= False

#generazione degli array di masse con probabilità definite per fare i test richiesti dalla consegna 2 
probgen2=np.zeros(len(m))
probgen2[196]=0.0015
probgen2[198]=0.0985
probgen2[199]=0.169
probgen2[200]=0.231
probgen2[201]=0.132
probgen2[202]=0.299
probgen2[204]=0.069
mtest2=np.random.choice(m,10000,p=probgen2)
partenze2=np.random.uniform(-A2/2,A2/2,len(mtest2))
raggi2=np.zeros(len(mtest2))
for i in range(len(mtest2)):
    raggi2[i]=raggio(mtest2[i],vmin[mediasindex],bmin[mediasindex])+partenze2[i]
for i in range(len(raggi2)):
    for j in range(len(pixels)):
        if ((raggi2[i]<=pixels[j].fine)&(raggi2[i]>pixels[j].inizio)):
            pixels[j].hit= True
            pixels[j].nhit=pixels[j].nhit+1
#funzionamento vero e proprio dello spettroscopio con i valori ottimizzati e somma degli "hit" dei pixel con lo stesso valore di massa e inserzione dei valori in una lista che comprende tutte le suddette somme 
bins2=[]
for i in range(len(pixels)-1):
    if (pixels[i].appartenenza==pixels[i+1].appartenenza)&(pixels[i].appartenenza!=-1):
        bins2.append(pixels[i].nhit+pixels[i+1].nhit)
print(bins2)
print(len(m),len(bins2))

#for i in range(len(pixels)):
 #   print(pixels[i].appartenenza, pixels[i].nhit, pixels[i].hit)
