            Chan-Vese model for active contours is a powerful and flexible method which is able to segment many types of images, including some that would be quite difficult to segment in means of "classical" segmentation – i.e., using thresholding or gradient based methods.The model is based on an energy minimization problem, which can be reformulated in the level set formulation, leading to an easier way to solve the problem.This is used widely in the medical imaging field, especially for the segmentation of the brain, heart etc.
We tried to modify it for finding out the the edge of lips so that through that we can track the lip movements.
           Initialize a mask (rectangle), which will then move and detect corners through large number of iterations, we used 1000 iterations here for accuracy.

Problems :

*It was not effective to find edges of images in all conditions, it depends on the lip structure ,the light exposure to the images etc.

*The accuracy of segmentation mainly depends on the size and position of initial mask.For different lip images(closed,opened etc) different size and position gives accurate segmentation. But its not possible to change the initial mask in the case of REAL TIME AUTOMATIC segmentation.

(from deepthi's exploration)
