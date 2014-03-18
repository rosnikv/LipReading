#!/usr/bin/env python

from sys import argv,exit
from numpy import array,ones,load,fromiter
from pickle import dump as pdump
from Haar import haar_fns
from time import time

def train_feature(patches_fname,offsets_fname,f,haars_per_feat):
	patches,offsets = load(patches_fname),load(offsets_fname)
	haar_locs = load("haar_locs.pyz")
	x_regressors = boost(patches,offsets[:,0],haars_per_feat,haar_locs)
	y_regressors = boost(patches,offsets[:,1],haars_per_feat,haar_locs)
	pdump(x_regressors,open("x_regressors_%d.pyz"%f,'w'),-1)
	pdump(y_regressors,open("y_regressors_%d.pyz"%f,'w'),-1)
		
def boost(patches,offsets,haars_per_feat,haar_locs):
	regs = []
	tic = time()
	for i in xrange(haars_per_feat):
		rect,htype,th,lo,hi,lo_slice,hi_slice = select_haar(patches,offsets,haar_locs)
		regs.append((rect,htype,th,lo,hi))
		offsets[lo_slice] -= lo*0.5 # TODO: maybe use some percentage
		offsets[hi_slice] -= hi*0.5
	print "boost took:",time()-tic
	return regs

def select_haar(patches,offsets,haar_locs):
	# iterate over all the haar feature type/size/locations and learn the regressors
	min_err = 99999
	best_haar = (None,None,0,0,0,None,None) # rect,htype,th,lo,hi,loslice,hislice
	for ul,dim in haar_locs: 
		for hfn in haar_fns:
			vals = fromiter((hfn(p,ul,dim) for p in patches),dtype=patches.dtype,count=len(patches))
			th,lo,hi,err = fit_regression_stump(vals,offsets)
			if err < min_err:
				min_err = err
				best_haar = (ul.tolist()+dim.tolist(),haar_fns[hfn],th,lo,hi,offsets[vals<=th],offsets[vals>th])
	return best_haar

# adapted from fitRegressionStump.m
def fit_regression_stump(vals,offsets):
	w = ones(len(offsets))/float(len(offsets)) # fake weights
	si = vals.argsort()
	vals,offsets = vals[si],offsets[si]
	cum_w = w.cumsum()
	cum_offs = (offsets*w).cumsum()
	sum_offs = cum_offs[-1]
	cum_w_conj = 1 - cum_w
	cum_offs_conj = sum_offs - cum_offs
	b = cum_offs / cum_w # averages at each
	a = cum_offs_conj/cum_w_conj - b
	error = (w*offsets**2).sum() - 2*a*cum_offs_conj - 2*b*sum_offs + (a**2+2*a*b)*cum_w_conj + b**2
	k = error.argmin()
	if k == len(vals)-1: # last element
		thresh = vals[k]
	else:
		thresh = (vals[k] + vals[k+1])/2.
	return thresh,b[k],a[k]+b[k],error[k]

if __name__ == "__main__":
	if len(argv) != 3:
		exit("Usage: %s feat_idx haars_per_feat"%argv[0])
	f,hpf = int(argv[1]),int(argv[2])
	print "starting to train feature %d, with %d haar features"%(f,hpf)
	train_feature("patches_%d.npz"%f,"offsets_%d.npz"%f,f,hpf)
