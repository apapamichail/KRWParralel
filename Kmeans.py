__author__ = "Papamichail A. Angelos, email : papamichail.ang@gmail.com"

from sklearn.cluster import KMeans
import numpy as np
import networkx as nx
import time
import random
import matplotlib.pyplot as plt
from helperMethods import *

G = readDataset()
#G = nx.karate_club_graph()
#G=readgml()
G =nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
K=500

start = time.time()
A = nx.adjacency_matrix(G)

kmeans = KMeans(n_clusters=K, init="random").fit(A)
end =time.time()
mytimeis = end - start
sumLabels = np.zeros((K))
labels=kmeans.labels_

coef(G,K,labels)
print(mytimeis)
#plotGraph(labels,G)


