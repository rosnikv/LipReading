#!/usr/bin/env python

from sys import argv, exit
from glob import glob
from itertools import izip,islice
from Image import Image as pvImage
from cv import Load as load_cascade
from Utils import read_pointsfile,detect_faces
#from LocalTrainer import LocalTrainer as Trainer
from DistributedTrainer import DistributedTrainer as Trainer

def main(img_dir,pts_dir,haar_file,num_trains):
	t = Trainer()
	cascade = load_cascade(haar_file)
	sglob = lambda dir: sorted(glob(dir+"/*"))
	paths = izip(sglob(img_dir),sglob(pts_dir))
	# split into training and testing
	for im,pf in islice(paths,num_trains):
		img = pvImage(im)
		pts = read_pointsfile(pf)
		faces = detect_faces(img,cascade)
		if faces:
			t.add_training_image(img,pts,faces[0])
		else:
			print "No face found for %s"%im
	t.train()
	t.export_aligner('aligner.yaml')

if __name__ == '__main__':
	if len(argv) != 5:
		exit("Usage: %s image_dir points_dir haar_cascade num_training_images"%argv[0])
	main(argv[1],argv[2],argv[3],int(argv[4]))

