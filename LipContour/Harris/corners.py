from PIL import Image
import harris
import numpy


im = numpy.array(Image.open('mouth34.jpg').convert("L"))
harrisim = harris.compute_harris_response(im)
filtered_coords = harris.get_harris_points(harrisim,6)
harris.plot_harris_points(im, filtered_coords)