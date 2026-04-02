
import os
import numpy as np
import DigitalMicrograph as DM

dir=r"C:\Users\arksa\Documents\em-data\jeol-pts"
os.chdir(dir)
file=r"2406PTTD.PTS"

x=257
y=257

ch=4096
binn=4
cut=2048


data=np.fromfile(file,dtype="u2")

flag=np.arange(data.size)[(data==55296) | (data==53504) | (data==53760)]
data=np.where((data==24576) | (data==28672), 1, data-45056)

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

si2=np.transpose(si,(2,0,1))
siDM=DM.CreateImage(si2.copy(order="C"))
siDM.ShowImage()
del siDM
