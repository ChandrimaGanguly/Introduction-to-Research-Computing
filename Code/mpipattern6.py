from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

index, edges = [0], []
for i in range(size):
    pos = index[-1]
    connections = random.randint(1,5)
    index.append(pos+connections)
    edges1=[]
    for j in range(connections):
        x = random.randint(0,size-1)
        while x==rank or x in edges1:
            x = random.randint(0,size-1)
        edges1.append(x)
        
    edges += edges1

graph = comm.Create_graph(index[1:], edges)

neighs = graph.Get_neighbors(rank)

print ("In Graph we assigned processor ",rank, " to have neighbours ", neighs)

if rank==0:
    print ("Graph has dimensions ",graph.dims)
    print ("Graph has #nodes ",graph.nnodes)
    print ("Graph has #edges ",graph.nedges)
    print ("Graph has index ",graph.index)
    print ("Graph has edges ",graph.edges)

print ("Processor ",rank," has in degree ",graph.indegree)
print ("Processor ",rank," has out degree ",graph.outdegree)
print ("Processor ",rank," has in edges ",graph.inedges)
print ("Processor ",rank," has out edges ",graph.outedges)

# We should be able to only specify connection to nodes,
# of which we can have several, on this rank with the following:

# sources = [rank]
# connections = random.randint(1,5)
# degrees = [connections]
# destinations = []
# for i in range (connections):
#     x = random.randint(0,size-1)
#     while x==rank:
#         x = random.randint(0,size-1)
#     destinations.append(x)
#
# graph = comm.Create_dist_graph(sources,degrees,destinations)

# But they currently give: NotImplementedError so it doesn't exist for my MPI implementation...

