###############################################################
####DUAL-ARM CLOTH MANIPULATION PROTOCOL - PARTIAL DRESSING####
###############################################################
# Check the Dual-Arm Cloth Manipulation protocol P-DACM-D-0.1 #
# for how to measure the T-shirt length L_n and edit the      #
# variable "neck_length_shirt" below.                         #
# To execude the script run "freecadcmd generate_head_stls.py"#
###############################################################

import os
import FreeCAD
import Part, math, Mesh
from FreeCAD import Base
import argparse
import numpy as np


#change those variables to fit your case.

neck_lenght_shirt=396 #L_n of shirt in mm

save_path=os.getcwd()+"/"
head_types=["small", "big"]




def parttomesh( part ):
    faces = []
    shape = part
    triangles = shape.tessellate(1) # the number represents the precision of the tessellation)
    for tri in triangles[1]:
        face = []
        for i in range(3):
            vindex = tri[i]
            face.append(triangles[0][vindex])
        faces.append(face)
    m = Mesh.Mesh(faces)   
    return m;

#defined T-shirt factors
neck_lenght_shirt_factor_big=1.11 
neck_lenght_shirt_factor_small=0.72 

for head_type in head_types:
    neck_lenght_shirt_factor=0.
    if head_type=="big":
        neck_lenght_shirt_factor=neck_lenght_shirt_factor_big
    elif head_type=="small":
        neck_lenght_shirt_factor=neck_lenght_shirt_factor_small
    else:
        print("No valid head type specified. ('small' or 'big') ")
        assert True
    
    #top sphere
    rs=((neck_lenght_shirt*neck_lenght_shirt_factor)/np.pi)/2
    print(rs*2)
    print("--")
    sphere = Part.makeSphere(rs)
    sphere.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0), App.Vector(0,0,0))
    #middle cylinder
    ch=15
    cylinder = Part.makeCylinder(rs,ch)
    cylinder.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0), App.Vector(0,0,0))
    sc_fuse = sphere.fuse(cylinder)
    #bottom sphere
    sphere = Part.makeSphere(rs)
    sphere.Placement=App.Placement(App.Vector(0,0,ch), App.Rotation(0,0,0), App.Vector(0,0,0))
    scs_fuse = sc_fuse.fuse(sphere)
    #make cylinder for cut
    cylinder = Part.makeCylinder(rs+20,200)
    cylinder.Placement=App.Placement(App.Vector(0,0,ch+45), App.Rotation(0,0,0), App.Vector(0,0,0))
    head_sphere = scs_fuse.cut(cylinder)
    #cone for standing
    cone = Part.makeCone(5,rs/2,rs+30)
    cone.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(0,0,0), App.Vector(0,0,0)) 
    #converte to mesh and save    
    m=parttomesh(cone)
    m.write(save_path + head_type + "_head_bottom.stl")
    #make top
    diff_top = head_sphere.cut(cone)    
    m = parttomesh(diff_top)
    m.write(save_path + head_type + "_head_top.stl")
    #full head
    fullhead = head_sphere.fuse(cone)
    diff_top = head_sphere.cut(cone)   
    m = parttomesh(fullhead)
    m.write(save_path + head_type + "_head_full.stl")
