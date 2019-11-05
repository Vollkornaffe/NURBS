import bpy

import CyclicNURBS_interface

def init_poly(numControl = 4, numSamples = 1000):

    if ("Control" in bpy.data.objects):
        bpy.data.objects.remove(bpy.data.objects["Control"])
    if ("Samples" in bpy.data.objects):
        bpy.data.objects.remove(bpy.data.objects["Samples"])
    if ("Control" in bpy.data.meshes):
        bpy.data.meshes.remove(bpy.data.meshes["Control"])
    if ("Samples" in bpy.data.meshes):
        bpy.data.meshes.remove(bpy.data.meshes["Samples"])

    bpy.ops.mesh.primitive_circle_add(vertices=numControl, radius=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.object.name = "Control"
    bpy.context.object.data.name = "Control"
    bpy.ops.mesh.primitive_circle_add(vertices=numSamples, radius=1, enter_editmode=False, location=(0, 0, 0))
    bpy.context.object.name = "Samples"
    bpy.context.object.data.name = "Samples"

def init_nurbs(degree = 3):

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    numControl = len(bpy.data.meshes['Control'].vertices)
    numSamples = len(bpy.data.meshes['Samples'].vertices)

    return CyclicNURBS_interface.CircularCurve(degree, numControl, numSamples)

def update(sc_ptr):

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    controlPoly = bpy.data.meshes['Control']
    samplesPoly = bpy.data.meshes['Samples']

    numControl = len(controlPoly.vertices)
    numSamples = len(samplesPoly.vertices)

    control_ptr = sc_ptr.control()
    i = 0
    for v in controlPoly.vertices:
        control_ptr[i*3 + 0] = v.co.x
        control_ptr[i*3 + 1] = v.co.y
        control_ptr[i*3 + 2] = v.co.z
        i += 1

    samples_ptr = sc_ptr.samples()
    i = 0
    for v in samplesPoly.vertices:
        v.co.x = samples_ptr[i*3 + 0]
        v.co.y = samples_ptr[i*3 + 1]
        v.co.z = samples_ptr[i*3 + 2]
        i += 1

    samplesPoly.update()
