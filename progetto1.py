
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

    
#porzione di codice che permette la verifica mediante un solo hit da parte di tutte le masse dalla partenza casuale, di verificare che tutti i colpi vengano registrati e sommati correttamente
partenze0=np.random.uniform(-A2/2,A2/2,len(m))
raggi0=np.zeros(len(m))
for i in range(len(m)):
    raggi0[i]=raggio(m[i],vmin[mediasindex],bmin[mediasindex])+partenze0[i]
for i in range(len(raggi0)):
    for j in range(len(pixels)):
        if ((raggi0[i]<=pixels[j].fine)&(raggi0[i]>pixels[j].inizio)):
            pixels[j].hit= True
            pixels[j].nhit=pixels[j].nhit+1
bins0=[]
for i in range(len(pixels)-1):
    if (pixels[i].appartenenza==pixels[i+1].appartenenza)&(pixels[i].appartenenza!=-1):
        bins0.append(pixels[i].nhit+pixels[i+1].nhit)

#Grafico che mostra l'efficienza dello script mostrando che ogni hit viene registrato una volta per massa 
plt.plot(m/uma,bins0,'o',color='crimson')
plt.xlabel('Masse [uma]')
plt.ylabel('Numero di hit')
plt.title('Verifica che tutte le masse abbiano un hit')
plt.show()

#reset della conta del numero degli "hit" e della variabile "hit" che verifica, come spiegato nell'altro file, se un pixel viene colpito o meno 
           
for i in range(len(pixels)):
    pixels[i].nhit=0
    pixels[i].hit= False


#generazione degli array di masse con probabilità definite per fare i test al variare dei valori ottimizzati 

probgen=np.zeros(len(m))
probgen[99]=0.5
probgen[101]=0.5
mtest05=np.random.choice(m,1000,p=probgen)
partenze05=np.random.uniform(-A2/2,A2/2,len(mtest05))
raggi05=np.zeros(len(mtest05))
vminmod=np.ones(3)*vmin[mediasindex]
bminmod=np.ones(3)*bmin[mediasindex]
appoggio=np.arange(len(pixels))+1

for k in range(len(vminmod)):
    bins05=np.zeros(len(pixels))     
    bins051=[]
    vminmod[k]=vminmod[k]+(k+2)     #spostamento del voltaggio attorno al valore ottimizzato
    bminmod[k]=bminmod[k]+(k+1)*0.2 #spostamento del campo magntico attorno al valore ottimizzato 
    for i in range(len(mtest05)):
        raggi05[i]=raggio(mtest05[i],vminmod[k],bminmod[k])+partenze05[i]
    for n in range(len(raggi05)):
        for j in range(len(pixels)):
            if ((raggi05[n]<=pixels[j].fine)&(raggi05[n]>pixels[j].inizio)):
                pixels[j].hit= True
                pixels[j].nhit=pixels[j].nhit+1
    for n in range(len(pixels)-1):
            bins05[n]=pixels[n].nhit
    for l in range(len(pixels)-1):
        if (pixels[l].appartenenza==pixels[l+1].appartenenza)&(pixels[l].appartenenza!=-1):
            bins051.append(pixels[l].nhit+pixels[l+1].nhit)
    #grafici dei risultati non ottimizzati di volta in volta 
    fig,ax = plt.subplots(1,2, figsize=(12,6) )

    ax[0].plot(appoggio, bins05, 'o', color='blue')
    ax[1].plot(m/uma, bins051, '*',  color='red'  )

    ax[0].set_title('Pixel colpiti in generale')
    ax[1].set_title('Pixel relativi alle masse colpiti')

    ax[0].set_xlabel('Pixel')
    ax[0].set_ylabel('Numero di hit')

    ax[1].set_xlabel('Masse [uma]')
    ax[1].set_ylabel('Numero di hit')
    
    plt.show()
    
    for s in range(len(pixels)):
        pixels[s].nhit=0
        pixels[s].hit= False




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
plt.plot(m/uma,bins1,'*',color='orange')
plt.xlabel('m [uma]')
plt.ylabel('numero di hit')
plt.title('Risultati del test con NaCl')
plt.show()

#reset della conta del numero degli "hit" e della variabile "hit" che verifica, come spiegato nell'altro file, se un pixel viene colpito o meno 

for i in range(len(pixels)):
    pixels[i].nhit=0
    pixels[i].hit= False

    

#generazione degli array di masse con probabilità definite per fare i test richiesti dalla consegna 2 
probgen2=np.zeros(len(m))
probgen2[195]=0.0015
probgen2[197]=0.0985
probgen2[198]=0.169
probgen2[199]=0.231
probgen2[200]=0.132
probgen2[201]=0.299
probgen2[203]=0.069
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

plt.plot(m/uma,bins2,'*',color='limegreen')
plt.xlabel('m [uma]')
plt.ylabel('numero di hit')
plt.title('Risultati del test con gli isotopi di Hg')
plt.show()

abbis23=bins1[22]
abbis35=bins1[34]
abbis37=bins1[36]

abbis196=bins2[195]
abbis198=bins2[197]
abbis199=bins2[198]
abbis200=bins2[199]
abbis201=bins2[200]
abbis202=bins2[201]
abbis204=bins2[203]

print(abbis23,abbis35,abbis37,abbis196,abbis198,abbis199,abbis200,abbis201,abbis202,abbis204)

file_scrittura=open("Risultati.txt","w")
l1="Il file presenta i risultati dei test con i valori ottimizzati e le abbondanze isotopiche relative ai due casi da analizzare, i dati sono riportati in percentuale."
l2="Abbondanze isotopiche NaCl:"
l3="Na23:"
l4="Cl35:"
l5="Cl37:"
l6="Abbondanze isotopiche Hg:"
l7="Hg196:"
l8="Hg198:"
l9="Hg199:"
l10="Hg200:"
l11="Hg201:"
l12="Hg202:"
l13="Hg204:"
file_scrittura.writelines([l1,"\n",l2,"\n",l3,"\n",str(abbis23/10),"\n",l4,"\n",str(abbis35/10),"\n",l5,"\n",str(abbis37/10),"\n",l6,"\n",l7,"\n",str(abbis196/100),"\n",l8,"\n",str(abbis198/100),"\n",l9,"\n",str(abbis199/100),"\n",l10,"\n",str(abbis200/100),"\n",l11,"\n",str(abbis201/100),"\n",l12,"\n",str(abbis202/100),"\n",l13,"\n",str(abbis204/100),"\n"])
file_scrittura.close()
