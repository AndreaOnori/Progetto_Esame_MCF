import numpy as np
import matplotlib.pyplot as plt
import math
from classi import Pixel
#costanti

np.random.seed()

pix=500*pow(10,-6)
A2=500*pow(10,-6)
e=1.6*pow(10,-19)
uma=1.66*pow(10,-27)

def raggio(m,V,B):  #raggio nota la massa
    return math.sqrt(2*m*V/(e*B**2))

def massa(r,V,B):   #massa noto il raggio
    return e*r**2*B**2/(2*V)

#randomizzazione di V e B
#volt=np.random.uniform(0.01,100)
#b=np.random.uniform(0.01,100)
#print(volt,b)

#randomizzazione masse
#m=(np.random.randint(1,210,500)+1)*uma
m=(np.arange(210)+1)*uma

vmin=np.empty(0)
bmin=np.empty(0)
spaces=np.empty(0)
radiuses=np.zeros(210)
spaces=np.empty(0)
h1=np.ones(420)
h2=np.zeros(210)


#voltaggi esistenti
for i in range(1000000):
    volt=np.random.uniform(0,1000)
    b=np.random.uniform(0,1000)
    for j in range(len(m)):
        r=raggio(m[j],volt,b)
        radiuses[j]=r
        if (j>0)&(radiuses[j]-radiuses[j-1]<2*pix):
            break
        elif(j==209)&(radiuses[j]-radiuses[j-1]>=2*pix)&(volt not in vmin)&(b not in bmin):
            vmin=np.append(vmin,volt)
            bmin=np.append(bmin,b)

print(vmin)
print(bmin)
print(len(vmin),len(bmin))

         
#media dei voltaggi e spaziazione 
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


print(raggi)
print(spazi)
#print(raggi[0][0])
#print(vmin,bmin,spaces)
print(len(vmin),len(bmin),len(spaces))

print(medias)
#media minima per ottimizzare le distanze 
minmedias=2000
mediasindex=0

for i in range(len(medias)):
    if medias[i]<minmedias:
        minmedias=medias[i]
        mediasindex=i
print(minmedias,mediasindex,vmin[mediasindex],bmin[mediasindex])


plt.plot(raggi[:,mediasindex],h2,'o',color='crimson')
plt.plot(raggi[:,mediasindex]+pix/2,h2,'*',color='blue')
plt.plot(raggi[:,mediasindex]-pix/2,h2,'*',color='orange')
plt.show()

spaziotot=raggi[209][mediasindex]+pix
npixel=math.ceil(spaziotot/pix)
print(npixel)
pixels=[]
for i in range(npixel):
    pixels.append(Pixel(i,pix,-1))

for i in range(len(m)):
    for j in range(len(pixels)):
        if ((raggi[i][mediasindex]-A2/2<=pixels[j].fine)&(raggi[i][mediasindex]-A2/2>pixels[j].inizio))|((raggi[i][mediasindex]+A2/2<=pixels[j].fine)&(raggi[i][mediasindex]+A2/2>pixels[j].inizio)):
            pixels[j].appartenenza=i+1

    
'''m1=(np.random.randint(1,210,500))*uma
partenze=np.random.uniform(-A2/2,A2/2,len(m1))
raggi1=np.zeros(len(m1))
for i in range(len(m1)):
    raggi1[i]=raggio(m1[i],vmin[mediasindex],bmin[mediasindex])+partenze[i]
    print(raggi1[i])
for i in range(len(raggi1)):
    for j in range(len(pixels)):
        if ((raggi1[i]<=pixels[j].fine)&(raggi1[i]>pixels[j].inizio)):
            pixels[j].hit= True
            pixels[j].nhit=pixels[j].nhit+1
           

for i in range(len(pixels)):
    print(pixels[i].appartenenza, pixels[i].nhit, pixels[i].hit)

plt.plot(m,raggi[:,mediasindex])
plt.show()'''

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

bins1=[]
sommeperbins=np.zeros(len(m))
for i in range(len(pixels)-1):
    if (pixels[i].appartenenza==pixels[i+1].appartenenza)&(pixels[i].hit==True):
        bins1.append(pixels[i].nhit+pixels[i+1].nhit)
    print(pixels[i].appartenenza, pixels[i].nhit, pixels[i].hit)
print(bins1)

for i in range(len(pixels)):
    pixels[i].nhit=0
    pixels[i].hit= False


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

bins2=[]
sommeperbins=np.zeros(len(m))
for i in range(len(pixels)-1):
    if (pixels[i].appartenenza==pixels[i+1].appartenenza)&(pixels[i].hit==True):
        bins2.append(pixels[i].nhit+pixels[i+1].nhit)
    print(pixels[i].appartenenza, pixels[i].nhit, pixels[i].hit)
print(bins2)


