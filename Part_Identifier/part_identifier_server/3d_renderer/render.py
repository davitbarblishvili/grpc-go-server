from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import os

def absoluteFilePaths(directory):
    paths = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            paths.append(os.path.abspath(os.path.join(dirpath, f)))
    return paths

def create3DPlot(paths):
    for path in paths: 
        print(path)
        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure, auto_add_to_figure=False)
        figure.add_axes(axes)

        # Load the STL files and add the vectors to the plot
        your_mesh = mesh.Mesh.from_file(path)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

        # Auto scale to the mesh size
        scale = your_mesh.points.flatten('F')
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()

resp = absoluteFilePaths("/Users/dbarblishvili/go/src/grpc-go-course/Part_Identifier/part-finder-data")
print(resp)
create3DPlot([resp[3]])