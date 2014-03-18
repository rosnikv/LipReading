from yaml import dump
try:
	from yaml import CDumper as Dumper
except ImportError:
	from yaml import Dumper
from numpy import array,int,zeros,ones,dot
from numpy.linalg import eig
from itertools import product,izip
from Utils import *

feature_names = ['left eye (center)','right eye (center)',
'mouth (left)','mouth (right)',
'left eyebrow (left)','left eyebrow (right)',
'right eyebrow (left)','right eyebrow (right)',
'left temple','left eye (left)','left eye (right)',
'right eye (left)','right eye (right)','right temple',
'nose (center)','nose (left)','nose (right)',
'mouth (top)','mouth (bottom)','chin']

class Trainer(object):
	def __init__(self):
		# constants/parameters
		self.num_features = 20
		self.max_iterations = 10
		self.step_size = 0.5
		self.image_size = array((60,60))
		self.patch_size = array((24,24))
		self.jitter = 4 # amount to slide patches l/r/u/d
		self.haars_per_feat = 8
		self.num_princomps = 15
		# data
		self.training_imgs = []
		self.truth_points = []
		self.haar_locs = list(self.haar_generator()) # enumerate them all TODO: sample from this

	def haar_generator(self):
		for ul in (array(u) for u in product(xrange(self.patch_size[0]),xrange(self.patch_size[1]))):
			for dim in (array(d) for d in product(xrange(1,self.patch_size[0]-ul[0]),xrange(1,self.patch_size[1]-ul[1]))):
				yield ul,dim
	
	def add_training_image(self,pvimg,pts,face_rect):
		assert len(pts) == self.num_features
		offsets,scale,img = scale_face(face_rect,pvimg,self.image_size)
		pts = ((pts-offsets)/scale).astype(int) # convert to face coords
		self.training_imgs.append(integral_img(img))
		self.truth_points.append(pts)

	def train(self):
		self.truth_points = array(self.truth_points)
		self.mean_shape = self.truth_points.mean(0)
		# compute basis (PCA)
		c = (self.truth_points - self.mean_shape).reshape(len(self.truth_points),-1) # features are col vectors
		ct = c.transpose()
		vals,vecs = eig(dot(c,ct))
		self.basis = dot(ct,vecs[vals.argsort()[::-1]])[:,:min(self.num_princomps,len(c))].reshape(-1,self.num_features,2)
	
	def get_patches(self,f):
		patches,offsets = [],[]
		for i,point in enumerate(self.truth_points[:,f,:]): # for each training image
			for coord in self.__gen_patch_coords(point,self.training_imgs[i].shape):
				p = get_patch(coord,self.training_imgs[i],self.patch_size)
				if p is None: continue
				patches.append(p)
				offsets.append(coord-point)
		patches,offsets = array(patches),array(offsets)
		print f,patches.shape, offsets.shape
		return patches,offsets
		
	def __gen_patch_coords(self,pt,img_size):
		img_ul,img_br = self.patch_size/2,img_size-self.patch_size/2
		ul,br = pt-self.jitter,pt+self.jitter
		return product(xrange(max(0,ul[0],img_ul[0]),min(br[0],img_br[0])),
		               xrange(max(0,ul[1],img_ul[1]),min(br[1],img_br[1])))

	def mk_feature(self,idx):
		return {'name':feature_names[idx],
				'mean_position': mk_xypoint(self.mean_shape[idx,:].tolist()),
				'basis_vectors': self.basis[:,idx,:].tolist(),
				'locator': mk_xypoint(([mk_locator(h) for h in self.locators[idx][0]],
									   [mk_locator(h) for h in self.locators[idx][1]]))
				}
# end class Trainer

def mk_xypoint(pt):
	return {'x':pt[0],'y':pt[1]}
	
def mk_locator(haar):
	return {'image_feature': {'type':haar[1],'rect':haar[0]},
			'thresholds'   : [float(haar[2])],
			'coefficients' : [float(haar[3]),float(haar[4])]}

