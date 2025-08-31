from vpython import *
import time
import sympy as smp
import math
path = r"C:\Users\hardy\Desktop\課內資料\英物\8. Euler's Pendulum\拉格理論\完整磁場\2D - Numerical Solution.txt"
data = []

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            data.append(eval(line)) #t,x,y,z,the[n],phi[n], psi_d
f.close()

#Spawn Cylinder
l = data[0][1] #Length of Pendulum
r = data[0][0] #Radius of Pendulum
h = data[0][2] #Thickness of plate
w = l      #Width of plate
dt = 1/data[0][3] #Time Interval
h/=2 #Makes the plate looks thinner
data.remove(data[0])
scene = canvas(title="Euler's Pendulum", width=1100, height=600, x=0, y=0, background=color.white)


plate = box(pos=vec(0,h/4,0), size=vec(w*2,h/2,w*2), color=color.white)
'''
time.sleep(3)
the = radians(30)
for n in range(0,1080,1):
    phi = radians(n)
    distance = -r*smp.cos(the) + r + l/2*smp.sin(the)
    x = distance*smp.cos(phi)
    y = distance*smp.sin(phi)
    z = -r*smp.sin(the)-l/2*smp.cos(the)
    pendulum.pos=vec(x,z,y)
    pendulum.axis = vec(-l/2*math.sin(the)*math.cos(phi),l/2*math.cos(the), -l/2*math.sin(the)*math.sin(phi))
    time.sleep(0.01)    
'''
time.sleep(10)
pendulum = cylinder(pos=vec(data[0][1],data[0][3],data[0][2]),axis=vec(0,1,0), radius=r, length=l/2, texture = textures.metal, make_trail = True)
t = 0
for n in data:
    the = n[4]
    phi = n[5]
    psi_d = n[6]
    pendulum.pos=vec(n[1],n[3],n[2])
    pendulum.axis = vec(-l/2*math.sin(the)*math.cos(phi),l/2*math.cos(the), -l/2*math.sin(the)*math.sin(phi))
    pendulum.rotate(angle = psi_d*dt, axis = pendulum.axis, origin = pendulum.pos)
    scene.title = str(math.ceil(t*100)/100.0)
    t+=dt
    time.sleep(dt)

    