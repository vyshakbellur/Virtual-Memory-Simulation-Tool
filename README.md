# Virtual-Memory-Simulation-Tool
python script emulating virtual memory operation

Algorithm:

Based on the processes, address and their intent, whether to read or write, objects are created at each row of the text file. 
Physical memory can accommodate 32 addresses at a time. This is accomplished using an array. 
First 32 processes are input into the array as objects. Objects comprise of all the details and has additional details such as time stamp and number of times the process was called for. 
Since there is no process in the main memory at the beginning of simulation, these are considered page faults. 
Subsequent requests are rendered by first checking in the memory. If the page is found, next request is served.
If page is not found, based on a chosen algorithm, it is swapped from the virtual space. 
For random, a number from 0 to 31 is randomly generated. Generated number is the memory location where the entry is going to be replaced. 
In case of FIFO, elements are replaced sequentially from 0 to 31. It repeats in cyclic manner and the page replacement is carried out.
For LRU, time stamp of the process arrival is tracked. The process which has the least time stamp and which is not dirty, is replaced. 
PER is programmed by keeping track of references. If referenced, the reference bit is set in the memory. Reference bits are reset after every 200 requests. 
Dirty bits and disk writes are monitored at each page fault. 

Instructions to run the code:

In the command prompt please enter in the following pattern:
Python “python script name” “data file name” “algorithm name” “0 for no debug 1 for debug”
Algorithm name can be 
FIFO or fifo
LRU or lru
PER or per
RAND or rand 
