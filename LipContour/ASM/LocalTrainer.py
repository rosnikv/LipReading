from Trainer import *
from boost_feature import boost

class LocalTrainer(Trainer):

	def train(self):
		super(LocalTrainer,self).train()
		# train the locators
		self.locators = [ self.__train_feature(f) for f in xrange(self.num_features) ]
	
	def __train_feature(self,f):
		patches,offsets = self.get_patches(f)
		x_regressors = boost(patches,offsets[:,0],self.haars_per_feat,self.haar_locs)
		y_regressors = boost(patches,offsets[:,1],self.haars_per_feat,self.haar_locs)
		return x_regressors, y_regressors
		
	def export_aligner(self,fname):
		yaml = {'num_points': self.num_features,
			    'max_iterations': self.max_iterations,
				'step_size': self.step_size,
				'image_size': self.image_size.tolist(),
				'patch_size': self.patch_size.tolist()
				}
		yaml['features'] = [self.mk_feature(i) for i in xrange(self.num_features)]
		dump(yaml,open(fname,'w'),Dumper)
	
# end class LocalTrainer

