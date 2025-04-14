from shaders.create_thinfilm_shader import create_shader_material
from geometry_nodes.create_geometry_nodes import create_geometry_node_group
from animate.animate_deformation import setup_animation
from render.render_output import render_animation


def main():
    create_shader_material()
    create_geometry_node_group()
    setup_animation()
    render_animation()
