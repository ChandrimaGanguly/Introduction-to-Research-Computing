from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size==8:
    cartesian3d = comm.Create_cart(dims = [2,2,2],periods = [True,True,True],reorder=True)

    coord3d = cartesian3d.Get_coords(rank)
    print ("In 3D topology, Processor ",rank, " has coordinates ",coord3d)

    left,right = cartesian3d.Shift(direction = 0,disp=1)
    up,down = cartesian3d.Shift(direction = 1,disp=1)
    back,front = cartesian3d.Shift(direction = 2,disp=1)

    print ("In 3D topology, Processor ",rank, " has neighbours ", left," and ", right)
    print ("In 3D topology, Processor ",rank, " has neighbours ", up," and ", down)
    print ("In 3D topology, Processor ",rank, " has neighbours ", back," and ", front)

#     We can also make sub-topologies so we only communicate to a small section of ranks
    cartesian2d = cartesian3d.Sub(remain_dims=[False,True,True])
    rank2d = cartesian2d.Get_rank()
    coord2d = cartesian2d.Get_coords(rank2d)

    print ("In 2D topology, Processor ",rank," has new rank ",rank2d," and coordinates ", coord2d)
    
    left,right = cartesian2d.Shift(direction = 0,disp=1)
    up,down = cartesian2d.Shift(direction = 1,disp=1)

    print ("In 2D topology, Processor ",rank, " has new rank ",rank2d," and neighbours ", left," and ", right)
    print ("In 2D topology, Processor ",rank, " has new rank ",rank2d," and neighbours ", up," and ", down)
    
    
# communication should be done using non-blocking send and revieves
# rather than collectives as MPI can reorder process labels to 
# optimise communication.  However we should have the following collectives
# for neighbours (as they exist in the github: https://github.com/erdc/mpi4py/blob/master/src/MPI/Comm.pyx):

# output = cartesian3d.neighbor_allgather(sendobj=rank)
# output = cartesian3d.neighbor_alltoall(sendobj=rank)

# But they currently give: NotImplementedError it doesn't exist for my MPI implementation...


