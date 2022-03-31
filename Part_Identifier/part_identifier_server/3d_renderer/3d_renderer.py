import os
import sys
import torch
import os
import torch
import matplotlib.pyplot as plt

# Util function for loading meshes
from pytorch3d.io import load_objs_as_meshes,load_obj

# Data structures and functions for rendering
from pytorch3d.structures import Meshes
from pytorch3d.vis.plotly_vis import AxisArgs, plot_batch_individually, plot_scene
from pytorch3d.vis.texture_vis import texturesuv_image_matplotlib
from pytorch3d.renderer import (
    look_at_view_transform,
    FoVPerspectiveCameras, 
    PointLights, 
    DirectionalLights, 
    Materials, 
    RasterizationSettings, 
    MeshRenderer, 
    MeshRasterizer,  
    SoftPhongShader,
    HardPhongShader,
    TexturesUV,
    TexturesVertex
)

# add path for demo utils functions 
import sys
import os
sys.path.append(os.path.abspath(''))
from plot_image_grid import image_grid


if torch.cuda.is_available():
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)
else:
    device = torch.device("cpu")

#Load a mesh and texture file
# Set paths
DATA_DIR = "./data"
obj_filename = os.path.join(DATA_DIR, "./obj/1619574-00-A.obj")

verts, faces_idx, _ = load_obj("/Users/dbarblishvili/go/src/grpc-go-course/Part_Identifier/part_identifier_server/3d_renderer/data/obj/1115833-00-A.obj")
faces = faces_idx.verts_idx

# Initialize each vertex to be white in color.
verts_rgb = torch.ones_like(verts)[None]  # (1, V, 3)

# Initialize each vertex to be black in color.
# verts_rgb_colors = torch.zeros([1, len(verts), 3])
textures = TexturesVertex(verts_features=verts_rgb.to(device))

##################################################################################################
mesh = Meshes(
            verts=[verts.to(device)],   
            faces=[faces.to(device)],
            textures=textures
        )

# Load obj file
#mesh = load_objs_as_meshes([obj_filename], device=device)

# Let's visualize the texture map
#plt.figure(figsize=(7,7))
#texture_image=mesh.textures.maps_padded()
#plt.imshow(texture_image.squeeze().cpu().numpy())
#plt.axis("off")
#plt.show()





# PyTorch3D has a built-in way to view the texture map 
# with matplotlib along with the points on the map corresponding to vertices.
#plt.figure(figsize=(7,7))
#texturesuv_image_matplotlib(mesh.textures, subsample=None)
#plt.axis("off")
#plt.show()





# create a renderer
R, T = look_at_view_transform(2.7, 0, 180) 
cameras = FoVPerspectiveCameras(device=device, R=R, T=T)

# Define the settings for rasterization and shading. Here we set the output image to be of size
# 512x512. As we are rendering images for visualization purposes only we will set faces_per_pixel=1
# and blur_radius=0.0. We also set bin_size and max_faces_per_bin to None which ensure that 
# the faster coarse-to-fine rasterization method is used. Refer to rasterize_meshes.py for 
# explanations of these parameters. Refer to docs/notes/renderer.md for an explanation of 
# the difference between naive and coarse-to-fine rasterization. 
raster_settings = RasterizationSettings(
    image_size=512, 
    blur_radius=0.0, 
    faces_per_pixel=1, 
)

# Place a point light in front of the object. As mentioned above, the front of the cow is facing the 
# -z direction. 
lights = PointLights(device=device, location=[[0.0, 0.0, -3.0]])

# Create a Phong renderer by composing a rasterizer and a shader. The textured Phong shader will 
# interpolate the texture uv coordinates for each vertex, sample from a texture image and 
# apply the Phong lighting model
renderer = MeshRenderer(
    rasterizer=MeshRasterizer(
        cameras=cameras, 
        raster_settings=raster_settings
    ),
    shader=SoftPhongShader(
        device=device, 
        cameras=cameras,
        lights=lights
    )
)

# render the mesh
images = renderer(mesh)
plt.figure(figsize=(10, 10))
plt.imshow(images[0, ..., :3].cpu().numpy())
plt.axis("off")
plt.show()

