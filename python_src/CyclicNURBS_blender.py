import bpy

import CyclicNURBS_interface

def init_poly_curve(curveData):

    if ("Control" in bpy.data.objects):
        bpy.data.objects.remove(bpy.data.objects["Control"])
    if ("Samples" in bpy.data.objects):
        bpy.data.objects.remove(bpy.data.objects["Samples"])
    if ("Control" in bpy.data.meshes):
        bpy.data.meshes.remove(bpy.data.meshes["Control"])
    if ("Samples" in bpy.data.meshes):
        bpy.data.meshes.remove(bpy.data.meshes["Samples"])

    bpy.ops.mesh.primitive_circle_add(vertices=curveData.numControl, radius=1, enter_editmode=False)
    bpy.context.object.name = "Control"
    bpy.context.object.data.name = "Control"
    bpy.ops.mesh.primitive_circle_add(vertices=curveData.numSamples, radius=1, enter_editmode=False)
    bpy.context.object.name = "Samples"
    bpy.context.object.data.name = "Samples"

def init_poly_surface(surfaceData):

    if ("Control" in bpy.data.objects):
        bpy.data.objects.remove(bpy.data.objects["Control"])
    if ("Samples" in bpy.data.objects):
        bpy.data.objects.remove(bpy.data.objects["Samples"])
    if ("Control" in bpy.data.meshes):
        bpy.data.meshes.remove(bpy.data.meshes["Control"])
    if ("Samples" in bpy.data.meshes):
        bpy.data.meshes.remove(bpy.data.meshes["Samples"])

    bpy.ops.mesh.primitive_torus_add(major_segments=surfaceData.u_numControl, minor_segments=surfaceData.v_numControl, major_radius=2, minor_radius=1, enter_editmode=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='ONLY_FACE')
    bpy.ops.object.editmode_toggle()
    bpy.context.object.name = "Control"
    bpy.context.object.data.name = "Control"

    bpy.ops.mesh.primitive_torus_add(major_segments=surfaceData.u_numSamples, minor_segments=surfaceData.v_numSamples, major_radius=2, minor_radius=1, enter_editmode=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='ONLY_FACE')
    bpy.ops.object.editmode_toggle()
    bpy.context.object.name = "Samples"
    bpy.context.object.data.name = "Samples"

def init_nurbs_curve(curveData):

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    return CyclicNURBS_interface.CyclicCurve(curveData)

def init_nurbs_surface(surfaceData):

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    return CyclicNURBS_interface.CyclicSurface(surfaceData)

def update_curve(curveData, cc_ptr):

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    controlPoly = bpy.data.meshes['Control']
    samplesPoly = bpy.data.meshes['Samples']

    control_ptr = cc_ptr.control()
    for i in range(0, curveData.numControl):
        v = controlPoly.vertices[i]
        control_ptr[i*3 + 0] = v.co.x
        control_ptr[i*3 + 1] = v.co.y
        control_ptr[i*3 + 2] = v.co.z

    samples_ptr = cc_ptr.samples()
    for i in range(0, curveData.numSamples):
        v = samplesPoly.vertices[i]
        v.co.x = samples_ptr[i*3 + 0]
        v.co.y = samples_ptr[i*3 + 1]
        v.co.z = samples_ptr[i*3 + 2]

    samplesPoly.update()

def update_surface(surfaceData, cs_ptr):

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    controlPoly = bpy.data.meshes['Control']
    samplesPoly = bpy.data.meshes['Samples']

    for j in range(0, surfaceData.u_numControl):
        control_ptr = cs_ptr.control(j)
        for i in range(0, surfaceData.v_numControl):
            v = controlPoly.vertices[i + j * surfaceData.v_numControl]
            control_ptr[i*3 + 0] = v.co.x
            control_ptr[i*3 + 1] = v.co.y
            control_ptr[i*3 + 2] = v.co.z

    samples_ptr = cs_ptr.samples()
    for j in range(0, surfaceData.u_numControl):
        for i in range(0, surfaceData.v_numControl):
            v = controlPoly.vertices[i + j * surfaceData.v_numControl]
            v.co.x = samples_ptr[(i + j * surfaceData.v_numControl)*3 + 0]
            v.co.y = samples_ptr[(i + j * surfaceData.v_numControl)*3 + 1]
            v.co.z = samples_ptr[(i + j * surfaceData.v_numControl)*3 + 2]

    samplesPoly.update()