from mpi4py import MPI
import numpy as np
import scipy.signal as scs
import matplotlib.pyplot as plt
import sys

# Function that advances the game one step
def step(cells):
    mask = np.array([[1,1,1],[1,0,1],[1,1,1]])
    count = scs.convolve2d(cells,mask,mode='same',boundary='wrap')
    newcells = np.where(cells==1,np.where((count>1),np.where(count<4,1,0),0),np.where(count==3,1,0))
    return newcells

# Set up communication
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 12 is so there is space for the cells from other ranks
cells = np.zeros((10,12))
if rank==0:
    cells[3,6:8] = 1
    cells[4,4:6] = 1
    cells[4,7:9] = 1
    cells[5,4:8] = 1
    cells[6,5:7] = 1

for i in range(60):
    
    #################################################
    #    Communication of boundaries goes here      #
    #################################################

    cells = step(cells)

# Plot results, duck should be in 4th rank
fig = plt.figure()
ax = plt.axes()
ax.matshow(cells[:,1:11])
filename = 'PlotRank'+str(rank)+'.png'
savefig(filename)
