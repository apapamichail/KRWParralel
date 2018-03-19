# KRWParralel
This project contains:
A linear version of the KRW algorithm,
A parallel version of the KRW algorithm,
Helper files 
and a kmeans implementation as well as a spectral.

A community Detection Algorithm that uses a modified version of Random Walk.
The main purpose of this project was to create a new algorithm for community detection and explore the 
improvements we could have in time complexity if we used pregel. Pregel is a library developed from google that 
can parallelize a problem into clusters and sees nodes of a graph as vectors that can communicate step-wise.
The use a little modified version of pregel proved its effectives. The version for python is a toy version in the 
sense that it cannot scale over machines only in one machine with the use of cores.
There is also code created for the comparison of our implementation in reference to the quality of the clusters and 
the time complexity. The methods used for this purpose are not a state of art way to do something like that. 
Nevertheless they accomplish their purpose. Pregel is effective.
The documentation provided is in  greek but the algorithms are described in English.

