degree = 3

import bpy
import sys
sys.path.append('/home/lars/src/NURBS/')
import interface

controlPoly = bpy.data.meshes['Control']
samplesPoly = bpy.data.meshes['Samples']

numControl = len(controlPoly.vertices)
numSamples = len(samplesPoly.vertices)

sc_ptr = interface.SimpleCircle(1,numControl,numSamples)

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
