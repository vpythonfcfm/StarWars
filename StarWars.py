from vpython import *
from math import *
from random import *
import numpy as np
from funcion import objeto 
from stl import mesh 

sun=sphere(color=vector(0.5,0.5,0.5), radius= 25)

class nave():
    def __init__(self,color,Vo,M,sun=False):
        self.Vo=Vo
        self.M=M
        self.obj=objeto(mesh.Mesh.from_file('xwing.stl'),color=color)





def rotar_2d(vector_2d, phi):
    mat_rot =np.array([[np.cos(phi), -np.sin(phi)],[np.sin(phi), np.cos(phi)]])
    vec_rotado = np.matmul(mat_rot, vector_2d)
    return vec_rotado

## Vectores unitarios ##
x_i = arrow(pos=vector(0,0,0), axis=vector(1,0,0), color=color.red, shaftwidth=0.05)
txt_x = text(text='x', pos=x_i.pos+x_i.axis, axis=x_i.axis, align='center', height=0.4,
          color=color.red, billboard=True, emissive=True)

y_j = arrow(pos=vector(0,0,0), axis=vector(0,1,0), color=color.blue, shaftwidth=0.05)
txt_y = text(text='y', pos=y_j.pos+y_j.axis, axis=y_j.axis, align='center', height=0.4,
          color=color.blue, billboard=True, emissive=True)

z_k = arrow(pos=vector(0,0,0), axis=vector(0,0,1), color=color.green, shaftwidth=0.05)
txt_z = text(text='z', pos=z_k.pos+z_k.axis, axis=z_k.axis, align='center', height=0.4,
          color=color.green, billboard=True, emissive=True)


def np_to_vec(np_array):
    vec=vector(np_array[0],np_array[1],np_array[2])
    return vec

##--------------------##


## Datos estrella ##

d = 100 # densidad
Ms = 2e30 # masa sol
au = 1.49e11# unidad astronomica
R = 100
sol = nave(color.yellow,vector(0,0,0),Ms) # sol

##----------------##



## Fuerza Gravitacional ##

# función calculo de fuerza
def ag(nave_a,nave_b):
    G = 50e-2 #6.67392e-11 
    rab_vec = nave_b.obj.cdg - nave_a.obj.cdg
    rab = rab_vec.mag
    F= G*nave_a.M*rab_vec/rab**3

    return F

    #G = 6.67392e-11
    #rab = dis(ca,cb)
    #alfa = abs(asin((ca.pos.y-cb.pos.y)/dis(ca,cb)))
    #F = (G*ma*mb)/((rab)**2)
    #a = abs(F)/mb
    #ax = a*cos(alfa)*Sig(ca.pos.x,cb.pos.x)
    #ay = a*sin(alfa)*Sig(ca.pos.y,cb.pos.y)
    #ac=[ax,ay,a]    
    #return ac
##----------------------##


## datos naves ##

# 

# Luke
phi = 0.2 *  np.pi
Mc = 100 # masa cuerpo
pos_luke = rotar_2d(np.array([0, 2 * R]), phi)
pos_luke = vector(pos_luke[0], pos_luke[1], 0)

Luke=nave(color.red,0,Mc)
Luke.obj.set_pos(pos_luke)
Luke.obj.rotar_y(-np.pi/2,Luke.obj.cdg)
Luke.obj.rotar_z(-np.pi/3,Luke.obj.cdg) # Ajuste para que quede tangencial

a = ag(Luke,sol).mag
dis= (Luke.obj.cdg - sol.obj.cdg).mag
v0 = sqrt(a*dis) # velocidad inicial
v0_luke = rotar_2d(np.array([v0, 0]), phi) * 0.965
v0 = vector(v0_luke[0], v0_luke[1], 0)
Luke.Vo=v0


# Vader
phi = 1 *  np.pi
Mc = 100 # masa cuerpo
pos_vader = rotar_2d(np.array([0, 2 * R]), phi)
pos_vader = vector(pos_vader[0], pos_vader[1], 0)


Vader=nave(color.green,0,Mc)
Vader.obj.set_pos(pos_vader)
Vader.obj.rotar_y(-np.pi/2,Vader.obj.cdg)
Vader.obj.rotar_z(np.pi/2,Vader.obj.cdg) # Ajuste para que quede tangencial


a = ag(Vader,sol).mag
dis= (Vader.obj.cdg - sol.obj.cdg).mag
v0 = sqrt(a*dis) # velocidad inicial
v0_vader = rotar_2d(np.array([v0, 0]), phi) * 0.965
v0 = vector(v0_vader[0], v0_vader[1], 0)
Vader.Vo=v0


##----------------##


## inicio de movimiento ##
año = 365 * 24 * 3600
t = 120
dt = 10



while True:

    rate(t)
    rLuke_prev = Luke.obj.cdg
    rVader_prev = Vader.obj.cdg 

        
    ## movimiento c
    #if abs(i[0].pos.x)-80>80 or abs(i[0].pos.y)>80:
    #   i[1].x = 0
    #    i[1].y = 0
    #    i[0].radius = 0
    Luke.obj.set_pos(Luke.obj.cdg+Luke.Vo*dt) 
    a = ag(Luke,sol)
    Luke.Vo= Luke.Vo + a*dt 
    dth_Luke = (Luke.obj.cdg - rLuke_prev).mag/(2*R)
    Luke.obj.rotar_z(-dth_Luke,Luke.obj.cdg)

    Vader.obj.set_pos(Vader.obj.cdg+Vader.Vo*dt) 
    a = ag(Vader,sol)
    Vader.Vo= Vader.Vo + a*dt
    dth_Vader = (Vader.obj.cdg - rVader_prev).mag/(2*R)
    Vader.obj.rotar_z(-dth_Vader,Vader.obj.cdg)
    #print (sqrt(a[2]*dis(i[0],sol)))
