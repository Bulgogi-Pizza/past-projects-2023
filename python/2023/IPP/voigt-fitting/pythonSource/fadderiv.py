import numpy as np
from scipy import special
    
def fadderiv(v = None,par0 = None): 
    # [vf,dvdpar]= fadderiv(v,par0)
# input  --v: wavenumber
#        --par0: initial parameters. 4 by g matrix,first row is peak
#                position, second row is intensity,third row is Gaussain width,
#                fourth row is Lorentzian width
# output --     vf:voigt line shape
#           dvdpar:voigtline shape derivatives w.r.t. line parameters,length(v) by 4*g matrix
#           the format is:  [dVdv1 dVds1 dVdag1 dVdal dVdv2 dVds2 dVdag2 dVda2 ...}
    
    v0 = par0[0]
    
    s = par0[1]
    
    ag = par0[2]
    
    al = par0[3]
    
    # vectorize parameters
    aD = (np.ones((len(v),1)) * ag)
    aL = (np.ones((len(v),1)) * al)
    S = (np.ones((len(v),1)) * s)
    if par0.ndim == 1 :
        vv0 = v * np.ones((1,1)) - np.ones((len(v),1)) * v0
    else :
        vv0 = v * np.ones((1,len(v0))) - np.ones((len(v),1)) * v0
    vv0 = vv0[0]
    x = np.multiply(vv0,(np.sqrt(np.log(2)))) / aD
    x = x[0]
    y = np.ones((len(v),1)) * (al / ag) * (np.sqrt(np.log(2)))
    z = x + 1j * y
    z = z[0]
    w = special.wofz(z)
    
    #                      # University, Canada, March 2015.
    vf = w.real * np.transpose(s)
    K = w.real
    L = w.imag
    # derivatives
    dvds = K
    c1 = np.multiply(y,y)
    c2 = np.multiply(x,y)
    c2 = c2[0]
    
    dVdvj = 2 * (np.multiply(c2,K) - np.multiply(c1,L)) / aL
    dVdad = 2 * (np.multiply((np.multiply(x,x) - c1),K) - np.multiply(2 * c2,L) + y / np.sqrt(np.pi)) / aD
    dVdal = 2 * (np.multiply(c2,L) + np.multiply(c1,K) - y / np.sqrt(np.pi)) / aL
    dVdvj = dVdvj[0]
    dVdad = dVdad[0]
    dVdal = dVdal[0]
    
    vjs = np.multiply(dVdvj,S)
    ags = np.multiply(dVdad,S)
    als = np.multiply(dVdal,S)
    vjs = vjs[0]
    ags = ags[0]
    als = als[0]
    der = np.array([vjs,dvds,ags,als])
    der.resize(der.size)
    dvdpar = np.reshape(der, tuple(np.array([len(v),np.asarray(par0).size])), order="F")

    return vf,dvdpar