#######################
# icanim3d.py
# Emerson Yu
# Final Project
# This is the 3D portion of the IC animation, visualizing the manufacturing process.
#######################

from math import pi
import vpython as vp
from numpy import arange #vpython comes with numpy
from mazegen import Maze

def mazeTo3D(maze=None,z=1,vis=False):
    '''Turns maze into two lists of boxes (default invisible).'''
    if maze is None:
        maze = Maze()
    etch = []
    complement = []
    for r,row in enumerate(maze.maze):
        for c,cell in enumerate(row):
            if cell == 1:
                etch.append(vp.box(pos=vp.vector(c,5,r),length=1,height=z,width=1,visible=vis))
            else:
                complement.append(vp.box(pos=vp.vector(c,5,r),length=1,height=z,width=1,visible=vis))
    return etch,complement

def changeHeight(boxes, newHeight, mode=1):
    '''Makes box(es) gradually change height to newHeight, with their bottom surface(s) appearing static.
    Mode = 0 means no waiting.'''
    if isinstance(boxes,vp.box):
        upsideDown = False
        if boxes.up == vp.vector(0,-1,0):
            upsideDown = True
        change = (newHeight - boxes.height)/50
        for i in arange(50):
            if mode == 1:
                wait()
            boxes.height += change
            if upsideDown:
                boxes.pos.y -= change/2
            else:
                boxes.pos.y += change/2
        if newHeight == 0:
            boxes.visible = False
    elif isinstance(boxes,list):
        upsideDown = False
        if boxes[0].up == vp.vector(0,-1,0):
            upsideDown = True
        change = (newHeight - boxes[0].height)/50
        for i in arange(50):
            if mode == 1:
                wait()
            for box in boxes:
                box.height += change
                if upsideDown:
                    box.pos.y -= change/2
                else:
                    box.pos.y += change/2
        if newHeight == 0:
            for box in boxes:
                box.visible = False

def mazeVisible(boxes):
    '''Switches visibility of a 3D maze.'''
    for box in boxes:
        box.visible = False if box.visible else True

def bake(cv, color):
    '''Changes canvas's background color from white to color (vector) and then back to white.'''
    deltaR = (1-color.x)/50
    deltaG = (1-color.y)/50
    deltaB = (1-color.z)/50
    for i in arange(50):
        wait()
        cv.background=vp.vector(1-deltaR*i,1-deltaG*i,1-deltaB*i)
    for i in arange(50):
        wait()
        cv.background = vp.vector(color.x+deltaR*i,color.y+deltaG*i,color.z+deltaB*i)
    cv.background = vp.color.white


def wait(fps=40):
    try:
        vp.rate(fps)
    except KeyboardInterrupt:
        exit()

def newLabel(string,col=0):
    '''Creates a new second-line label. col = 0 or 1 (black or white)'''
    if col == 0:
        return vp.label(text=string,pixel_pos=True, pos=vp.vector(10,930,0),height=25,box=False,align='left',color=vp.color.black)
    elif col == 1:
        return vp.label(text=string,pixel_pos=True, pos=vp.vector(10,930,0),height=25,box=False,align='left',color=vp.color.white)
    else:
        raise ValueError('col must be 0 or 1.')

def pixelatedCylinder(height, radius, perRadius, color):
    '''Creates a "cylinder" made up of a list of invisible boxes at the origin and perRadius boxes fitting in a radius.'''
    quarter = [[0]*perRadius for i in arange(perRadius)]
    for i in arange(perRadius):
        for j in arange(perRadius):
            if j**2>perRadius**2-i**2:
                continue
            quarter[i][j] = 1
    boxes = []
    side = radius/perRadius
    for x,row in enumerate(quarter):
        for z,val in enumerate(row):
            if val == 1:
                # weird float stuff
                boxes.append(vp.box(pos=vp.vector(x/radius+side*x/1.4,0,z/radius+side*z/1.4),length=side,height=height,width=side,color=color,visible=False))
    second = []
    for box in boxes:
        second.append(box.clone(visible=False))
    for box in second:
        box.rotate(angle=pi/2,axis=vp.vector(0,1,0),origin=vp.vector(0,0,0))
    third = []
    for box in second:
        third.append(box.clone(visible=False))
    for box in third:
        box.rotate(angle=pi/2,axis=vp.vector(0,1,0),origin=vp.vector(0,0,0))
    fourth = []
    for box in third:
        fourth.append(box.clone(visible=False))
    for box in fourth:
        box.rotate(angle=pi/2,axis=vp.vector(0,1,0),origin=vp.vector(0,0,0))
    boxes.extend(second)
    boxes.extend(third)
    boxes.extend(fourth)
    return boxes

