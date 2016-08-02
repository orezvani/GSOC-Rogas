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
The work done in the google summer of code is 
### Conducting intensive research on local community detection
asdfsd
### Implementation of several state-of-the-art algorithms for local
community detection



<br>
Before runing the prototype, ensure the system is Ubuntu and all the external 
python packages mentioned above are installed correctly. 
<br>
<br>
**Notice that pillow is 
the latest package for PIL and it is not compatible with the old PIL package. 
If your have already had PIL in your python dist-packages (/usr/lib/python2.7/dist-packages/),
please delete the original PIL and install the new Pillow package. If you are using Eclipse or 
other IDE, I suggest to use the source code to install Pillow so that the unresolved import 
issues of the IDE can be solved.**
<br>
<br>
You also need to change the code of the *queryConsole.start()* method a bit 
to connect your own PostgreSQL database. Then you can start the prototype 
by running the *GUI_Console* program.
<br>
<br>
More details about the Rogas, please refer to 
the thesis "Towards a Unified Framework for Network Analytics" collected in 
Australian National University (http://users.cecs.anu.edu.au/~u5170295/publications/thesis-minjian.pdf). You can also 
contact *minjian.liu@anu.edu.au* or *qing.wang@anu.edu.au* for more information.
<br>
<br>
PS: For answering how to change the output of the GUI_Console as left alignment (default is center alignment)
You can change the source code of the pylsytable as follow:(the path in Ubuntu normally is 
'/usr/local/lib/python2.7/dist-packages/pylsy/pylsy.py).
<br>
* Find the "def _pad_string(self, str, colwidth):" function in the pylsy.py
* change " return ' ' * prefix + str +' ' * suffix " (center alignment ) as " return str + ' ' * prefix +' ' * suffix " (left alignment)

## Contributors
Instructor: Qing Wang (*qing.wang@anu.edu.au*) <br>
Principal Developer: Minjian Liu (*minjian.liu@anu.edu.au*) <br>
Developers: Yan Xiao (*xiaoyanict@foxmail.com*), Chong Feng (*u4943054@anu.edu.au*)
