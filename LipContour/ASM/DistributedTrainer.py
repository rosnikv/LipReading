from Trainer import *
from pickle import dump as pdump
from numpy import load
from subprocess import Popen
from time import sleep
from glob import glob

class DistributedTrainer(Trainer):
	def __init__(self):
		super(DistributedTrainer,self).__init__()
		pdump(self.haar_locs,open("haar_locs.pyz",'w'),-1)

	def train(self):
		super(DistributedTrainer,self).train()
		# train the locators
		subprocesses = [ self.__train_feature(f) for f in xrange(self.num_features) ]
		while any(sp.poll() is None for sp in subprocesses):
			sleep(30) # wait 30 seconds
		while len(glob("*_regressors_*")) < self.num_features*2:
			sleep(30)

	def __train_feature(self,f):
		patches,offsets = self.get_patches(f)
		patches.dump("patches_%d.npz"%f)
		offsets.dump("offsets_%d.npz"%f)
		return Popen('echo "python boost_feature.py %d %d" | qsub -cwd -N boost_%d'%(f,self.haars_per_feat,f),shell=True)
		#return Popen(['./boost_feature.py',str(f),str(self.haars_per_feat)])

	def __read_locator(self,idx):
		x_regs = load(open("x_regressors_%d.pyz"%idx,'r'))
		y_regs = load(open("y_regressors_%d.pyz"%idx,'r'))
		return x_regs,y_regs

	def export_aligner(self,fname):
		# collect data from distributed processes
		self.locators = [self.__read_locator(f) for f in xrange(self.num_features)]
		yaml = {'num_points': self.num_features,
			    'max_iterations': self.max_iterations,
				'step_size': self.step_size,
				'image_size': self.image_size.tolist(),
				'patch_size': self.patch_size.tolist()
				}
		yaml['features'] = [self.mk_feature(i) for i in xrange(self.num_features)]
		dump(yaml,open(fname,'w'),Dumper)
	
# end class DistributedTrainer
