import sys
import os
from generate_file_paths import generate_files
sys.path.append(os.path.abspath(''))
import torch
from pytorch3d.transforms import RotateAxisAngle
from pytorch3d.transforms import Translate
from pytorch3d.io import load_obj
from pytorch3d.structures import Meshes
from pytorch3d.vis.plotly_vis import plot_scene
from pytorch3d.renderer import TexturesVertex
from loguru import logger



class PartRenderer():
    def __init__(self):
        self.count = 0
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
            torch.cuda.set_device(self.device)
        else:
            self.device = torch.device("cpu")

    def generate_orientation(self, mesh, faces, textures):
        # define rotation axis and angle
        different_orientations = []
        
        for i in range(1, 4):
            for axis in ['X', 'Y', 'Z']:
                rot_axis = RotateAxisAngle(90 * i,axis, device=self.device)
                verts_b = rot_axis.transform_points(mesh.verts_list()[0])
                trans = Translate(0,0,5, device=self.device)
                verts_b = trans.transform_points(verts_b)
                mesh_b = Meshes(verts=[verts_b], faces=[faces], textures=textures)
                different_orientations.append(mesh_b)

        return different_orientations
        

    def save_png(self, fig, obj_path):
        if self.count == 9: 
            self.count = 0

        if not os.path.exists("rendered_parts"):
            os.mkdir("rendered_parts")

        obj_name = obj_path.split('/')[-1]
        obj_name = obj_name.split('.')[0]


        fig.write_image(f"../part_recognition/rendered_parts/{obj_name}_{self.count}.png", width=1280, height=720, scale=5)
        self.count += 1

        logger.info(f"Storing orientation -> {self.count} of image -> {obj_name}")

  
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

        new_meshes = self.generate_orientation(mesh, faces, textures)

        # Render the plotly figure
        for new_mesh in new_meshes:
            fig = plot_scene({
                "": {
                    "": new_mesh,
                }, 
            }, 
            )

            # save 2d image
            self.save_png(fig, part_path)
            #fig.show()

        
if __name__ == "__main__":
    renderer = PartRenderer()
    logger.info("Started Loading Images")
    file_paths = generate_files()
    logger.info("Completed Loading Images")
   
    count = 0
    for each_path in file_paths:
        renderer.render_part(each_path)

    logger.info("Completed Saving Rendered Images")
        

