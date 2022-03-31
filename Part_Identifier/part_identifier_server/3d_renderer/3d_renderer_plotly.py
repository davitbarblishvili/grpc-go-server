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
        obj_name = obj_path.split('/')[-1]
        obj_name = obj_name.split('.')[0]
        fig.write_image(f"./rendered_parts/{obj_name}.png")

  
    def render_part(self, part_path, color=0.8):

        verts, faces_idx, _ = load_obj(part_path)
        faces = faces_idx.verts_idx

        # Initialize each vertex to be white in color.
        verts_rgb = color * torch.ones_like(verts)[None]  # (1, V, 3)

        # Initialize each vertex to be black in color.
        # verts_rgb_colors = torch.zeros([1, len(verts), 3])
        textures = TexturesVertex(verts_features=verts_rgb.to(self.device))

        ##################################################################################################

        mesh = Meshes(
            verts=[verts.to(self.device)],   
            faces=[faces.to(self.device)],
            textures=textures
        )

        # Render the plotly figure
        fig = plot_scene({
            "subplot1": {
                "part_mesh": mesh
            }
        })
        self.save_png(fig, part_path)
        fig.show()


        '''
        # Create a Meshes object
        mesh = Meshes(
            verts=[verts.to(self.device)],   
            faces=[faces.to(self.device)],
            textures=textures
        )
        # Render the plotly figure
        fig = plot_scene({
            "subplot1": {
                "part_mesh": mesh
            }
        })
        fig.show()
       

       
        mesh_batch = Meshes(
            verts=[verts.to(self.device), (verts + 2).to(self.device)],   
            faces=[faces.to(self.device), faces.to(self.device)]
        )
        fig = plot_scene({
            "subplot1": {
                "part_mesh1": mesh_batch[0],
                "part_mesh2": mesh_batch[1]
            }
        })
        fig.show()

       

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
        '''



if __name__ == "__main__":
    renderer = PartRenderer()
    file_paths = generate_files()
    count = 0
   
    for each_path in file_paths:
        if count == 1: 
            break
        count += 1
        renderer.render_part(each_path)
        

