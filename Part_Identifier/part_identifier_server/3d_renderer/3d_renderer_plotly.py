import os
import torch
import matplotlib.pyplot as plt

# Util function for loading meshes
from pytorch3d.io import load_objs_as_meshes, load_obj

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
    TexturesUV,
    TexturesVertex
)

# add path for demo utils functions 
import sys
import os
sys.path.append(os.path.abspath(''))


if torch.cuda.is_available():
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)
else:
    device = torch.device("cpu")



verts, faces_idx, _ = load_obj(
"/Users/dbarblishvili/go/src/grpc-go-course/Part_Identifier/part_identifier_server/3d_renderer/data/obj/1115833-00-A.obj")
faces = faces_idx.verts_idx

# Initialize each vertex to be white in color.
#verts_rgb = torch.ones_like(verts)[None]  # (1, V, 3)

# Initialize each vertex to be black in color.
verts_rgb_colors = torch.zeros([1, len(verts), 3])
textures = TexturesVertex(verts_features=verts_rgb_colors.to(device))

##################################################################################################

# Create a Meshes object
mesh = Meshes(
    verts=[verts.to(device)],   
    faces=[faces.to(device)],
    textures=textures
)

# Render the plotly figure
fig = plot_scene({
    "subplot1": {
        "part_mesh": mesh
    }
})
fig.show()

##################################################################################################



##################################################################################################
mesh = Meshes(
    verts=[verts.to(device)],   
    faces=[faces.to(device)]
)

# Render the plotly figure
fig = plot_scene({
    "subplot1": {
        "part_mesh": mesh
    }
})
fig.show()
##################################################################################################




##################################################################################################
mesh_batch = Meshes(
    verts=[verts.to(device), (verts + 2).to(device)],   
    faces=[faces.to(device), faces.to(device)]
)


fig = plot_scene({
    "subplot1": {
        "part_mesh1": mesh_batch[0],
        "part_mesh2": mesh_batch[1]
    }
})
fig.show()

##################################################################################################


##################################################################################################

fig2 = plot_scene({
    "part_plot1": {
        "part": mesh_batch
    }
},
    xaxis={"backgroundcolor":"rgb(200, 200, 230)"},
    yaxis={"backgroundcolor":"rgb(230, 200, 200)"},
    zaxis={"backgroundcolor":"rgb(200, 230, 200)"}, 
    axis_args=AxisArgs(showgrid=True))
fig2.show()

##################################################################################################


