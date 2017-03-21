__author__ = "Papamichail A. Angelos, email : papamichail.ang@gmail.com"

import random
import time
import matplotlib.pyplot as plt
import absorbing_centrality as arw
import networkx as nx
import numpy as np



def readDataset():
    dblp_graph = open('dblp.txt', 'r')


    dblpGraph = nx.Graph()
    count = 0;
    for line in dblp_graph:
        nodeSet = line.split("\t")
        dblpGraph.add_edge(nodeSet[0], nodeSet[1][:-1])
        count += 1
        if count==5000:
             break
        # print("nodeset[0]= ", nodeSet[0], "\t nodeSet[1]= ", nodeSet[1])
    dblpGraph = nx.convert_node_labels_to_integers(dblpGraph, first_label=0, ordering='default', label_attribute=None)

    return dblpGraph


def pickRandomCenters(a,b,k):
    i=0
    centers=random.sample(range(a, b), k)
    return centers
def oneDivDegree(G):
    divDegrees = {}

    for v in G.nodes():
        d = G.degree(v)
        if d != 0:
            divDegrees[v] = 1 / d
        else:
            divDegrees[v] = 0

    return divDegrees


def plotGraph(labels,G,K):

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

def measureClusCoef(Gs,K):
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

    measureClusCoef(Gs,K)






def oneDivDegree(G):
    divDegrees = {}

    for v in G.nodes():
        d = G.degree(v)
        if d != 0:
            divDegrees[v] = 1 / d
        else:
            divDegrees[v] = 0

    return divDegrees


def readgml():
    G = nx.read_gml('football.gml')
    return G




def sameCenters(Kcenters,Kcentersold):
    c=0
    for i in range(0,K):
        if Kcenters[i] == Kcentersold[i]:
            c = c +1
    if c == K-1:
        return True
    else:
        return False



def newCenters(G,absorptionPropability,labels, isCenter,K,Kcenters):
    # New centers based on each induced subgraph ! #
    i = 0
    alpha = 0.85
    maxKValue = np.zeros(K)
    maxKNode = np.zeros(K)
    print(absorptionPropability)
    for v in G.nodes(): #|V| Iterations
        myPropabilityDivHisPropabilityToAbsorbSum=0
        sumOfshortestPaths = 0
        Ks=0
        if isCenter[v] ==0:
            for i in range(0,K):# K Iterations

                if labels[v] != i:
                    myPropabilityDivHisPropabilityToAbsorbSum = myPropabilityDivHisPropabilityToAbsorbSum+  absorptionPropability[labels[v]][v]/absorptionPropability[i][v]

            #         sp = len(nx.shortest_path(G,source=Kcenters[i],target=v))
            #         if sp>0:
            #             Ks= Ks +1
            #             sumOfshortestPaths = sp +sumOfshortestPaths
            #             myPropabilityDivHisPropabilityToAbsorbSum= myPropabilityDivHisPropabilityToAbsorbSum+ absorptionPropability[i][v] *(1- sp/6)
            # print(Ks)
            # print("absorptionPropability[labels[v]][v]")
            #
            # print(absorptionPropability[labels[v]][v])
            # print("sumOfPropabilityAbsorbedByOthers")
             #
            # print( absorptionPropability[labels[v]][v] )
            # print(myPropabilityDivHisPropabilityToAbsorbSum)
            if maxKValue[labels[v]] < myPropabilityDivHisPropabilityToAbsorbSum*K+myPropabilityDivHisPropabilityToAbsorbSum:
                maxKValue[labels[v]] =  myPropabilityDivHisPropabilityToAbsorbSum*K+myPropabilityDivHisPropabilityToAbsorbSum
                maxKNode[labels[v]] = v

    # for v in G.nodes():
    #     if absorptionPropability[labels[v]][v] > maxKValue[labels[v]] and isCenter[v] ==0:
    #         maxKValue[labels[v]] = absorptionPropability[labels[v]][v]
    #         maxKNode[labels[v]] = v

    for i in range(0, K):
        Kcenters[i] = maxKNode[i]
        # g.clear()

    return Kcenters


def makeNeighbors(G):
    # create a dictionary in a dictionary to
    # one is the dictionary of nodes the other
    # of their neighbors
    # all have the value 0 cause we havent visited them yet
    d = dict()
    for v in G.nodes():
        neighbors=[]
        for e in G.edges(v):
            neighbors.append(e[1])
        d.update({v:neighbors})

    return d

