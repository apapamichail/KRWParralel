__author__ = "Papamichail A. Angelos, email : papamichail.ang@gmail.com"

from sklearn.cluster import SpectralClustering
from helperMethods import *

G = readDataset()
#G = nx.karate_club_graph()
#G=readgml()

mytimeis=0
K=500

G =nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)

start = time.time()
A = nx.adjacency_matrix(G)


spectral = SpectralClustering(n_clusters=K, gamma=0.5).fit(A)
end =time.time()
mytimeis = end - start
sumLabels = np.zeros((K))
labels=spectral.labels_
for v in labels:
    sumLabels[v] = sumLabels[v] +1


print(mytimeis)
print(labels)
coef(G,K,labels)
#plotGraph(labels,G)

