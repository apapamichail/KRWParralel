__author__ = "Papamichail A. Angelos, email : papamichail.ang@gmail.com"

import pregeltest
import time
from helperMethods import plotGraph

Kcenters=[]

distanceNew=0
distanceOld=0
coefold=0
coef=0
labels=[]
start = time.time()
while(True):
    distanceOld = distanceNew
    Kcentersold=Kcenters
    coefold = coef
    labelsold=labels
    Kcenters, distanceNew, labels, G,coef = pregeltest.main(Kcenters)  # do whatever is in test1.py

    print(Kcenters)
    print("---------------")
    print(distanceNew)
    print(distanceOld)
    if coefold > coef  or coef < coefold+0.1*coefold :
        # runs untill current solution is worse than last solution based on averager clustering coeeficient
        break
end = time.time()  # the clock starts ticking!

K=500
print(coefold)
print(end-start)
#plotGraph(labelsold,G,K) 

# print("END")