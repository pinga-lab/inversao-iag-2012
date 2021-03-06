from os import path
from matplotlib import pyplot
import numpy
from fatiando.mesher.dd import SquareMesh
from fatiando.seismic import traveltime, srtomo
from fatiando import vis, logger, utils, inversion
import cPickle as pickle

params = __import__('exercicio2_entrada')
area = (0, 5, 0, 5)
with open(params.dados) as f:
    model, src_loc, rec_loc, tts, error = pickle.load(f)
shape = model.shape
vmin, vmax = model.props['vp'].min(), model.props['vp'].max()
srcs, recs = utils.connect_points(src_loc, rec_loc)
mesh = SquareMesh(area, shape)
solver = inversion.linear.overdet(mesh.size)
results = srtomo.run(tts, srcs, recs, mesh, solver)
estimate, residuals = results

pyplot.figure(figsize=(14, 5))
pyplot.subplot(1, 2, 1)
pyplot.axis('scaled')
pyplot.title('Tomografia')
vis.map.squaremesh(mesh, estimate, vmin=1./vmax, vmax=1./vmin,
    cmap=pyplot.cm.gist_gray)
cb = pyplot.colorbar()
cb.set_label('Vagarosidade')
pyplot.subplot(1, 2, 2)
pyplot.grid()
pyplot.title('Residuos (erro %g s)' % (error))
pyplot.hist(residuals, color='gray', bins=10)
pyplot.xlabel("Segundos")
pyplot.show()
