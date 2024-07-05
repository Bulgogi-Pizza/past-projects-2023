##
import numpy as np
import matplotlib.pyplot as plt
from voigt import voigt
from fit2voigt import fit2voigt

par0 = 'C:/Users/19-NT25-71-16/Downloads/VoigtFitting_Matlab_Python/Raw_Data/par0_O2.txt'
dat = 'C:/Users/19-NT25-71-16/Downloads/VoigtFitting_Matlab_Python/Raw_Data/testdata_2_O2.txt'

par0 = np.loadtxt(open(par0,'r'))
dat = np.loadtxt(open(dat,'r'))


##########
##
parmin = fit2voigt(dat,par0)
x = parmin['x']
res = parmin['fun']
##
fit = voigt(dat[:,0],x)
##


plt.rcParams["figure.dpi"] = 1000
plt.subplot(211)
plt.plot(dat[:,0],dat[:,1],'b', label = 'data', linewidth = 0.3)
plt.plot(dat[:,0],fit,'r', label = 'fit', linewidth = 0.3)
plt.legend(loc='upper left')
plt.xlim(np.array([13151.5,13153.5]))
plt.ylim(-0.01,0.15)

plt.subplot(212)
plt.plot(dat[:,0],res,'k',label = 'residual')
plt.legend('residual','location')
plt.legend(loc='upper left')
plt.xlim(np.array([13151.5,13153.5]))
plt.ylim(np.array([- 10,10]) * 0.001)
