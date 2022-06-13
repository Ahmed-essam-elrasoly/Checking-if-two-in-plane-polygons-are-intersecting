# Libraries 
import numpy as np
from itertools import repeat

#Task Function
def Check_Interfer (Shapes_Geo): #input is in the format [[(Ax1,Ay1), (Ax2,Ay2), (Ax3,Ay3), ...], [(Bx1,By1), (Bx2,By2), (Bx3,By3), ...]]
    global arm
    #function to check if a point is in a triangle    
    arm ={}
    def PInTri(point,tri_points): #entries are the point of interest and the triangle
        arm[point] = 0
        Dx , Dy = point #the point of interest
    
        A,B,C = tri_points #spreading the triangle
        Ax, Ay = A
        Bx, By = B
        Cx, Cy = C
        
        #barycentric coordinates solution
        M1 = np.array([ [Dx - Bx, Dy - By, 0],
                        [Ax - Bx, Ay - By, 0],
                        [1      , 1      , 1]
                      ])
    
        M2 = np.array([ [Dx - Ax, Dy - Ay, 0],
                        [Cx - Ax, Cy - Ay, 0],
                        [1      , 1      , 1]
                      ])
    
        M3 = np.array([ [Dx - Cx, Dy - Cy, 0],
                        [Bx - Cx, By - Cy, 0],
                        [1      , 1      , 1]
                      ])
    
        M1 = np.linalg.det(M1)
        M2 = np.linalg.det(M2)
        M3 = np.linalg.det(M3)
 
        if(M1 == 0 or M2 == 0 or M3 ==0): #the point is on the arms of the shape
            arm[point] = arm[point] + 1
            if arm[point] >1 and point != A and point != B and point != C: 
                return False
            else:
                return True
        elif((M1 > 0 and M2 > 0 and M3 > 0)or(M1 < 0 and M2 < 0 and M3 < 0)):
                #if products is non 0 check if all of their sign is same, if true the point is inside the triangle
                return True
        else:
                return False
    #function to split shapes into split of triangles
    def SplitToTris(shape):
        Tris = []
        for vortex in range(1,len(shape)-2):
            Tris.append([shape[0], shape[vortex], shape[vortex+1]])
        Tris.append([shape[0], shape[1], shape[-1]])
        return Tris
    #importing each shape
    Shape_1 = Shapes_Geo[0]
    Shape_2 = Shapes_Geo[1]
    #checking if shapes are valid
    if len(Shape_1) < 3 or len(Shape_2)<3 :
        print('False geometry')
        return None
    #spliting each shape to triangles 
    Shape_1_Tris = SplitToTris(Shape_1)
    Shape_2_Tris = SplitToTris(Shape_2)
    #preparing results
    Shape_1_Vorts_in_Shape_2 = []
    Shape_2_Vorts_in_Shape_1 = []
    #checking if shape 1 vortices are in shape 2
    for tri2 in Shape_2_Tris:
        if True in list(map(PInTri,Shape_1, repeat(tri2))):
            Shape_1_Vorts_in_Shape_2 = True
            break
        else:
            Shape_1_Vorts_in_Shape_2 = False
    #checking if shape 2 vortices are in shape 1
    for tri1 in Shape_1_Tris:
        if True in list(map(PInTri,Shape_2, repeat(tri1))):
            Shape_2_Vorts_in_Shape_1 = True
            break
        else:
            Shape_2_Vorts_in_Shape_1 = False
    #summing results up
    if  Shape_1_Vorts_in_Shape_2 or Shape_2_Vorts_in_Shape_1:
        return True
    else:
        return False
