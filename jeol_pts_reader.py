# ouput data is "si".
# first 2 channel of si is replaced to live and real time.
# however time resolution is 10 msec.
# this would be too poor for quantification...

import os
import numpy as np
import DigitalMicrograph as DM

dir=r"C:\Users\arksa\Documents\em-data\jeol-pts"
os.chdir(dir)
file=r"2406PTTD.PTS"

x=257
y=257

# number of energy channel of EDS.
ch=4096

# binning of energy channel in output.
# if you want enegy resolution, set 1.
# this parameter is set just for memory and disc saving.
binn=4

# cutoff energy of output.
# this is also for memory saving.
cut=2048

data=np.fromfile(file,dtype="u2",offset=16384)

flag=np.arange(data.size)[(data==55296) | (data==53504) | (data==53760)]
# assuming livetime stamp is 24576 = 0x6000
# assuming realtime stamp is 28672 = 0x7000
livet=24576
realt=28672

# resolution of time stamp.
# maybe 10 msec
tscale=10

#data=np.where((data==24576) | (data==28672), 1, data-45056)
data=np.where((data==livet) | (data==realt), binn*((data-livet)//(realt-livet)), data-45056)


flagsize=flag.size

print(flagsize)

si=np.zeros((x+1,y,(ch-cut)//binn),dtype="u2")

ypos=-1
j=0
for i in range(flag.size):
    pos=flag[i]
    if data[pos]==55296-45056:
        ypos+=1
        j=0
    elif data[pos]==53760-45056:
        nextpos=flag[i+1]
        if data[nextpos]==53760-45056 or data[nextpos]==53504-45056:
            si[j,ypos,:]=np.bincount(data[pos+1:nextpos]//binn,minlength=(ch-cut)//binn)[:(ch-cut)//binn]
            j+=1

si[:,:,0:2]*=tscale

si2=np.transpose(si,(2,0,1))
siDM=DM.CreateImage(si2.copy(order="C"))
siDM.ShowImage()
del siDM
