__author__ = "Papamichail A. Angelos, email : papamichail.ang@gmail.com"

from helperMethods import  *
mytimeis=0
nodesToVisit=[]



###### LOAD A GRAPH #######

G = nx.Graph()
G = readDataset()
#G = nx.karate_club_graph()
#G = readgml()

K=1000
# K CENTERS!

nodeLabels = {}
#Normalize node names to start from 0
G =nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
start= time.time() # the clock starts ticking!
divDegrees =oneDivDegree(G) # O(n*m) time for every node its degree divided by one
neighbors = makeNeighbors(G)

length=G.number_of_nodes()
absorptionPropability = np.zeros((K, length))
isCenter = np.zeros((length))




labels = np.zeros((length )) #need to keep track on the center every node belongs
Kcenters=pickRandomCenters(0,length-1,K)# INITIALIZE

#######################
#values which will make my algorithm end if they come close, algorithm converges
SPOld =0
SPNew = 0.1
#######################

iterations=0
Gs = [] # a list for induced subgraphs
epsilon=0.1

time1sum=0 # measure time needed for each major step
time2sum=0
time3sum=0

while (SPOld < SPNew - 0.2*SPNew): #I iterations
    print(iterations)
    isCenter = np.zeros((length))
    absorptionPropability = np.zeros((K, length))
    labels = np.zeros((length))
    iterations = iterations+1
    SPOld = SPNew
    for k in range(0, K):
        isCenter[Kcenters[k]] = 1
        absorptionPropability[k][Kcenters[k]] = 1
        labels[Kcenters[k]] = k
    greaterThanEpsilon = 0
    it=0
    greaterThanZeroNew=0
    greaterThanZeroOld=-1
    while(greaterThanZeroOld < greaterThanZeroNew - 0.2*greaterThanZeroNew):#J Iterations
        greaterThanZeroOld = greaterThanZeroNew
        greaterThanZeroNew = 0
        print(it)
        counter = 0

        it = it+1
        randomListofNodes = G.nodes()
        random.shuffle(randomListofNodes)
        time1=time.time()
        while(randomListofNodes.__len__()>0):# V iterations

            v = randomListofNodes.pop()
            if isCenter[v] == 0:
                neighList = neighbors.get(v)
                for e in neighList:  # |AverageDegree| Iterations
                    for k in range(0, K):
                        oldval = absorptionPropability[k][v]
                       # absorptionPropability[k][v] =0
                        if (isCenter[e] == 1 and e== Kcenters[k]) or isCenter[e] == 0:
                            absorptionPropability[k][v] = absorptionPropability[k][v] + absorptionPropability[k][e]*divDegrees[v]
                        counter =counter +1

                    if absorptionPropability[k][v]>0:
                         greaterThanZeroNew =greaterThanZeroNew +1
        print("counter :"+str(counter) )
        time1sum=time.time() -time1 +time1sum
        # print(absorptionPropability)
        #     print("Old : "+str(greaterThanZeroOld))
        #     print("New : " + str(greaterThanZeroNew))
    SPNew =0
    time2 = time.time()
    for v in G.nodes(): # |V| iterations
        # find  which is the nearest for every node
        max=0
        id =0
        for i in range(0,K): # K iterations
            if absorptionPropability[i][v] > max:
                max = absorptionPropability[i][v]
                id = i
                labels[v] = id

        # for edges in G.edges(v):
        #     G[edges[0]][edges[1]]['weight'] = id
        SPNew = SPNew + absorptionPropability[id][v]
    time2sum = time.time() - time2 + time2sum

    # # print(SPNew)
    # print(SPOld)
    # print(absorptionPropability)
    time3=time.time()
    Kcenters = newCenters(G,absorptionPropability,labels,isCenter, K, Kcenters)

    time3sum = time3sum + time.time()-time3
    print(Kcenters)



end=time.time()
for v in G.nodes():
    for edges in G.edges(v):
        G[edges[0]][edges[1]]['weight'] = id

for i in range(0, K):
    # build K subgraphs
    Gs.append(nx.Graph())

for e in G.edges():
    # fill the subgraphs depending on the weight
    w = G[e[0]][e[1]]['weight']
    Gs[w].add_edge(e[0], e[1], weight=w)
mytimeis=end-start
coef(G,K,labels)
#print(labels)
#print(absorptionPropability)
# print(distances)
# print("---")
#print(labels)

#plotGraph(labels,G,K)
print("My time is : "+str(mytimeis))
#print(labels)
print("...The end...")
print("Loop over nodes and their neighbors and K : " +str(time1sum))
print("Loop over nodes and K : " +str(time2sum))
print("newcenters : " +str(time3sum))