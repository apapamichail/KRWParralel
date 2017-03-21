__author__ = "Papamichail A. Angelos, email : papamichail.ang@gmail.com"


from pregel import *
import networkx as nx
# The next two imports are only needed for the test.
from numpy import *
import random
import matplotlib.pyplot as plt
import time
import pregel
import threading
from helperMethods import *
distance =0

def closestCenter(vertices):

    distance=0
    for vertex in vertices:
        # find  which is the nearest for every node
        max=0
        id =0
        for k in range(0,K):
            if  vertex.value[k]> max:
                max = vertex.value[k]
                labels[vertex.id] = k
      #  print(vertex.value[labels[vertex.id]])
        distance = distance +vertex.value[labels[vertex.id]]


    return distance



def plotGraph(labels,G):

    listi={}
    nodelabels={}
    for id in range(0, K):
        listi[id] = list()

    for ns in G.nodes():
        nodelabels[ns]=ns
        for id in range(0,K):
            if labels[ns] == id:
                listi[id].append(ns)

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    node_color=['#6666ff','#ff0000','#66ffff','#99cc00','#990000','#996600','#000099','#00cc66','#ff00ff','#660066','#66ccff']
    for id in range(0, K):
        nx.draw_networkx_nodes(G, pos,
                               nodelist=listi[id],
                               node_color=node_color[id],
                               node_size=500,
                               alpha=0.8)


    # edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=G.edges(),
                           width=8, alpha=0.5, edge_color='r')

    nx.draw_networkx_labels(G,pos,nodelabels,font_size=16)
    plt.show() # display


def pickRandomCenters(a,b,k):
    i=0
    centers=random.sample(range(a, b), k)
    return centers

for k in range(0,K):
    isCenter[Kcenters[k]]=1

def initializeCenters():
    isCenter = zeros(num_vertices)
    for k in range(0, K):
        isCenter[Kcenters[k]] = 1




def newCenters(G, vertices, labels, isCenter):
    # New centers based on each induced subgraph ! #
    global K
    i = 0
    alpha = 0.85
    maxKValue = zeros(K)
    maxKNode = zeros(K)
    Kcenters=zeros(K)
    for v in vertices:
        myPropabilityDivHisPropabilityToAbsorbSum=0
        max = 0
        id = 0
        if isCenter[v.id] ==0:
            for k in range(0, K):
                if v.value[k] > max:
                    max = v.value[k]
                    labels[v.id] = k

        if isCenter[v.id] ==0:
            for i in range(0,K):
                if labels[v.id] != i:
                    # print(v.value[labels[v.id]])
                    # print(v.value[labels[i]])
                   # print(v.value[labels[v.id]])

                    myPropabilityDivHisPropabilityToAbsorbSum = myPropabilityDivHisPropabilityToAbsorbSum+  v.value[labels[v.id]]/v.value[labels[i]]

        if isCenter[v.id] ==0:
          #  print(myPropabilityDivHisPropabilityToAbsorbSum)
            if maxKValue[labels[v.id]] < myPropabilityDivHisPropabilityToAbsorbSum:
                maxKValue[labels[v.id]] =  myPropabilityDivHisPropabilityToAbsorbSum
                maxKNode[labels[v.id]] = v.id
        vertices.__getitem__(v.id).value= zeros(K)

    # for v in G.nodes():
    #     if absorptionPropability[labels[v]][v] > maxKValue[labels[v]] and isCenter[v] ==0:
    #         maxKValue[labels[v]] = absorptionPropability[labels[v]][v]
    #         maxKNode[labels[v]] = v





    for i in range(0, K):
        Kcenters[i] = maxKNode[i]
        isCenter[Kcenters[i]] =1
        vertices.__getitem__(int(Kcenters[i])).value[i]=int(1)




    # g.clear()
    return Kcenters


def coef(G,K,labels):

    for v in G.nodes():
        for edges in G.edges(v):
            G[edges[0]][edges[1]]['weight'] =int(labels[v])


    Gs = []
    for i in range(0, K):
        # build K subgraphs
        Gs.append(nx.Graph())

    for e in G.edges():
        # fill the subgraphs depending on the weight
        w = G[e[0]][e[1]]['weight']
        a = int(w)
        Gs[w].add_edge(int(e[0]), int(e[1]), weight=a)

    c = measureClusCoef(Gs)
    return c

def measureClusCoef(Gs):
    coef={}
    sum=0
    for k in range(0,K):
        try:
            coef[k] = nx.average_clustering(Gs[k])
        except ZeroDivisionError:
            coef[k] = 0
        sum = sum + coef[k]
    print("Sum/K")
    print(sum/K)
    print("coef")
    print(coef)
    return sum/K

c=0
num_workers = 8
isCenter = []
G = nx.karate_club_graph()
G = readDataset()
#G = readgml()
num_vertices = G.number_of_nodes()
isCenter = zeros(num_vertices)
labels = zeros(num_vertices)
K = 1000
pregel.K = 1000


def main(Kcenters):
    global c
    global G
    global distance
    global isCenter
    global num_vertices

    distance=0
    if len(Kcenters)==0:
        Kcenters = pickRandomCenters(0, num_vertices, K)  # INITIALIZE

    G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
    num_vertices = G.number_of_nodes()

    vertices=[]
    for v in G.nodes():
        vertices.append(Parw(v, zeros(K), []))

    for k in range(0, K):
        #print(Kcenters[k])
#        vertices.__getitem__(Kcenters[k]).active=False #doesnt Actually Work
        vertices.__getitem__(int(Kcenters[k])).value[k]=1
        isCenter[Kcenters[k]]=1
    pregel.isCenter = isCenter
    create_edges(vertices)
    start = time.time()  # the clock starts ticking!
    # for i in range(0,3):
    #pr_test = pagerank_test(vertices)
#    print ("Test computation of pagerank:\n%s" +str( pr_test))
   # print(Kcenters)
    c =c+1
   # print(c)
    a = runPregel(vertices)

    distance= closestCenter(vertices)
    #print(labels)
    #
    # for k in range(0,num_workers-1):
    #     pregel.workers[k].join()
   # print(isCenter)
    Kcenters = newCenters(G, vertices, labels, isCenter)


    end = time.time()  # the clock starts ticking!
    print("time")
    print(end - start)
    c = coef(G,K,labels)
    #print(labels)
    #plotGraph(labels,G)

    return Kcenters,distance,labels,G,c

def create_edges(vertices):
    """Generates 4 randomly chosen outgoing edges from each vertex in
    vertices."""
    for vertex in vertices:
        verticesQ=[]
        for edges in G.edges(vertex.id):
            verticesQ.append(vertices.__getitem__(edges[1]))

        vertex.out_vertices = verticesQ


def runPregel(vertices):
    """Computes the pagerank vector associated to vertices, using
    Pregel."""
    p = Pregel(vertices,num_workers)
    p.run()

    return None



    #return mat([vertex.value for vertex in p.vertices]).transpose()

class Parw(Vertex):
    def update(self,k):
        # This routine has a bug when there are pages with no outgoing
        # links (never the case for our tests).  This problem can be
        # solved by introducing Aggregators into the Pregel framework,
        # but as an initial demonstration this works fine.
        if isCenter[self.id]==0:
            if self.superstep < 10:
                self.value[k] =0
                for n in self.out_vertices:
                    self.value[k] = self.value[k] + (1/len(self.out_vertices))*n.value[k]

                # self.outgoing_messages = [(vertex, outgoing_pagerank)
                #                           for vertex in self.out_vertices]
            else:
                self.active = False


main([])