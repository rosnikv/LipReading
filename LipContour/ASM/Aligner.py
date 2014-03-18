from itertools import izip
from yaml import load
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader
from numpy import array, zeros, asarray, dot, sum, searchsorted, int
from Utils import visualize,integral_img,clip_corners,scale_face,get_patch
from Haar import haar_types

def load_yaml(filename):
	return load(open(filename,'r'),Loader=Loader)

def extract_xy(dct):
	return [dct['x'],dct['y']]

def scaled_viz(points,fname,index,num_points,scale,offsets,face_rect):
	pts = (points.reshape((num_points,2))*scale).astype(int)+offsets
	visualize(fname,pts,index,face_rect)

class Aligner(object):
	def __init__(self,yaml):
		if type(yaml) is type(''):
			yaml = load_yaml(yaml)
		self.num_points = yaml['num_points']
		self.max_iterations = yaml['max_iterations']
		self.step_size = yaml['step_size']
		self.image_size = array(yaml['image_size'])
		self.patch_size = array(yaml['patch_size'])
		self.features = []
		self.mean = zeros(self.num_points*2)
		self.basis = zeros((self.num_points*2,len(yaml['features'][0]['basis_vectors'])))
		for i,fyaml in enumerate(yaml['features']):
			self.features.append(Feature(fyaml))
			self.mean[i*2:i*2+2] = extract_xy(fyaml['mean_position'])
			self.basis[i*2:i*2+2] = array(map(extract_xy,fyaml['basis_vectors'])).T
	
	def project(self,shape):
		# project shape back onto basis vectors
		return self.mean + dot(self.basis,dot(self.basis.T,shape-self.mean))

	def align_face(self,face_rect,pvimg):
		if not face_rect:
			print "Skipping",pvimg.filename,"... no face detected"
			return []
		print "aligning face (%d,%d):%dx%d of"%face_rect,pvimg.filename

		offsets,scale,img = scale_face(face_rect,pvimg,self.image_size)
		scoff = (offsets/scale).astype(int) # offsets for the scaled image
		integral = integral_img(img)
		points = self.mean
		scaled_viz(points,pvimg.filename,0,self.num_points,scale,offsets,face_rect)
		# meat: iteratively align each feature
		for n in range(self.max_iterations):
			for i,feat in enumerate(self.features):
				patch = get_patch(points[i*2:i*2+2]+scoff,integral,self.patch_size)
				if patch is None: continue
				points[i*2:i*2+2] -= self.step_size*feat.align(patch)
			points = self.project(points) # project back onto face basis
			scaled_viz(points,pvimg.filename,n+1,self.num_points,scale,offsets,face_rect)
		# translate back to original img coords 
		return (points.reshape((self.num_points,2))*scale).astype(int)+offsets
		# Michael's return: scaled so the face_rect is (0,0,1,1)
		#return points.reshape((self.num_points,2))/self.image_size


class Feature(object):
	def __init__(self,yaml):
		self.name = yaml['name']
		locator = yaml['locator']
		self.x_regressors = [Regressor(x) for x in locator['x']]
		self.y_regressors = [Regressor(y) for y in locator['y']]

	def align(self,patch):
		return sum((array(map(lambda r: r.apply(patch),regs))
			for regs in izip(self.x_regressors,self.y_regressors)))

class Regressor(object):

	def __init__(self,yaml):
		img_feat = yaml['image_feature']
		feature_rect = img_feat['rect']
		ul = array(feature_rect[:2])  # upper left corner
		dim = array(feature_rect[2:]) # width, height
		self.apply = lambda p: self.test_haar(haar_types[img_feat['type']](p,ul,dim))
		self.thresholds = yaml['thresholds'] # assert that they're in sorted order?
		self.coeffs = yaml['coefficients']

	def test_haar(self,h_value):
		return self.coeffs[searchsorted(self.thresholds,h_value,side='right')]

