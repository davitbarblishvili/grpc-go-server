from dis import dis
import os
import torch
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np
from math import radians
from pytorch3d.transforms import axis_angle_to_matrix
from pytorch3d.renderer.camera_utils import camera_to_eye_at_up, rotate_on_spot
from pytorch3d.transforms import RotateAxisAngle
from pytorch3d.transforms import Translate

# Util function for loading meshes
from pytorch3d.io import load_objs_as_meshes, load_obj

# Data structures and functions for rendering
from pytorch3d.structures import Meshes
from pytorch3d.vis.plotly_vis import AxisArgs, plot_batch_individually, plot_scene
from pytorch3d.vis.texture_vis import texturesuv_image_matplotlib
from pytorch3d.renderer import (
    look_at_view_transform,
    PerspectiveCameras,
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
from generate_file_paths import generate_files
sys.path.append(os.path.abspath(''))


class PartRenderer():
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
            torch.cuda.set_device(self.device)
        else:
            self.device = torch.device("cpu")

    def save_png(self, fig, obj_path):

        if not os.path.exists("rendered_parts"):
            os.mkdir("rendered_parts")

        obj_name = obj_path.split('/')[-1]
        obj_name = obj_name.split('.')[0]

        #img_bytes = fig.to_image(format="png")
        #image = Image.open(io.BytesIO(img_bytes))
        #image.show()

        fig.write_image(f"../part_recognition/rendered_parts/{obj_name}.png", width=1280, height=720, scale=5)

  
    def render_part(self, part_path, color=0.8):

        # load object file
        verts, faces_idx, _ = load_obj(part_path)
        faces = faces_idx.verts_idx

        # Initialize each vertex to be white in color.
        verts_rgb = color * torch.ones_like(verts)[None]  # (1, V, 3)

        # Initialize each vertex to be black in color.
        # verts_rgb_colors = torch.zeros([1, len(verts), 3])
        textures = TexturesVertex(verts_features=verts_rgb.to(self.device))

        ##################################################################################################

        # generate mesh
        mesh = Meshes(
            verts=[verts.to(self.device)],   
            faces=[faces.to(self.device)],
            textures=textures
        )

        # define rotation axis and angle
        rot_x = RotateAxisAngle(270,'X', device=self.device)
        rot_y = RotateAxisAngle(90,'Y', device=self.device)
        rot_z = RotateAxisAngle(90,'Z', device=self.device)
        verts_b = rot_z.transform_points(mesh.verts_list()[0])

        trans = Translate(0,0,5, device=self.device)
        verts_b = trans.transform_points(verts_b)

        # reinitialize the mesh with new orientation
        mesh_b = Meshes(verts=[verts_b], faces=[faces], textures=textures)

    
        # Render the plotly figure
        fig = plot_scene({
            "subplot1": {
                "mesh_trace_title": mesh_b,
            }, 
        
        }, 
        )

        # save 2d image
        #self.save_png(fig, part_path)
        fig.show()

        


if __name__ == "__main__":
    renderer = PartRenderer()
    file_paths = generate_files()
   
    for each_path in file_paths:
        renderer.render_part(each_path)
        break
        

