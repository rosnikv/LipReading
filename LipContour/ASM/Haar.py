### Haar module: definitions of Haar features ###

#def rect_sum(int_img,ul,br):
#	'''Sum over the rectangle defined by upper-left and bottom-right corners, in an integral image'''
#	return int_img[br[0],br[1]]-int_img[br[0],ul[1]]-int_img[ul[0],br[1]]+int_img[ul[0],ul[1]]

def horiz2(patch,ul,wh):
	br = ul + wh
	mid = ul[0]+wh[0]/2
	return patch[ul[0],ul[1]] - 2*patch[mid,ul[1]] + patch[br[0],ul[1]] - \
	       patch[ul[0],br[1]] + 2*patch[mid,br[1]] - patch[br[0],br[1]]

def horiz3(patch,ul,wh):
	br = ul + wh
	mid1 = ul[0]+wh[0]/3
	mid2 = ul[0]+wh[0]*2/3
	return patch[ul[0],ul[1]] - 2*patch[mid1,ul[1]] + 2*patch[mid2,ul[1]] - patch[br[0],ul[1]] - \
	       patch[ul[0],br[1]] + 2*patch[mid1,br[1]] - 2*patch[mid2,br[1]] + patch[br[0],br[1]]

def vert2(patch,ul,wh):
	br = ul + wh
	mid = ul[1]+wh[1]/2
	return patch[ul[0],ul[1]] - patch[br[0],ul[1]] - \
	     2*patch[ul[0],mid] + 2*patch[br[0],mid]   + \
		   patch[ul[0],br[1]] - patch[br[0],br[1]]

def vert3(patch,ul,wh):
	br = ul + wh
	mid1 = ul[1]+wh[1]/3
	mid2 = ul[1]+wh[1]*2/3
	return patch[ul[0],ul[1]] - patch[br[0],ul[1]] - \
	     2*patch[ul[0],mid1] + 2*patch[br[0],mid1] + \
	     2*patch[ul[0],mid2] - 2*patch[br[0],mid2] - \
		   patch[ul[0],br[1]] + patch[br[0],br[1]]

def diag(patch,ul,wh):
	br = ul + wh
	md = (ul+br)/2
	return patch[ul[0],ul[1]] - 2*patch[md[0],ul[1]] +   patch[br[0],ul[1]] - \
	     2*patch[ul[0],md[1]] + 4*patch[md[0],md[1]] - 2*patch[br[0],md[1]] + \
		   patch[ul[0],br[1]] - 2*patch[md[0],br[1]] +   patch[br[0],br[1]]

haar_types = {'haar_horiz2': horiz2,'haar_horiz3': horiz3,
              'haar_vert2' : vert2, 'haar_vert3' : vert3,
			  'haar_diag'  : diag}

haar_fns = {horiz2:'haar_horiz2',horiz3:'haar_horiz3',
            vert2 :'haar_vert2', vert3 :'haar_vert3',
		    diag  :'haar_diag'}