def main():
    '''Driver program for 3D animation about IC manufacturing.'''
    print('Setting up...please wait...')
    cv = vp.canvas(title='IC Manufacturing',width=1000,height=1000,background=vp.color.white,autoscale=True,userzoom=False,userspin=False,userpan=False)
    cv.autoscale = False
    cv.camera.pos = vp.vector(5,8,5)
    cv.camera.rotate(angle=pi/4)
    cv.camera.rotate(angle=0.3,axis=vp.vector(-1,0,1))
    # vp.arrow(pos=vp.vector(0,0,0),axis=vp.vector(5,0,0),color=vp.vector(1,0,0),length=15) # for reference
    # vp.arrow(pos=vp.vector(0,0,0),axis=vp.vector(0,5,0),color=vp.vector(0,1,0),length=15)
    # vp.arrow(pos=vp.vector(0,0,0),axis=vp.vector(0,0,5),color=vp.vector(0,0,1),length=15)
    wafer = vp.cylinder(axis=vp.vector(0,0.1,0),radius=7,color=vp.vector(0.3,0.9,1))
    chips = pixelatedCylinder(0.3,7,10,wafer.color) # this takes a while (preload)
    wafer.color = vp.color.white
    input('Hit enter to start.')
    disclaimer = vp.label(text='Note: Not to scale. Real materials/steps may vary.',pixel_pos=True, pos=vp.vector(10,980,0),height=25,box=False,align='left',color=vp.color.black)
    label = vp.label(text='Silicon dioxide masking film grown on silicon substrate wafer.',pixel_pos=True, pos=vp.vector(10,930,0),height=25,box=False,align='left')
    for i in arange(100):
        wait()
        wafer.axis = vp.vector(0,0.1+.002*i,0)
    wafer.axis = vp.vector(0,0.3,0)
    label.visible = False
    label = newLabel('Clean/Bake (very high temp).')
    bake(cv,vp.vector(1,0.6,0))
    label.visible = False
    label = newLabel('Vaporized hexamethyldisilazane (HMDS) added to promote adhesion of photoresist.')
    bake(cv,vp.vector(0.8,0.8,0.8))
    label.visible = False
    label = newLabel('Photoresist applied via spin coating (wafer rotates).')
    pointer = vp.arrow(pos=vp.vector(8,0.5,0),axis=vp.vector(0,0,-5),color=vp.color.red)
    pour = vp.cylinder(pos=vp.vector(0,10,0),axis=vp.vector(0,10,0),radius=0.1,color=vp.color.purple)
    for i in arange(50):
        wait()
        pour.pos.y -= 0.2
        pointer.rotate(angle=0.5,axis=wafer.axis,origin=wafer.axis)
    photoresist = vp.cylinder(pos=vp.vector(0,0.3,0),axis=vp.vector(0,0.1,0),radius=0,color=vp.color.purple)
    for i in arange(50):
        wait()
        pour.axis = vp.vector(0,10-i/5,0)
        photoresist.radius += 7/50
        pointer.rotate(angle=0.5,axis=wafer.axis,origin=wafer.axis)
    pour.visible = pointer.visible = label.visible = False
    photoresist.radius = 7.2
    label = newLabel('Bake to evaporate excess solvent (low temp pre-exposure bake).')
    bake(cv,vp.vector(1,0.8,0.2))
    label.visible = False
    label = newLabel('Edge bead removal (get rid of photoresist on sides).')
    pointer.visible = True
    beadRemoval = vp.cylinder(pos=vp.vector(0,0,7),axis=vp.vector(0,10,0),radius=0.1,color=vp.color.gray(0.2))
    for i in arange(50):
        wait()
        pointer.rotate(angle=0.5,axis=wafer.axis,origin=wafer.axis)
        photoresist.radius -= 0.004
    photoresist.radius = 7
    pointer.visible = False
    for i in arange(50):
        wait()
        beadRemoval.axis = vp.vector(0,10-i*0.2,0)
    beadRemoval.visible = label.visible = False
    label = newLabel('This is the optical system used to expose patterns onto the photoresist, step by step.')
    optics = vp.cylinder(pos = vp.vector(0,10,0),axis=vp.vector(0,20,0),radius=8,color=vp.color.black)
    for i in arange(50):
        wait()
        optics.pos.y -= 0.1
    beam = vp.cylinder(pos=vp.vector(0,5,0),axis=vp.vector(0,-5,0),radius=0.1,color=vp.color.yellow,opacity=0.8)
    cv.camera.pos = vp.vector(5,5,5)
    for i in arange(4):
        vp.sleep(1)
        beam.visible = False
        wafer.pos.z += 0.2
        photoresist.pos.z += 0.2
        vp.sleep(1)
        beam.visible = True
    wafer.pos.z = photoresist.pos.z = 0
    cv.camera.pos = vp.vector(5,8,5)
    label.visible = False
    label = newLabel("Let's zoom in on the optics.")
    for i in arange(30):
        wait()
        cv.camera.rotate(angle=pi/60,axis=vp.vector(-1,0,-1))
        cv.camera.rotate(angle=-0.01,axis=vp.vector(-1,0,1))
        cv.camera.pos = vp.vector(5-i/5,8+i/5,5-i/5)
    optics.visible = photoresist.visible = wafer.visible = beam.visible = False
    for i in arange(30): # resetting camera using loops (undoing float imprecision with itself)
        cv.camera.rotate(angle=-pi/60,axis=vp.vector(-1,0,-1))
        cv.camera.rotate(angle=0.01,axis=vp.vector(-1,0,1))
    cv.background = vp.color.gray(0.2)
    cv.camera.pos = vp.vector(10,8.5,6.5) # new camera pos
    cv.camera.rotate(angle=-0.3,axis=vp.vector(-1,0,1))
    cv.camera.rotate(angle=0.5,axis=vp.vector(0,1,0),origin=vp.vector(0,10,0))
    mask,maskLight = mazeTo3D(z=0.1)
    for box in mask:
        box.rotate(angle=pi/2,axis=vp.vector(1,0,0),origin=vp.vector(4,0,0))
        box.pos.y += 8
        box.color = vp.color.black
    glass = vp.box(pos=vp.vector(3.5,4.5,5.1),axis=vp.vector(1,0,0),length=8,width=0.1,height=8,opacity=0.3)
    label.visible = disclaimer.visible = False
    label = newLabel('Diffraction occurs at the mask and pupil plane.\nEvery lens is a possible source of aberrations.',1)
    disclaimer = vp.label(text='Note: Realistically, the mask and chip would contain billions of these patterns.',pixel_pos=True, pos=vp.vector(10,980,0),height=25,box=False,align='left',color=vp.color.white)
    mazeVisible(mask)
    label2 = vp.label(text='Mask (chromium blocks light)',pos=vp.vector(glass.pos.x,glass.pos.y+6,glass.pos.z),height=25,box=False,color=vp.color.white,opacity=0)
    source = vp.sphere(color=vp.color.yellow,pos=vp.vector(3.5,4.5,15))
    label3 = vp.label(text='UV light source',pos=vp.vector(source.pos.x,source.pos.y+3,source.pos.z),height=25,box=False,color=vp.color.white,opacity=0)
    condenser = vp.cylinder(pos=vp.vector(3.5,4.5,10),axis=vp.vector(0,0,0.1),opacity=0.3,radius=4)
    label4 = vp.label(text='Condenser',pos=vp.vector(condenser.pos.x,condenser.pos.y-5,condenser.pos.z),height=25,box=False,color=vp.color.white,opacity=0)
    project1 = vp.cylinder(pos=vp.vector(3.5,4.5,0),axis=vp.vector(0,0,0.1),opacity=0.3,radius=4)
    label5 = vp.label(text='Projection lens',pos=vp.vector(project1.pos.x,project1.pos.y-6,project1.pos.z),height=25,box=False,color=vp.color.white,opacity=0)
    pupil = vp.cylinder(pos=vp.vector(3.5,4.5,-2),axis=vp.vector(0,0,0.1),radius=3,color=vp.color.black)
    label6 = vp.label(text="Pupil plane's diameter = numerical aperture",pos=vp.vector(pupil.pos.x,pupil.pos.y-5,pupil.pos.z-5),height=25,box=False,color=vp.color.white,opacity=0)
    project2 = vp.cylinder(pos=vp.vector(3.5,4.5,-4),axis=vp.vector(0,0,0.1),opacity=0.3,radius=4)
    label7 = vp.label(text='Projection lens',pos=vp.vector(project2.pos.x,project2.pos.y-6,project2.pos.z-4),height=25,box=False,color=vp.color.white,opacity=0)
    field = vp.box(pos=vp.vector(3.5,4.5,-10),axis=vp.vector(1,0,0),length=2,width=0.1,height=2,color=vp.color.purple)
    label8 = vp.label(text="Field on wafer (4:1 reduction of mask)",pos=vp.vector(field.pos.x,field.pos.y+3,field.pos.z),height=25,box=False,color=vp.color.white,opacity=0)
    light = vp.cylinder(pos=source.pos,axis=vp.vector(0,0,0.1),opacity=0.6,color=vp.color.yellow,radius=1,make_trail=True,trail_radius=1)
    for i in arange(50):
        wait()
        light.pos.z -= 0.1
        light.radius += 0.01
        light.trail_radius += 0.01
    for i in arange(50):
        wait()
        light.pos.z -= 0.1
    for i in arange(50):
        wait()
        light.pos.z -= 0.1
        light.radius += 0.02
        light.trail_radius += 0.02
    for i in arange(20):
        wait()
        light.pos.z -= 0.1
        light.radius -= 0.1
        light.trail_radius -= 0.1
    for i in arange(20):
        wait()
        light.pos.z -= 0.1
        light.radius += 0.1
        light.trail_radius += 0.1
    for i in arange(60):
        wait()
        light.pos.z -= 0.1
        light.radius -= 0.025
        light.trail_radius -= 0.025
    label.visible = False
    label = newLabel('Based on the Rayleigh criterion, in order to get small feature sizes,\nwe want to minimize wavelength and the k1 coefficient (theoretical minimum 0.25),\nand maximize numerical aperture.',1)
    vp.sleep(5)
    label.visible = False
    label = newLabel('Current commercial lithography uses DUV light of wavelengths down to 193 nm.\nThis alone can achieve feature sizes of 40 nm, but auxiliary techniques can be applied.',1)
    vp.sleep(3)
    label.visible = False
    label = newLabel('These techniques include:',1)
    vp.sleep(0.5)
    label.visible = False
    label = newLabel('These techniques include:\n- Multiple patterning',1)
    vp.sleep(0.5)
    label.visible = False
    label = newLabel('These techniques include:\n- Multiple patterning\n- Immersion lithography',1)
    vp.sleep(0.5)
    label.visible = False
    label = newLabel('These techniques include:\n- Multiple patterning\n- Immersion lithography\n- Computational lithography (e.g. phase-shift masks, OPC, SMO, etc.)',1)
    vp.sleep(0.5)
    label.visible = False
    label = newLabel('These techniques include:\n- Multiple patterning\n- Immersion lithography\n- Computational lithography (e.g. phase-shift masks, OPC, SMO, etc.)\n- Atomic layer deposition',1)
    vp.sleep(0.5)
    label.visible = False
    label = newLabel('These techniques include:\n- Multiple patterning\n- Immersion lithography\n- Computational lithography (e.g. phase-shift masks, OPC, SMO, etc.)\n- Atomic layer deposition\n- etc. (several in the works)',1)
    vp.sleep(3)
    label.visible = label2.visible = label3.visible = label4.visible = label5.visible = label6.visible = label7.visible = label8.visible = False
    label = newLabel("Let's zoom in on the prospective chip.",1)
    light.clear_trail()
    light.visible = False
    cv.camera.rotate(angle=-pi/2+0.28,axis=vp.vector(0,1,0),origin=vp.vector(0,cv.camera.pos.y,0))
    cv.camera.pos = vp.vector(3.5,4.5,10)
    vp.sleep(0.5)
    for i in arange(1,21):
        wait()
        cv.camera.pos = vp.vector(3.5,4.5,10-i*1.65)
    cv.camera.pos = vp.vector(3.5,4.5,-23)
    vp.sleep(1)
    disclaimer.color = vp.color.black
    label.color = vp.color.black
    mazeVisible(mask) # hide
    glass.visible = source.visible = condenser.visible = project1.visible = pupil.visible = project2.visible = field.visible = False
    cv.camera.rotate(angle=pi/2-0.28,axis=vp.vector(0,1,0),origin=vp.vector(0,cv.camera.pos.y,0)) # reset
    cv.camera.rotate(angle=-0.5,axis=vp.vector(0,1,0),origin=vp.vector(0,10,0))
    cv.camera.rotate(angle=0.3,axis=vp.vector(-1,0,1))
    cv.camera.pos = vp.vector(5,8,5)
    cv.background = vp.color.white
    wafer.visible = label.visible = optics.visible = photoresist.visible = False
    etch,complement = mazeTo3D(vis=True)
    unexposed,exposed = mazeTo3D()
    for box in unexposed:
        box.pos.y = 6
        box.color = vp.color.purple
    for box in exposed:
        box.pos.y = 6
        box.color = vp.color.purple
    changeHeight(unexposed,0.1,0)
    changeHeight(exposed,0.1,0)
    mazeVisible(unexposed)
    mazeVisible(exposed)
    label = newLabel('Before exposure, a camera checks the topological alignment of preset marks.')
    align = []
    for i in arange(0,8,7):
        for j in arange(0,8,7):
            align.append(vp.box(pos=vp.vector(i,5.5,j),length=0.3,height=0,width=0.3,color=vp.color.green,opacity=0.5))
    changeHeight(align,0.2)
    vp.sleep(1)
    changeHeight(align,0)
    label.visible = False
    label = newLabel('Now, the photoresist can be exposed.')
    for box in maskLight:
        box.up = vp.vector(0,-1,0)
        box.pos.y = 25.5
        box.opacity = 0.3
        box.color = vp.color.yellow
    mazeVisible(maskLight)
    changeHeight(maskLight,20)
    for box in maskLight:
        box.up = vp.vector(0,1,0)
    changeHeight(maskLight,0)
    label.visible = False
    label = newLabel('Post-exposure bake to mitigate standing wave effect.')
    bake(cv,vp.vector(1,0.7,0.1))
    label.visible = False
    label = newLabel('Wash away exposed positive photoresist with developer.')
    develop = vp.box(pos=vp.vector(7.5,5.7,3.5),axis=vp.vector(0,0,1),up=vp.vector(1,0,0),length=8,width=0.2,height=0,opacity=0.5,color=vp.vector(0.5,0.5,0))
    for i in arange(50):
        wait()
        develop.height += 0.16
        develop.pos.x -= 0.08
    changeHeight(exposed,0)
    develop.up = vp.vector(-1,0,0)
    for i in arange(50):
        wait()
        develop.height -= 0.16
        develop.pos.x -= 0.08
    develop.visible = False
    label.visible = False
    label = newLabel('Etch the uncovered silicon dioxide with plasma.')
    for i in arange(50):
        wait()
        cv.background = vp.vector(1,1-0.006*i,1)
    changeHeight(complement,0.5)
    for i in arange(50):
        wait()
        cv.background = vp.vector(1,0.7+0.006*i,1)
    cv.background = vp.color.white
    label.visible = False
    label = newLabel('Strip the leftover photoresist via plasma ashing.')
    for i in arange(50):
        wait()
        cv.background = vp.vector(1,1-0.006*i,1)
    changeHeight(unexposed,0)
    for i in arange(50):
        wait()
        cv.background = vp.vector(1,0.7+0.006*i,1)
    cv.background = vp.color.white
    label.visible = False
    label = newLabel('Now comes FEOL (front-end-of-line).\nDepending on the layer (e.g. transistors), etch/dope/strip accordingly.\n(Detailed steps not shown here)')
    vp.sleep(3)
    label.visible = False
    label = newLabel('After FEOL comes BEOL (back-end-of-line).\nDepending on the layer, coat with barrier/dielectric/spacer.')
    for box in exposed:
        box.color = vp.color.yellow
        box.pos.y = 5
    for box in unexposed:
        box.color = vp.color.yellow
    combined = exposed + unexposed
    mazeVisible(combined)
    changeHeight(combined,0.1)
    vp.sleep(2)
    label.visible = False
    label = newLabel('(BEOL) Fill with interconnect layer and apply chemical mechanical polishing.')
    fill = []
    for box in complement:
        fill.append(box.clone(pos=vp.vector(box.pos.x,box.pos.y+0.35,box.pos.z),color=vp.vector(0.5,0.1,0),height=0))
    cover = vp.box(pos=vp.vector(3.5,5.6,3.5),color=vp.vector(0.5,0.1,0),height=0,length=8,width=8,visible=False)
    changeHeight(fill,0.5)
    cover.visible = True
    changeHeight(cover,0.2)
    changeHeight(cover,0)
    for i in arange(50):
        wait()
        changeHeight(fill,0.5-0.002*i,0)
        changeHeight(unexposed,0.1-0.002*i,0)
    changeHeight(fill,0.4,0)
    changeHeight(unexposed,0,0)
    vp.sleep(2)
    label.visible = False
    label = newLabel('(BEOL) Repeat the entire process 12-30x with different layers\nof different materials/functions (each with own masks), with vias in between.\nOverlay alignment is checked for every layer.')
    maze11,maze12 = mazeTo3D(Maze(key='1'),z=0.1,vis=True)
    maze21,maze22 = mazeTo3D(Maze(key='2'),z=0.1,vis=True)
    maze31,maze32 = mazeTo3D(Maze(key='3'),z=0.1,vis=True)
    maze41,maze42 = mazeTo3D(Maze(key='4'),z=0.1,vis=True)
    maze51,maze52 = mazeTo3D(Maze(key='5'),z=0.1,vis=True)
    vias = []
    for i in arange(1,8,2):
        for j in arange(1,8,2):
            vias.append(vp.cylinder(pos=vp.vector(i-0.5,5.5,j-0.5),radius=0.2,axis=vp.vector(0,0,0),color=vp.vector(0.5,0.1,0)))
    for box in maze11:
        box.pos.y = 5.5
        box.color = vp.vector(0.3,0.9,1)
    for box in maze12:
        box.pos.y = 5.5
        box.color = vp.vector(0.5,0.1,0)
    for box in maze21:
        box.pos.y = 5.5
        box.color = vp.vector(0.3,0.9,1)
    for box in maze22:
        box.pos.y = 5.5
        box.color = vp.vector(0.5,0.1,0)
    for box in maze31:
        box.pos.y = 5.5
        box.color = vp.vector(0.3,0.9,1)
    for box in maze32:
        box.pos.y = 5.5
        box.color = vp.vector(0.5,0.1,0)
    for box in maze41:
        box.pos.y = 5.5
        box.color = vp.vector(0.3,0.9,1)
    for box in maze42:
        box.pos.y = 5.5
        box.color = vp.vector(0.5,0.1,0)
    for box in maze51:
        box.pos.y = 5.5
        box.color = vp.vector(0.3,0.9,1)
    for box in maze52:
        box.pos.y = 5.5
        box.color = vp.vector(0.5,0.1,0)
    for i in arange(50):
        wait()
        for box in maze11:
            box.pos.y += 0.03
        for box in maze12:
            box.pos.y += 0.03
        for box in maze21:
            box.pos.y += 0.06
        for box in maze22:
            box.pos.y += 0.06
        for box in maze31:
            box.pos.y += 0.09
        for box in maze32:
            box.pos.y += 0.09
        for box in maze41:
            box.pos.y += 0.12
        for box in maze42:
            box.pos.y += 0.12
        for box in maze51:
            box.pos.y += 0.15
        for box in maze52:
            box.pos.y += 0.15
        for cyl in vias:
            cyl.axis = vp.vector(0,0.152*i,0)
    mazeVisible(align)
    changeHeight(align,7.7)
    for i in arange(50):
        wait()
        for box in align:
            box.opacity -= 0.01
    mazeVisible(align)
    vp.sleep(2)
    for i in arange(50):
        wait()
        for box in maze11:
            box.pos.y -= 0.03
        for box in maze12:
            box.pos.y -= 0.03
        for box in maze21:
            box.pos.y -= 0.058
        for box in maze22:
            box.pos.y -= 0.058
        for box in maze31:
            box.pos.y -= 0.086
        for box in maze32:
            box.pos.y -= 0.086
        for box in maze41:
            box.pos.y -= 0.114
        for box in maze42:
            box.pos.y -= 0.114
        for box in maze51:
            box.pos.y -= 0.142
        for box in maze52:
            box.pos.y -= 0.142
        for cyl in vias:
            cyl.axis = vp.vector(0,7.6-0.152*i,0)
    for cyl in vias:
        cyl.visible = False
    vp.sleep(2)
    for i in arange(50):
        wait()
        cv.camera.pos = vp.vector(5+i,8+i/2,5+i)
        cv.background = vp.vector(1-0.014*i,1-0.002*i,1)
    mazeVisible(maze11)
    mazeVisible(maze12)
    mazeVisible(maze21)
    mazeVisible(maze22)
    mazeVisible(maze31)
    mazeVisible(maze32)
    mazeVisible(maze41)
    mazeVisible(maze42)
    mazeVisible(maze51)
    mazeVisible(maze52)
    mazeVisible(exposed)
    mazeVisible(fill)
    mazeVisible(etch)
    mazeVisible(complement)
    cv.camera.pos = vp.vector(-3,-3,-3)
    wafer.color = vp.vector(0.3,0.9,1)
    wafer.visible = True
    disclaimer.visible = label.visible = False
    disclaimer = vp.label(text='Note: Not to scale. Real materials/steps may vary.',pixel_pos=True, pos=vp.vector(10,980,0),height=25,box=False,align='left',color=vp.color.black)
    label = newLabel('Finally, cut up the wafer into identical chips.\nChips may be delayered for failure analysis (not shown).\nOtherwise, they are packaged.')
    for i in arange(50):
        wait()
        cv.camera.pos = vp.vector(-3+i*0.16,-3+i*0.22,-3+i*0.16)
        cv.background = vp.vector(0.3+0.014*i,0.9+0.002*i,1)
    cv.background = vp.color.white
    cv.camera.pos = vp.vector(5,8,5)
    vp.sleep(2)
    mazeVisible(chips)
    wafer.visible = False
    for i in arange(50):
        wait()
        for box in chips:
            box.pos = vp.vector(box.pos.x*1.005,box.pos.y,box.pos.z*1.005)
    for i in arange(50):
        wait()
        for box in chips:
            box.color = vp.color.gray(1-i/200)
            box.length += 0.0005
            box.width += 0.0005
            box.height += 0.001
    vp.sleep(5)
    cv.delete()

if __name__ == '__main__':
    main()