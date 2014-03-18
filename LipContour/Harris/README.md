            The Harris (or Harris & Stephens) corner detection algorithm is one of the simplest corner indicators available. The general idea is to locate points where the surrounding neighborhood shows edges in more than one direction, these are then corners or interest points.
            In short, a matrix W is created from the outer product of the image gradient, this matrix is averaged over a region and then a corner response function is defined as the ratio of the determinant to the trace of W.
First we need to be able to do convolutions of 2D signals. For this NumPy is not enough and we need to use the signal module in SciPy.
           The point of using Gaussian derivative filters here is that this computes a smoothing of the image, to a scale defined by the size of the filter, and the derivatives at the same time. The derivatives are less noisy than if computed with a simple difference filter on the original image.
           Picking all values above a threshold with the additional constraint that corners must be separated with a minimum distance is an approach that often gives good results. To do this, take all candidate pixels, sort them in descending order of corner response values and mark off regions too close to positions already marked as corners.
          Then we detected corner points in the image, and the points are plotted and overlaid on the original image. This approach was little bit different from the harris corner detection available in wikipedia.

Problems:  

          The cropped mouth region images were the output to these, So for different images it locates different corner points.And corner points may be 2 or 3 in number..or sometimes more than 5, it was difficult to distinguish some special features from lip area using harris corner detection and we were sure that this points only won’t deal with SVM classification and predicting words.Hence have to drop this method from our proposed system implementation.
