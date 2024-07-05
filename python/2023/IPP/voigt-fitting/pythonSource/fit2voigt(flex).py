import numpy as np
from fadderiv import fadderiv
from scipy.optimize import least_squares

def voigtfitmin(dat = None,par = None): 
    # lsqnonlin minimiser
    # vf=voigt_f(dat[:,0],par);
    
    vf,dvdpar = fadderiv(dat[:,0],par)
    res = vf - dat[:,1]

    # Jacobian
    # if nargout > 2:
    #jac = dvdpar 
    #return res,jac
    return res
        
def fit2voigt(dat = None,par0 = None) : 
    #from input parameters calculates voigt linshape
    # input  --v: wavenumber
    #        --par0: initial parameters. 4 by g matrix,first row is peak
    #                position, second row is intensity,third row is Gaussain width,
    #                fourth row is Lorentzian width
    
    # output -- parmin: best fit parameter,
    #        -- resnom: sum fo residual squares, and so on
    
    # written by Mahmut Ruzi, Latrobe Institue for Molecular Sciences, La Trobe
    # University, Melbourne, Australia, June 2016
    # if you have any suggestions, or find any bugs, you can contact me at: mruzi17@gmail.com
    
    dat = sorted(dat, key=lambda row: (row[0]))
    dat = np.array(dat)
    ##
    # note - Gaussian and Lorentzian width ratio ahould be between 1e-4 to 100
    # so that the voigt function is accurate. for details see:
    
    # Sanjar M. Abrarov and Brendan M. Quine, A rational approximation for efficient
    # computation of the Voigt function inquantitative spectroscopy, http://arxiv.org/abs/1504.00322
    
    # Lb = np.array([0.001,10])
    
    # Gb = np.array([0.01,10])
        
    
    maxfeval = 150 * np.asarray(par0).size
    
#     if par0.ndim == 1 :
#         lb = (np.array([[np.multiply(dat[0][0],np.ones((1,1)))],
# 			[0 * np.ones((1,1))],
# 			[Gb[0] * np.ones((1,1))],
# 			[Lb[0] * np.ones((1,1))]]))
#         ub = (np.array([[np.multiply(dat[-1][0],np.ones((1,1)))],
#                         [np.inf * np.ones((1,1))],
#                         [Gb[1] * np.ones((1,1))],
#                         [Lb[1] * np.ones((1,1))]]))
#     elif par0.ndim > 1 :
#         lb = (np.array([[np.multiply(dat[0][0],np.ones((1,len(par0[0]))))],
#                         [0 * np.ones((1,len(par0[0])))],
#                         [Gb[0] * np.ones((1,len(par0[0])))],
#                         [Lb[0] * np.ones((1,len(par0[0])))]]))
#         ub = (np.array([[np.multiply(dat[-1][0],np.ones((1,len(par0[0]))))],
#                         [np.inf * np.ones((1,len(par0[0])))],
#                         [Gb[1] * np.ones((1,len(par0[0])))],
#                         [Lb[1] * np.ones((1,len(par0[0])))]]))
        
#     lb = lb.reshape(4)
#     ub = ub.reshape(4)

    bounds = (-np.inf, np.inf)
    parmin = least_squares(lambda par : voigtfitmin(dat,par),par0,jac = '3-point', method = 'trf',ftol=1e-8,bounds = bounds, xtol=1e-6, max_nfev=maxfeval, verbose=0)
    ##


        

    return parmin['x']