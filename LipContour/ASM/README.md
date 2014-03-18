Active Shape Model 

Basic Terms

Aligning shapes: alignment is a transformation which yields the minimum distance between the shapes.
Output of ASM search algorithm is (x,y) coordinates of the face landmarks.

Shape Model : allowable set of shapes.matrix formula is used for shape model which represents the relation between the points.

Points distribution model : learn allowable shape constellations of shape points from training samples.
PCA is used to build the model

profile model:specifies what the image is expected to look like around the landmarks.

Shape mode : allowable relative position of landmarks.
During search shape model adjusts the shape suggested by profile model to confirm to a legitimate face shape.
Shape model must convert profile model to an allowable face shape.
Before building the shape model align the training shapes. Then shape model consists of an average face and allowable distortions of average face.
ASM ‘s advantage that they did not require a handcrafted model, although the training images had to be manually landmarked.

          ASMs build models by training on a set of reference images,which means that they mechanically extract important characteristics of the training set. In practice, hand tuning is still needed to get best results for a specific application.

WORKING OF ASM:
           The ASM search starts with a start shape: the start shape is the model mean shape aligned to the overall position and size of the face found by a global face detector.Two global face detectors are mainly used:
The Rowley detector: uses a committee of neural networks. The Rowley detector provide eye positions in addition to the face position. Although it is has a worse detection rate and is slower than the Viola Jones detector.
           The Viola Jones detector:uses a method which accumulates the results of many weak classifiers, each of which looks for a very simple image feature.
Before the ASM search begins, we use a global face detector to locate the approximate position and size of the face. We then generate a start shape by using this position and size to position and scale the model mean face.
The quality of the start shape is important. It is is unlikely that an ASM search will recover completely from a bad start shape.

1. Align the mean shape to the reference (i.e. the manually land-marked) shape.

2. Face Scale and align the mean shape to the face position determined by the face detector.

3. Scale and align the mean shape to the face and eye positions determined by the face detector.

4. Generate an initial StartShape. Then generate another start shape, StartShapeEyes, by aligning the mean shape to the eye position found by the face detector (ignoring the overall face position found by the face detector). If the inter-eye distance in StartShapeEyes is very different from StartShape, then blend the eyes in StartShapeEyes into StartShape. Use the resulting StartShape as the start shape.The net effect is to use eye positions to correct start shapes that are too big.
During profile matching, we search in the vicinity of each landmark for the best profile match. In this section we look at two parameters:
1. The number of pixels in the model profile for each 1D landmark. This width is always an odd number: the middle pixel plus an equal number of pixels on each side of the center pixel. For example, nProfWidth=11 means a middle pixel and 5 pixels on each side.
2. During search, we sample the image at displacements of  -n to +n PixelSearch pixels along the whisker.

The profile match at each landmark suggests a displacement from the current position. We declare convergence and stop iterating when either of the following conditions is met:

1.maximum iteration is reached.

2.Total displacements (of n) of the landmark displacements are less than or equal to the maximum displacement of n PixelSearchs.
During the landmark search, we generate a suggested shape by profile matching and then confirm the suggested shape to the shape model.Using flexible shape model allows bad profile matches to pass unchecked and so does not give the best results when searching.

PROBLEMS WITH ASM

1.Lights and background
lighting effects and small differences in pose and facial symmetry usually make the image texture on one side of the face quite different from the other — in fact, often more so than the texture across two images of the same individual. This can affect the asm and can cause it not to identify.lighting must be uniform for most images in each dataset.

2.Huge amount of data set
The generalization ability of the detector is determined by the range of faces in the training data. From this perspective, three or five  datasets are not completely satisfactory. It should also be said that the image sets exclude anyone with unusual looks (very overweight, etc.).

3.Skin discrimination
Most of the people in the images are Caucasian. When the african or asian images are validated on the basis of Caucasians, the system may fail to identify.

4.Problems with landmarking
Manual landmarking is not a perfect process and a close examination of the data reveals some discrepancies.For effective training and testing we need a sufficient number of samples of uncorrelated data.


(data from preethu's exploration) 
