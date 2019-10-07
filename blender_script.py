degree = 3

import bpy
import sys
sys.path.append('/home/lars/src/NURBS/')
from interface import *

control_poly = bpy.data.meshes['Control']
samples_poly = bpy.data.meshes['Samples']

num_control = len(control_poly.vertices)
num_samples = len(samples_poly.vertices)

sc = SimpleCircle()
sc.degree(degree)

control = sc.control(num_control)
i = 0
for v in control_poly.vertices:
    control[i*3 + 0] = v.co.x
    control[i*3 + 1] = v.co.y
    control[i*3 + 2] = v.co.z
    i += 1

samples = sc.samples()
i = 0
for v in samples_poly.vertices:
    v.co.x = samples[i*3 + 0]
    v.co.y = samples[i*3 + 1]
    v.co.z = samples[i*3 + 2]
    i += 1
