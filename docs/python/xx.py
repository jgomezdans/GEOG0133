#! /usr/bin/env python
from kernels import *
import numpy as np
import pylab as plt

#load the data, as above
infile = 'data.npz'
data = np.load(infile)
r = data['reflectance']
vza = data['vza']
sza = data['sza']
raa = data['raa']
wavebands = data['wavebands']
mask = data['mask']
doy = data['doy']
lclut = data['landCoverLUT']
lc = data['landcover']
fireday = data['activeFire']
#mask[doy < 110,0,0] = False
# calculate the kernels
k = Kernels(vza[mask],sza[mask],raa[mask],LiType='Dense',RossHS=False,doIntegrals=False)

# data
red = r[:,0,:,:][mask]
nir = r[:,1,:,:][mask]
doys = doy[mask[:,0,0]]

H = np.matrix([k.Isotropic,k.Ross,k.Li])
X = np.zeros(3)
Y = red[0]
R_red = np.eye(1) * 0.01**2
R_nir = np.eye(1) * 0.06**2
# observation uncertainty

# model
M = np.eye(3)
# model uncertainty
Q_red = np.eye(3) * 0.005**2
Q_nir = np.eye(3) * 0.02**2

# initial conditions
x0_red = np.array([0.08996554, 0.0083535, 0.04541085])
x0_nir = np.array([0.44320984, 0.3960118, 0. ])
C_red = np.eye(3) * 0.2**2
C_nir = np.eye(3) * 0.5**2

import kalman
# red
kfr = kalman.Kalman(red,x0_red,C_red,R_red,M,Q_red,H,doys)
plt.clf()
kfr.run()
plt.ylim(0,1)
plt.errorbar(kfr.alldoys,kfr.x[:,0],yerr=np.sqrt(kfr.C[:,0,0]),fmt='ro',label='fiso')
plt.errorbar(kfr.alldoys,kfr.x[:,1],yerr=np.sqrt(kfr.C[:,1,1]),fmt='bo',label='fvol')
plt.errorbar(kfr.alldoys,kfr.x[:,2],yerr=np.sqrt(kfr.C[:,2,2]),fmt='go',label='fgeo')
plt.legend(loc='best')
plt.savefig('figures/kernelsKFred.png')

plt.clf()
plt.plot(kfr.sample_doys,kfr.y,'o',label='obs')
plt.plot(kfr.sample_doys,kfr.fwd,'+',label='fwd')
plt.legend(loc='best')
plt.savefig('figures/kernelsKFfwdred.png')

# nir
plt.clf()
kfn = kalman.Kalman(nir,x0_nir,C_nir,R_nir,M,Q_nir,H,doys)
kfn.run()
plt.ylim(0,1)
plt.errorbar(kfn.alldoys,kfn.x[:,0],yerr=np.sqrt(kfn.C[:,0,0]),fmt='ro',label='fiso')
plt.errorbar(kfn.alldoys,kfn.x[:,1],yerr=np.sqrt(kfn.C[:,1,1]),fmt='bo',label='fvol')
plt.errorbar(kfn.alldoys,kfn.x[:,2],yerr=np.sqrt(kfn.C[:,2,2]),fmt='go',label='fgeo')
plt.legend(loc='best')
plt.savefig('figures/kernelsKFnir.png')

plt.clf()
plt.plot(kfn.sample_doys,kfn.y,'o',label='obs')
plt.plot(kfn.sample_doys,kfn.fwd,'+',label='fwd')
plt.legend(loc='best')
plt.savefig('figures/kernelsKFfwdnir.png')



