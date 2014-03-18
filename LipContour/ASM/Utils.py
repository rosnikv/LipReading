from itertools import product
from cv import HaarDetectObjects, CreateMemStorage
from numpy import array, int, float, asarray, zeros
from Image import Image as pvImage
from os.path import splitext,basename

def detect_faces(pvimg,cascade):
	#print "detecting face in:",pvimg.filename
	rects = HaarDetectObjects(pvimg.asOpenCVBW(),cascade,CreateMemStorage())
	if len(rects) == 0: return False
	return [r[0] for r in rects] # discard neighbors value

def read_pointsfile(path):
	f = open(path)
	f.readline() # ignore version num
	n = int(f.readline().split()[-1]) # number of points
	f.readline() # ignore open brace
	return array(map(lambda _: map(float,f.readline().split()),xrange(n)))

def visualize(fname,points,index=None,face_rect=None):
	pvimg = pvImage(fname)
	for p in points: pvimg.annotatePoint(p)
	if index: pvimg.annotateLabel((0,0),str(index))
	if face_rect: pvimg.annotateRect(face_rect)
	name,ext = splitext(basename(fname))
	pvimg.asAnnotated().save("%s_viz%s%s"%(name,'_%02d'%index if index else '',ext))

def integral_img(img):
	if type(img) != type(array(0)):
		img = asarray(img).T # make it a numpy ndarray (which for some reason transposes things)
	itg = zeros((img.shape[0]+1,img.shape[1]+1),dtype=int)
	for i,j in product(xrange(img.shape[0]),xrange(img.shape[1])):
		itg[i,j] = img[i,j]+itg[i,j-1]+itg[i-1,j]-itg[i-1,j-1]
	return itg  #keep the 1px 0-strip at [:-1,:-1]

def clip_corners(ul,br,shape):
	'''Bounds fixer for upper-left and bottom-right corners, given the shape of the image/matrix'''
	a = array([ul,zeros((2))        ]).max(axis=0).astype(int)
	b = array([br,array(shape)-(1,1)]).min(axis=0).astype(int)
	return a,b

def scale_face(rect,pvimg,scale_size): #uses same technique as reference
	scale = scale_size/array(rect[2:],dtype=float)
	img = pvimg.asPIL().convert('L').resize((pvimg.size*scale).astype(int))
	return rect[:2],1.0/scale,img # offsets, scale, and the image

def get_patch(point,integral,patch_size):
	'''Extracts a patch from an integral image centered at the given point'''
	half_patch = (patch_size/2).astype(int)
	ul,br = point-half_patch,point+half_patch+1
	if ul.min() < 0 or br[0] >= integral.shape[0] or br[1] >= integral.shape[1]:
		return None # patch is out of bounds
	return integral[ul[0]:br[0],ul[1]:br[1]]

