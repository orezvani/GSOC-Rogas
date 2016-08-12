#![Logo](https://cecs.anu.edu.au/sites/default/files/styles/anu_doublenarrow_440_scale/public/images/rogas-web.jpg?itok=JfEfhc1_)
#Local Community Detection using Rogas
Mojtaba (Omid) Rezvani

## Introduction
Rogas provides a high-level declarative query language to 
formulate analysis queries, but also can unify different graph algorithms 
within the relational environment for query processing.
<br>
<br>
The Rogas has three main components: (1) a hybrid data model, which 
integrates graphs with relations so that we have these two types of data 
structures respectively for network analysis and relational analysis; 
(2) a SQL-like query language, which extends standard SQL with 
graph constructing, ranking, clustering, and path finding operations; 
(3) a query engine, which is built upon PostgreSQL and can efficiently 
process network analysis queries using various graph systems and 
their supporting algorithms.
<br>
<br>
In this Google summer of code project, we add the community search, also 
known as local community detection capability to Rogas. We implement the 
state-of-the-art algorithms proposed for local community detection for 
Rogas.


## Sumary of contributions in Google Summer of Code
The work done in the google summer of code includes: 
### (1) Conducting intensive research on local community detection
In this section, we study several approaches to local community
detection problem and chose the top algorithms that outperform others
in terms of efficiency, scalability and accuracy of finding communities.
### (2) Implementation of several state-of-the-art algorithms for local
In this section, we choose four algorithms presented for local community
detectiona nd implement these algorithms in Python for the project. In
particular, we implement local community search using several definitions
including k-core, k-truss, k-edge-connected, &gamma;-quasi k-cliques as
presented in several papers.
### (3) Design and implementation of a new approach
We also present a new approach for local community detection in
large-scale networks and devise an efficient algorithm for this problem.
Specifically, we propose to use k-edge-connected components for local
community detection problem and propose an algorithm using random
contractions.
### (4) Comparison of performance of different algorithms
We then provide a through comparison of different algorithms in terms
of their performance on real social networks.

## Related works
Community detection in real-world social networks has been the focus of 
many scholars in computer science, and several algorithms have been 
developed for identifying communities from social networks. Studies in this 
area have mainly considered the problem of identifying all non-overlapping 
communities and overlapping communities from social networks. However, in 
real-life applications, we are usually interested in identifying communities 
around a given set of members of social networks. To this end, the community 
search problem has been defined [1] and several algorithms for solving this 
problem have been proposed. In this section, we review some of the 
state-of-the-art techniques that are proposed for identifying communities, 
in which a given set of query vertices participate.
<br><br>
Cui et al. [1] introduced a technique for identifying the 
degree-based dense communities in which a single query vertex participates, and 
studied two definitions for single vertex community search problem: Community 
Search with Maximality constraint (CSM) and Community Search with Threshold 
constraint (CST). In CSM, the objective is to find a connected subgraph that 
contains the given query vertex and has the largest minimum degree, while in CST, 
the objective is to find a connected subgraph that contains the query vertex and 
its minimum degree is no less than a given threshold. Barbieri et 
al. [2] proposed an extended model of CSM, which is 
capable of handling queries with more than one vertex, based on minimum degree. 
We implement this algorithm and provide it for Rogas.
<br><br>
The authors in [3] define the community of a vertex v, as a subgraph that is
a k-truss with maximum possible value of k. Since k-truss provides strong
connectivity and there is an efficient algorithm for finding k-trusses of a
network for a given k, this method achieves good results. We implement this
approach in Rogas.
<br><br>
The authors in [4] define the community of a vertex as a &gamma;-quasi k-clique
that has k vertices and every vertex is connected to &gamma; percent of other
vertices in the community. We also implement this approach in Rogas and present
the implementation publicly.
<br><br>
In [5], Wu et al. studied the free rider effect in community 
detection as the problem of communities being merged during the process of 
community detection algorithms, due to use of inappropriate fitness metrics. 
In this project, we make sure to avoid such effect in the chosen methods.

## A new approach for local community detection
Given a connectivity threshold k, we define a community as a maximal subgraph, 
in which there is at least k edge-disjoint paths between every pair of vertices.
We then use a randomized algorithm for the problem. In the randomized algorithm,
we iteratively pick a random edge and contract that edge, until there is no edge
left in the network. During random contractions, if the degree of a vertex
becomes less than k, we remove that vertex from network.

## References
[1] W. Cui, Y. Xiao, H. Wang, and W. Wang. Local search of communities in large graphs. In Proc. of SIGMOD'14, pages 991–1002. ACM, 2014.
<br>
[2] N. Barbieri, F. Bonchi, E. Galimberti, and F. Gullo. Efficient and effective community search. Data Mining and Knowledge Discovery, 29(5):1406–1433, 2015.
<br>
[3] X. Huang, H. Cheng, L. Qin, W. Tian, and J. X. Yu. Querying k-truss community in large and dynamic graphs. In Proc. of SIGMOD'14, pages 1311–1322. ACM, 2014.
<br>
[4] J. Shan, D. Shen, T. Nie, Y. Kou, and G. Yu. Searching overlapping communities for group query. World Wide Web, pages 1–24, 2015.
<br>
[5] Y. Wu, R. Jin, J. Li, and X. Zhang. Robust local community detection: on free rider effect and its elimination. Proc. of VLDB'15, 8(7):798–809, 2015.



