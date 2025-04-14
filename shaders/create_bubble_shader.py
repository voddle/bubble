import bpy


def create_bubble_shader():
    # create material
    mat_name = "Bubble_ThinFilm_Material"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # clean
    for node in nodes:
        nodes.remove(node)

    # add node
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (600, 0)

    diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")
    diffuse.location = (400, 0)

    ramp = nodes.new(type="ShaderNodeValToRGB")
    ramp.location = (200, 0)
    ramp.color_ramp.interpolation = "LINEAR"

    # rainbow
    ramp.color_ramp.elements[0].color = (1, 0, 0, 1)
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements.new(0.33).color = (0, 1, 0, 1)
    ramp.color_ramp.elements.new(0.66).color = (0, 0, 1, 1)
    ramp.color_ramp.elements[2].position = 1.0

    # Attribute
    attr = nodes.new(type="ShaderNodeAttribute")
    attr.location = (0, 0)
    attr.attribute_name = "thickness"

    # Fresnel node
    fresnel = nodes.new(type="ShaderNodeFresnel")
    fresnel.location = (200, -200)
    fresnel.inputs[0].default_value = 1.45  # IOR

    mix_shader = nodes.new(type="ShaderNodeMixShader")
    mix_shader.location = (400, -100)

    glossy = nodes.new(type="ShaderNodeBsdfGlossy")
    glossy.location = (400, -300)
    glossy.inputs[1].default_value = 0.05  #

    links.new(attr.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], diffuse.inputs["Color"])
    links.new(diffuse.outputs["BSDF"], mix_shader.inputs[2])
    links.new(glossy.outputs["BSDF"], mix_shader.inputs[1])
    links.new(fresnel.outputs["Fac"], mix_shader.inputs["Fac"])
    links.new(mix_shader.outputs["Shader"], output.inputs["Surface"])

    obj = bpy.context.active_object
    if obj is not None:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)


create_bubble_shader()
