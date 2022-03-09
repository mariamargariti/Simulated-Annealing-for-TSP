import math                       
import random                       
import numpy as np                  
import matplotlib.pyplot as plt     
import parser1 as par

    
#arxikes parametroi gia ton algorithmo tis simulated annealing 
def initParameter():
    tInitial=100.0  #arxiki thermokrasia
    tFinal=1       #teliki thermokrasia
    n=1000          #epanalipseis
    alfa=0.98       #T(k)=alfa*T(k-1)

    return tInitial,tFinal,alfa,n

#ypologizei tin apostash metaksy dyo polewn
#dhmiourgei enan pinaka 280x280 me mhdenika
#ekxwrei strogylopoihmenes tis apostaseis i-j kai j-i pou einai idies stin katallhlh thesh tou pinaka,
#epistrefei ton pinaka
def getDistMat(nCities, coordinates):
    distMat=np.zeros((nCities,nCities)) 
    for i in range(nCities):
        for j in range(i,nCities):
            distMat[i][j]=distMat[j][i]=round(np.linalg.norm(coordinates[i]-coordinates[j]))

    return distMat                              
 
#h synartisi dexetai ton pinaka tourGiven me omoiomorfa xwrismenous arithmous sto [0,280)
#ton arithmo twn polewn(nCities)
#ton pinaka olwn twn apostasewn distMat
def calTour(tourGiven, nCities, distMat):
    Tour=distMat[tourGiven[nCities-1], tourGiven[0]]   #apostash teleytaias polhs apo tin prwth
    for i in range(nCities-1):                                   
        Tour += distMat[tourGiven[i], tourGiven[i+1]]  #apostash kathe polhs apo thn epomenh
    return round(Tour) #stogylopoihmenh timh tou Tour


#h synartisi dexetai ton pinaka tourGiven me omoiomorfa xwrismenous arithmous sto [0,280)
#kai ton arithmo twn polewn(nCities) 
#ekxwroume sta i kai j tyxaious akeraious sto [0,280)
#an i!=j vazoume sto tourSwap[i] tin timh tou tourGiven[j] kai sto tourSwap[j] tin timh tou tourGiven[i]
#epistrefei ton pinaka tourSwap
def Swap(tourGiven, nCities):
    i=np.random.randint(nCities)          
    while True:
        j=np.random.randint(nCities)      
        if i!=j: 
            break                      

    tourSwap=tourGiven.copy()  #antigrafi tou tourGiven ston tourSwap
    tourSwap[i]=tourGiven[j]    #swap th thesi twn dyo polewn
    tourSwap[j]=tourGiven[i]  

    return tourSwap

def main():
    data=r"C:\Users\maria\FinalProject-Maria Margariti\a280.tsp" 
    
    #kalw th synarthsh built_all()
    #epistrefei to lexiko me key to onoma tou komvou kai value mia lista me tis apostaseis

    cities=par.built_all(data) 
    
   #metatrepw ta value se integers
    for key, item in cities.items():
        cities[key]=[int(item[0]), int(item[1])] 
   
   #dhmiourgw tin lista cities_list me list comprehension
   #pairnw to value kathe komvou (2 akeraioi) kai to ekxwrw sto cities_list
   
    cities_list = [cities[key] for key in cities] #[[288 149], ]

    #dhmiourgw ena numpy array me tin lista cities_list
    # [[288 149]
    #  [288 129]
    #  [270 133]
    #  [256 141]....]
    coordinates=np.array(cities_list) 
    
    #kalw thn initParameter() kai ekxwrw stis tInitial,tFinal,alfa,n tis times 100.0, 1, 0.98, 1000 antistoixa
    tInitial,tFinal,alfa,n=initParameter()

    #pairnw ton arithmo twn komvwn
    nCities=coordinates.shape[0]
    
    #ekxwrw ton pinaka me tis apostaseis i-j kai j-i stin metavlhth distMat
    distMat=getDistMat(nCities, coordinates)    
    n=nCities #arithmos polewn                    
    tNow=tInitial  #arxikopoiw thn twrini thermokrasia me tin arxiki(tInitial)                      
    tourNow=np.arange(nCities)   #epistrefei pinaka me arithmous sto diasthma [0, 280) 
    #epistrefei to athroisma twn apostasewn kathe polhs me thn epomenh ths kai ths prwtis me tin teleutaia
    valueNow=calTour(tourNow,nCities,distMat) 
    tourBest=tourNow.copy() #antigrafh tou tourNow array sto tourBest
    valueBest=valueNow  #ekxwrw to valueNow sto valueBest                              
    rBest=[] #dimiourgw ti lista rBest 
    rNow=[] #dimiourgw ti lista rNow 

    iter=0 #metrhths epanalipsewn                        
    while tNow >= tFinal:          
        for k in range(n):  
            tourNew=Swap(tourNow, nCities) #o pinakas me tis theseis twn newn komvwn
            valueNew=calTour(tourNew,nCities,distMat) 
            deltaE=valueNew-valueNow

            if deltaE < 0:                          
                accept=True
                #an i apostasi sto valueNew einai mikroteri apo to valueBest 
                #ekxwreitai sto tourBest h tourNew kai sto valueBest to valueNow
                if valueNew < valueBest:             
                    tourBest[:]=tourNew[:] 
                    valueBest=valueNew
            else:                                   
                pAccept=math.exp(-deltaE/tNow)    #ekxwrei sto pAccept to e^(-deltaE/tNow)
                if pAccept > random.random(): #random sto diasthma [0.0, 1.0)
                    accept=True 
                else:
                    accept=False 

            #an to accept ginei True ekxwrei to tourNew sto tourNow kai to valueNew sto valueNow
            if accept == True: 
                tourNow[:]=tourNew[:]
                valueNow=valueNew

        #shift 2 theseis to tourNow
        tourNow=np.roll(tourNow,2)                

        rBest.append(valueBest) #kanw append to distance tis kalyteris diadromis sti lista rBest  
        rNow.append(valueNow)  #kanw append stin lista rNow to distance tou valueNow 
        print('i:{}, t(i):{:.2f}, valueNow:{:.1f}, valueBest:{:.1f}'.format(iter,tNow,valueNow,valueBest))
        iter=iter+1 
        tNow=tNow*alfa  #T(k)=alfa*T(k-1)
        
    print("Best tour: \n", tourBest)
    print("Best value: {:.1f}".format(valueBest))

main()