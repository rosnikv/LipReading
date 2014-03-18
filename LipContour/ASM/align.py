#!/usr/bin/env python

from sys import argv, exit
from os.path import splitext,basename
from Image import Image as pvImage
from cv import Load as load_cascade
from numpy import loadtxt
from Utils import detect_faces,read_pointsfile,visualize
from Aligner import Aligner

def main(aligner_fname,cascade_fname,image_fnames):
	aligner = Aligner(aligner_fname)
	cascade = load_cascade(cascade_fname)
	images = (pvImage(fname) for fname in image_fnames)
	return [aligner.align_face(detect_faces(img,cascade)[0],img) for img in images]

def check_results(aligned,vs_ref=False):
	assert 'pgm' in argv[3] # only for pgms
	sse = 0.0
	for i in xrange(len(aligned)):
		bn = splitext(basename(argv[3+i]))[0].lower()
		if vs_ref: # Michael comparison
			pts = loadtxt("data/bioid/ref_impl_facepts/%s.facepts"%bn)
		else: # ground truth comparison
			pts = read_pointsfile("data/bioid/points/%s.pts"%bn)
			#visualize(argv[3+i],pts)
		err = ((aligned[i]-pts)**2).sum()
		print bn,err
		sse += err
	print "total error:",sse
	print "avg per img:",sse/float(len(aligned))

if __name__ == '__main__':
	if len(argv) < 4 or splitext(argv[1])[-1] != '.yaml' or splitext(argv[2])[-1] != '.xml':
		exit("Usage: %s trained_aligner.yaml haar_cascade.xml image(s)"%argv[0])
	aligned = main(argv[1],argv[2],argv[3:])

	if False:
		check_results(aligned)
