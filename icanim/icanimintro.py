#######################
# icanimintro.py
# Emerson Yu
# Final Project
# This is the first 2D portion of the IC animation, with introductory information regarding semiconductors and transistors.
#######################

import pygame as pg
from numpy import arange

class Animation:
    '''2D animation tools for pygame, including a dictionary for dirty rect animation.'''
    def __init__(self,width,height,fps,background,font_name='cambria',font_size=24):
        '''Also initializes clock and dirty_rect dictionary (which excludes the background).'''
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pg.display.set_mode((self.width,self.height))
        self.clock = pg.time.Clock()
        self.background = pg.image.load(background).convert()
        self.screen.blit(self.background,(0,0))
        pg.display.update()
        self.dirty_rects = {}
        self.font = pg.font.SysFont(font_name,font_size)

    def wait(self):
        '''Must be called every frame.'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                print('Exiting.')
                exit()
        self.clock.tick(self.fps)
        pg.display.update()
    
    def sleep(self,seconds):
        '''"Sleeps" by mass waiting. Can take floats.'''
        for i in arange(int(round(seconds*self.fps))):
            self.wait()

    def move(self,alias,x=None,y=None,mode=1):
        '''Gradually moves a surface in the dictionary by its top left corner.
        mode = 0 means instant (1 is default; 1 second). If x or y
        are left as None, no change along the respective axis will occur.'''
        rect = self.dirty_rects[alias][1]
        deltaX = 0 if x is None else x-rect.left
        deltaY = 0 if y is None else y-rect.top
        if mode == 0:
            rect.left += deltaX
            rect.top += deltaY
            self.refresh()
        elif mode == 1:
            left = rect.left
            top = rect.top
            for i in arange(1,self.fps+1):
                self.wait()
                rect.left = left+deltaX*(i/self.fps)
                rect.top = top+deltaY*(i/self.fps)
                self.refresh()
        elif isinstance(mode,int):
            raise ValueError('Mode must either be 0 or 1.')
        self.refresh()
        
    def erase(self,alias,mode=1):
        '''Gradually erases surface and removes it from the dictionary.
        mode = 0 means instant (1 is default; 1 second)'''
        if mode == 0:
            self.dirty_rects.pop(alias)
            self.refresh()
        elif mode == 1:
            self.fade(alias)
            self.dirty_rects.pop(alias)
            self.refresh()
        elif isinstance(mode,int):
            raise ValueError('Mode must either be 0 or 1')

    def add(self,img,alias=None,x=0,y=0,vis=True):
        '''Creates an item in the dictionary, with an initial position according to its center.
        img can either be a string file name or a Surface object. If img is a file name and no alias is given,
        default alias is the file name without extension. The purpose of aliases is to enable duplicates.
        vis = True (default) means alpha = 255, while vis = False means alpha = 0 (transparent)'''
        if isinstance(img,str):
            if alias is None:
                alias = img.split('.')[0]
            img = pg.image.load(img).convert_alpha() # Surface
        elif not isinstance(img,pg.Surface):
            raise TypeError('img must either be a file name or a Surface object.')
        if not isinstance(alias,str):
            raise TypeError('Alias must be None or str.')
        self.dirty_rects[alias] = img,img.get_rect() # dictionary with keys being str and values being tuples of Surface, Rect
        if not vis:
            self.dirty_rects[alias][0].set_alpha(0)
        self.move(alias,x,y,0)
        self.screen.blit(img,(self.dirty_rects[alias][1].left,self.dirty_rects[alias][1].top))
    
    def add_fade(self,img,alias=None,x=0,y=0):
        '''Adds img item while fading it in. Default alias is file name without extension.'''
        self.add(img,alias,x,y,vis=False)
        if isinstance(img,str) and alias is None:
            alias = img.split('.')[0]
        self.fade(alias)
    
    def img_of(self,key) -> pg.Surface:
        return self.dirty_rects[key][0]
    
    def rect_of(self,key) -> pg.Rect:
        return self.dirty_rects[key][1]
    
    def x_of(self,key) -> int:
        return self.dirty_rects[key][1].left
    
    def y_of(self,key) -> int:
        return self.dirty_rects[key][1].top
    
    def refresh(self):
        '''Redraws all objects.'''
        self.screen.blit(self.background,(0,0))
        for value in self.dirty_rects.values():
            self.screen.blit(value[0],(value[1].left,value[1].top))
    
    def clone(self,alias,new_alias=None,x=None,y=None,vis=True):
        '''Clones an item in the dictionary, defaultly creating a new alias with a numerical increment.
        x and y can optionally be used to set a new position. vis = True (default) means alpha = 255, 
        while vis = False means alpha = 0 (transparent)'''
        numberless = ''
        if new_alias is None:
            new_alias = ''
            for i in arange(len(alias)-1,-1,-1):
                try:
                    int(alias[i])
                except ValueError:
                    numberless = alias[i] + numberless
                else: # char is digit
                    new_alias = alias[i] + new_alias
            if new_alias == '':
                new_alias = numberless + '2'
            else:
                new_alias = numberless + str(int(new_alias)+1)
        elif alias == new_alias:
            raise ValueError("Clone's name must be different.")
        self.dirty_rects[new_alias] = self.dirty_rects[alias][0].copy(),self.dirty_rects[alias][1].copy()
        if not vis:
            self.dirty_rects[new_alias][0].set_alpha(0)
        self.move(new_alias,x,y,0)
    
    def fade(self,alias,mode=1):
        '''Either fades in or out an item, depending on its current overall alpha.
        mode = 0 means instant (1 is default; 1 second)'''
        if mode == 0:
            if self.dirty_rects[alias][0].get_alpha() == 0:
                self.dirty_rects[alias][0].set_alpha(255)
            else:
                self.dirty_rects[alias][0].set_alpha(0)
            self.refresh()
        elif mode == 1:
            if self.dirty_rects[alias][0].get_alpha() == 0:
                for i in arange(1,self.fps+1):
                    self.wait()
                    self.dirty_rects[alias][0].set_alpha(int(round(255*i/self.fps)))
                    self.refresh()
            else:
                for i in arange(1,self.fps+1):
                    self.wait()
                    self.dirty_rects[alias][0].set_alpha(int(round(255-255*(i/self.fps))))
                    self.refresh()
        elif isinstance(mode,int):
            raise ValueError('Mode must either be 0 or 1')
    
    def add_text(self,alias,string,x=0,y=0,vis=True,color=(0,0,0),font=None):
        '''Shortcut for adding text; spinoff of the add method.
        Default font color is black. Default font is self.font.'''
        if font is None:
            font = self.font
        self.add(font.render(string,True,color),alias,x,y,vis)
    
    def add_fade_text(self,alias,string,x=0,y=0,color=(0,0,0),font=None):
        '''Adds text item while fading it in. Default font color is black. Default font is self.font.'''
        if font is None:
            font = self.font
        self.add_text(alias,string,x,y,vis=False,color=color,font=font)
        self.fade(alias)
    
    def replace(self,alias,new_img,new_alias=None,mode=1,vis=True):
        '''Replaces item and its img. mode = 0 means instant, while mode = 1 means fade out and in (default).
        vis option only applies to mode = 0. New alias is optional (will otherwise reuse alias)'''
        if mode == 0:
            if new_alias is None:
                    self.add(new_img,alias,self.x_of(alias),self.y_of(alias),vis)
            elif isinstance(new_alias,str):
                self.add(new_img,new_alias,self.x_of(alias),self.y_of(alias),vis)
                self.dirty_rects.pop(alias)
        elif mode == 1:
            if self.img_of(alias).get_alpha != 0:
                self.fade(alias)
            if new_alias is None:
                self.add_fade(new_img,alias,self.x_of(alias),self.y_of(alias))
            elif isinstance(new_alias,str):
                self.add_fade(new_img,new_alias,self.x_of(alias),self.y_of(alias))
                self.dirty_rects.pop(alias)
        else:
            raise ValueError('Mode must either be 0 or 1')
    
    def replace_text(self,alias,new_string,new_alias=None,mode=1,color=(0,0,0),vis=True):
        '''Replaces text item and its img. mode = 0 means instant, while mode = 1 means fade out and in (default).
        Default color is black. Can only use default font.
        vis option only applies to mode = 0. New alias is optional (will otherwise reuse alias)'''
        if mode == 0:
            if new_alias is None:
                self.add_text(alias,new_string,self.x_of(alias),self.y_of(alias),vis,color=color)
            elif isinstance(new_alias,str):
                self.add_text(new_alias,new_string,self.x_of(alias),self.y_of(alias),vis,color=color)
                self.dirty_rects.pop(alias)
        elif mode == 1:
            if self.img_of(alias).get_alpha != 0:
                self.fade(alias)
            if new_alias is None:
                self.add_fade_text(alias,new_string,self.x_of(alias),self.y_of(alias),color=color)
            elif isinstance(new_alias,str):
                self.add_fade_text(new_alias,new_string,self.x_of(alias),self.y_of(alias),color=color)
                self.dirty_rects.pop(alias)
        else:
            raise ValueError('Mode must either be 0 or 1')

    def __str__(self):
        return str(self.dirty_rects)

def main():
    pg.init() # ignore pylint, this works fine
    a = Animation(1000,1000,40,'background.jpg') # make sure you are in the right working directory (cd icanim)
    input('Hit enter to start.')
    # a.add_text('cap1','',x=20) # for testing
    # a.add_text('cap2','',x=20,y=34) # for testing
    # a.add_text('cap3','',x=20,y=68) # for testing
    a.add_fade_text('title','Intro to IC',x=350,y=450,font=pg.font.SysFont('cambria',72))
    a.add_fade_text('by','by Emerson Yu',x=420,y=545)
    a.sleep(2)
    a.erase('by')
    a.erase('title')
    a.add_fade_text('cred','made with pygame and VPython',x=345,y=485)
    a.sleep(2)
    a.erase('cred')
    a.add_fade_text('section','1. Semiconductors',x=410,y=485)
    a.sleep(2)
    a.erase('section')
    a.add_fade_text('cap1',"These are silicon's orbitals according to its electron configuration.",x=20)
    a.add('orbitaltoband1.png',x=-252)
    a.move('orbitaltoband1',x=0)
    a.sleep(2)
    a.replace_text('cap1','In a solid containing many atoms, bunched orbitals form bands.')
    a.add('orbitaltoband2.png',x=1000)
    a.move('orbitaltoband2',x=252)
    a.sleep(2)
    a.replace_text('cap1','The distance between the highest-energy occupied band (valence band) and the')
    a.add_fade_text('cap2','lowest-energy unoccupied band (conduction band) is the band gap.',x=20,y=34)
    a.add_fade('orbitaltoband3.png',x=480)
    a.sleep(4)
    a.erase('orbitaltoband1',mode=0)
    a.erase('orbitaltoband2',mode=0)
    a.erase('orbitaltoband3',mode=0)
    a.fade('cap2')
    a.replace_text('cap1','The Fermi level is the total potential energy for a system of electrons at 0 K.')
    a.add_fade('fermi1.png')
    a.add_fade('fermi3.png',x=426)
    a.sleep(2)
    a.replace_text('cap1','The valence band is below this level, so its electrons are bound to the atom most of the time.')
    a.add_fade('fermi7.png',x=462,y=660)
    a.sleep(2)
    a.replace_text('cap1','The conduction band, however, is above this level, so electrons that jump into it can then')
    a.replace_text('cap2','be delocalized and carry current.',mode=0,vis=False)
    a.fade('cap2')
    for i in arange(1,21):
        a.sleep(0.05)
        a.move('fermi7',y=660+5*(-1)**i,mode=0)
    a.move('fermi7',y=300)
    a.sleep(0.5)
    a.move('fermi7',y=-100)
    a.erase('fermi7',0)
    a.fade('fermi3')
    a.fade('cap2')
    a.replace_text('cap1','Conductors have no band gap. Their electrons are completely delocalized.')
    a.add_fade('fermi2.png',x=130)
    a.add_fade('fermi7.png',x=166,y=480)
    for i in arange(1,3):
        a.move('fermi7',y=480+350*(-1)**i)
    a.erase('fermi7')
    a.replace_text('cap1','Insulators have a large band gap. Electrons from the valence band rarely get enough energy')
    a.replace_text('cap2','to jump to the conduction band.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('fermi4.png',x=722)
    a.sleep(2)
    a.fade('cap2')
    a.replace_text('cap1','Intrinsic semiconductors (e.g. silicon) have a small band gap, so they are less conductive')
    a.replace_text('cap2','than conductors but more conductive than insulators.',mode=0,vis=False)
    a.fade('cap2')
    a.fade('fermi3')
    a.sleep(2)
    a.fade('cap2')
    a.replace_text('cap1','However, they can be doped by adding impurities, becoming extrinsic semiconductors.')
    a.sleep(2)
    a.replace_text('cap1','Doped semiconductors can be p-type or n-type.')
    a.add_fade('fermi5.png',x=278)
    a.add_fade('fermi6.png',x=574)
    a.replace_text('cap1','In p-type (e.g. silicon + boron), the dopant atoms have one less electron per atom,')
    a.replace_text('cap2','with positive holes as charge carriers.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('fermi7.png',x=314,y=660)
    for i in arange(1,11):
        a.sleep(0.05)
        a.move('fermi7',y=660+5*(-1)**i,mode=0)
    a.move('fermi7',y=540)
    a.sleep(0.5)
    for i in arange(1,11):
        a.sleep(0.05)
        a.move('fermi7',y=540+5*(-1)**i,mode=0)
    a.move('fermi7',y=300)
    a.sleep(0.5)
    a.move('fermi7',y=-100)
    a.fade('fermi7')
    a.fade('cap2')
    a.replace_text('cap1','In n-type (e.g. silicon + phosphorus), the dopant atoms have one more electron per atom')
    a.replace_text('cap2','serving as a charge carrier.',mode=0,vis=False)
    a.fade('cap2')
    a.move('fermi7',610,400,0)
    a.fade('fermi7')
    for i in arange(1,11):
        a.sleep(0.05)
        a.move('fermi7',y=400+5*(-1)**i,mode=0)
    a.move('fermi7',y=-100)
    a.fade('fermi7')
    a.move('fermi7',y=660,mode=0)
    a.fade('fermi7')
    for i in arange(1,11):
        a.sleep(0.05)
        a.move('fermi7',y=660+5*(-1)**i,mode=0)
    a.move('fermi7',y=400)
    a.erase('fermi7')
    a.fade('cap2')
    a.replace_text('cap1','Either way, doping makes it easier for electrons to bridge the gap, improving conductivity.')
    a.sleep(2)
    for i in arange(1,7):
        a.erase('fermi'+str(i),0)
    a.replace_text('cap1','When a p-type and an n-type are placed next to each other, a p-n junction forms.')
    a.add_fade('pn1.png',x=57)
    a.add_fade('pn2.png',x=600)
    a.sleep(1)
    a.replace_text('cap1','Note that both semiconductors are initially entirely electrically neutral.')
    a.sleep(2)
    a.replace_text('cap1','However, putting them together changes that.')
    a.move('pn1',x=157)
    a.move('pn2',x=500)
    a.add_fade('pn3.png',x=101)
    a.sleep(3)
    a.replace_text('cap1',"Let's zoom in to see how this happens.")
    for i in arange(1,4):
        a.fade('pn'+str(i),0)
    a.add('pnclose1.png')
    a.add('pnclose2.png',x=285)
    a.add('pnclose3.png',x=685)
    a.replace_text('cap1',"The 'extra' (easily freed) electrons in the n-type are attracted to the positive holes.")
    a.replace_text('cap2','(potential electron spots) in the p-type, and vice versa. Thus, two-way diffusion occurs.',mode=0,vis=False)
    a.fade('cap2')
    a.move('pnclose3',485)
    a.move('pnclose2',485)
    a.sleep(5)
    a.fade('cap2')
    a.replace_text('cap1','The charge carriers cancel out each other in recombination.')
    a.replace_text('cap2',"Positive holes are filled, while the 'extra' electrons are no longer mobile.",mode=0,vis=False)
    a.fade('cap2')
    a.fade('pnclose2')
    a.move('pnclose3',685)
    a.add_fade('pnclose4.png',x=265)
    a.sleep(4)
    a.fade('cap2')
    a.replace_text('cap1','These charged areas near the junction are depleted of charge carriers, hence they form')
    a.replace_text('cap2','the depletion layer.',mode=0,vis=False)
    a.fade('cap2')
    a.sleep(3)
    for i in arange(1,5):
        a.erase('pnclose'+str(i),0)
    for i in arange(1,4):
        a.fade('pn'+str(i),0)
    a.fade('cap2')
    a.replace_text('cap1','The consequent electric field stops further diffusion.')
    a.sleep(2)
    a.replace_text('cap1',"Then, attaching a battery's positive terminal to the p-type and the negative terminal to")
    a.replace_text('cap2','the n-type would repel charge carriers toward the junction, reducing the depletion layer',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade_text('cap3','and allowing current to flow from the p-type to the n-type.',x=20,y=68)
    a.fade('pn3')
    a.add('pn4.png',x=-300,y=600)
    for i in arange(6):
        a.move('pn4',1200)
        a.move('pn4',-300,mode=0)
    a.fade('cap3')
    a.fade('cap2')
    a.replace_text('cap1','Thus, a p-n junction can serve as a diode (one-way conductor).')
    a.sleep(2)
    for i in arange(1,5):
        a.erase('pn'+str(i),0)
    a.replace_text('cap1','This behavior is crucial for transistors.')
    a.sleep(2)
    a.fade('cap1')
    a.add_fade_text('section','2. Transistors',x=415,y=485)
    a.sleep(2)
    a.erase('section')
    a.replace_text('cap1','Transistors can be used as binary switches or amplifiers.',mode=0,vis=False)
    a.fade('cap1')
    a.sleep(2)
    a.replace_text('cap1','A metal-oxide-semiconductor field-effect transistor (MOSFET) has 4 terminals:')
    a.replace_text('cap2','source, gate, drain, and body.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('transistor1.png')
    a.sleep(3)
    a.fade('cap2')
    a.replace_text('cap1','We will be using this n-type MOSFET (NMOS) as an example.')
    a.sleep(1.5)
    a.replace_text('cap1','Note that the source and drain wells are doped oppositely in respect to the body,')
    a.replace_text('cap2','forming a depletion region that blocks current from flowing between the drain and source.',mode=0,vis=False)
    a.fade('cap2')
    a.sleep(5)
    a.fade('cap2')
    a.replace_text('cap1','With application of high voltage, the gate acts as a capacitor and generates an electric field.')
    a.replace_text('cap2','This voltage has to be high enough for the electric field to attract enough electrons, though, ',mode=0,vis=False)
    a.fade('cap2')
    a.replace_text('cap3','otherwise the NMOS will stay in cutoff mode.',mode=0,vis=False)
    a.fade('cap3')
    a.add_fade('transistor4.png',x=170,y=300)
    a.sleep(6)
    a.fade('cap3')
    a.fade('cap2')
    a.replace_text('cap1',"Attracted by the electric field, electrons near the insulator delocalize.")
    a.replace_text('cap2','The accumulation of electrons counters the electric field, and a channel is created.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('transistor2.png',x=520)
    a.sleep(5)
    a.fade('cap2')
    a.replace_text('cap1',"This channel, of opposite type to the body, allows current to flow from the drain to the source.")
    a.replace_text('cap2','(high to low voltage) This is called linear operation mode.',mode=0,vis=False)
    a.fade('cap2')
    a.add('pn4.png',x=520,y=670,vis=False)
    a.replace('pn4',pg.transform.rotate(a.img_of('pn4'),180),mode=0,vis=False)
    a.fade('pn4')
    a.sleep(4)
    a.erase('pn4')
    a.fade('cap2')
    a.replace_text('cap1',"However, applying too high a voltage leads to saturation mode, where current cannot flow.")
    a.move('transistor2',x=330)
    a.sleep(3)
    a.erase('transistor2',0)
    a.erase('transistor4',0)
    a.erase('transistor1')
    a.add_fade('transistor3.png')
    a.replace_text('cap1',"Likewise, p-type MOSFETs (PMOS) function similarly, but with opposite signs.")
    a.replace_text('cap2','The voltage has to be low enough, but not too much so, in order for linear operation mode,',mode=0,vis=False)
    a.fade('cap2')
    a.replace_text('cap3','in which the electric field attracts positive holes.',mode=0,vis=False)
    a.fade('cap3')
    a.add_fade('transistor5.png',x=170,y=300)
    a.sleep(6)
    a.fade('cap3')
    a.fade('cap2')
    a.replace_text('cap1',"Current flows from source to drain in a PMOS (still high to low voltage, just other direction).")
    a.add_fade('pn4.png',x=520,y=670)
    a.sleep(2)
    a.erase('pn4')
    a.replace_text('cap1',"Note that these directions apply only to enhancement-mode MOSFETs (not depletion-modes).")
    a.sleep(2)
    a.replace_text('cap1',"Now let's see how we can use MOSFETs as switches in logic gates.")
    a.erase('transistor5',0)
    a.erase('transistor3')
    a.sleep(1)
    a.replace_text('cap1',"Complementary metal-oxide semiconductor (CMOSs) are often used to implement logic.")
    a.sleep(2)
    a.replace_text('cap1',"They are made up of PMOSs and NMOSs and follow these two rules:")
    a.replace_text('cap2','1. All PMOSs get input from a voltage supply or another PMOS',mode=0,vis=False)
    a.fade('cap2')
    a.replace_text('cap3',"2. All NMOSs get input from 'ground' (set as 0 V for the system) or another NMOS",mode=0,vis=False)
    a.fade('cap3')
    a.sleep(5)
    a.fade('cap3')
    a.fade('cap2')
    a.replace_text('cap1',"With that in mind, let's look at a CMOS inverter (NOT gate).")
    a.add_fade('cmos1.png')
    a.sleep(4)
    a.replace_text('cap1',"Let 0 = low voltage and 1 = high voltage.")
    a.sleep(2)
    font = pg.font.SysFont('cambria',48)
    a.add_fade_text('in1','1',x=30,y=855,font=font)
    a.replace_text('cap1',"When the input is 1, at the PMOS, VGS = Vin - Vdd does not reach its negative threshold,")
    a.replace_text('cap2','so the PMOS stays in cutoff mode and does not contribute to the output.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('cmos2.png',x=127,y=565)
    for i in arange(1,11):
        a.sleep(0.05)
        a.clone('cmos'+str(1+int(i)),x=127+10*i)
    for i in arange(1,17):
        a.sleep(0.05)
        a.clone('cmos'+str(11+int(i)),y=565-10*i)
    for i in arange(1,12):
        a.sleep(0.05)
        a.clone('cmos'+str(27+int(i)),x=227+10*i)
    i=0
    while 1:
        try:
            a.erase('cmos'+str(2+i),0)
        except KeyError:
            break
        else:
            i += 1
            a.wait()
    a.sleep(4)
    a.fade('cap2')
    a.replace_text('cap1',"However, at the NMOS, VGS = Vin - 0 reaches its positive threshold, turning it to")
    a.replace_text('cap2','linear operation.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('cmos2.png',x=127,y=565)
    for i in arange(1,11):
        a.sleep(0.05)
        a.clone('cmos'+str(1+int(i)),x=127+10*i)
    for i in arange(1,17):
        a.sleep(0.05)
        a.clone('cmos'+str(11+int(i)),y=565+10*i)
    for i in arange(1,12):
        a.sleep(0.05)
        a.clone('cmos'+str(27+int(i)),x=227+10*i)
    a.sleep(3)
    a.fade('cap2')
    a.replace_text('cap1',"The drain connects to the source, which is connected to ground, thus the NMOS contributes")
    a.replace_text('cap2','0 as ouput, since current flows from high to low potential.',mode=0,vis=False)
    a.fade('cap2')
    for i in arange(1,4):
        a.sleep(0.05)
        a.clone('cmos'+str(38+int(i)),x=337+10*i)
    for i in arange(1,4):
        a.sleep(0.05)
        a.clone('cmos'+str(41+int(i)),y=725+10*i)
    for i in arange(1,27):
        a.sleep(0.05)
        a.clone('cmos'+str(44+int(i)),x=367+10*i)
    for i in arange(1,25):
        a.sleep(0.05)
        a.clone('cmos'+str(70+int(i)),y=755+10*i)
    i=0
    while 1:
        try:
            a.erase('cmos'+str(2+i),0)
        except KeyError:
            break
        else:
            i += 1
            a.wait()
    a.sleep(4)
    a.fade('cap2')
    a.replace_text('cap1','Thus, an input of 1 gets an output of 0.')
    a.add_fade_text('out1','0',x=115,y=855,font=font)
    a.sleep(1)
    a.add_fade_text('in0','0',x=30,y=930,font=font)
    a.replace_text('cap1',"When the input is 0, at the NMOS, VGS = Vin - 0 does not reach its positive threshold,")
    a.replace_text('cap2','so the NMOS stays in cutoff mode and does not contribute to the output.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('cmos2.png',x=127,y=565)
    for i in arange(1,11):
        a.sleep(0.05)
        a.clone('cmos'+str(1+int(i)),x=127+10*i)
    for i in arange(1,17):
        a.sleep(0.05)
        a.clone('cmos'+str(11+int(i)),y=565+10*i)
    for i in arange(1,12):
        a.sleep(0.05)
        a.clone('cmos'+str(27+int(i)),x=227+10*i)
    i=0
    while 1:
        try:
            a.erase('cmos'+str(2+i),0)
        except KeyError:
            break
        else:
            i += 1
            a.wait()
    a.sleep(4)
    a.fade('cap2')
    a.replace_text('cap1',"However, at the PMOS, VGS = Vin - Vdd reaches its negative threshold, turning it to linear")
    a.replace_text('cap2','operation.',mode=0,vis=False)
    a.fade('cap2')
    a.add_fade('cmos2.png',x=127,y=565)
    for i in arange(1,11):
        a.sleep(0.05)
        a.clone('cmos'+str(1+int(i)),x=127+10*i)
    for i in arange(1,17):
        a.sleep(0.05)
        a.clone('cmos'+str(11+int(i)),y=565-10*i)
    for i in arange(1,12):
        a.sleep(0.05)
        a.clone('cmos'+str(27+int(i)),x=227+10*i)
    a.sleep(3)
    a.fade('cap2')
    a.replace_text('cap1','The source connects to the drain. Since the source is connected to Vdd, the PMOS then')
    a.replace_text('cap2','contributes 1 as output.',mode=0,vis=False)
    a.fade('cap2')
    a.clone('cmos39',x=635,y=205)
    for i in arange(1,17):
        a.sleep(0.05)
        a.clone('cmos'+str(39+int(i)),y=205+10*i)
    for i in arange(1,24):
        a.sleep(0.05)
        a.clone('cmos'+str(55+int(i)),x=635-10*i)
    for i in arange(1,10):
        a.sleep(0.05)
        a.clone('cmos'+str(78+int(i)),y=365+10*i)
    for i in arange(1,24):
        a.sleep(0.05)
        a.clone('cmos'+str(87+int(i)),x=405+10*i)
    for i in arange(1,11):
        a.sleep(0.05)
        a.clone('cmos'+str(110+int(i)),y=455+10*i)
    for i in arange(1,11):
        a.sleep(0.05)
        a.clone('cmos'+str(120+int(i)),x=635+10*i)
    i=0
    while 1:
        try:
            a.erase('cmos'+str(2+i),0)
        except KeyError:
            break
        else:
            i += 1
            a.wait()
    a.sleep(4)
    a.fade('cap2')
    a.replace_text('cap1','Thus, an input of 0 gets an output of 1.')
    a.add_fade_text('out0','1',x=115,y=930,font=font)
    a.sleep(1)
    a.replace_text('cap1','Hence, this CMOS functions as a NOT gate (like a boolean operator).')
    a.sleep(2)
    a.erase('in1',0)
    a.erase('in0',0)
    a.erase('out1',0)
    a.erase('out0',0)
    a.erase('cmos1')
    a.replace_text('cap1','Many, many logic gates make up an integrated circuit (aka IC or chip).')
    a.sleep(2)
    a.replace_text('cap1','But how are such tiny yet extensively detailed chips made?')
    a.sleep(2)
    a.fade('cap1')
    a.add_fade_text('section','3. Manufacturing',x=414,y=485)
    a.sleep(2)
    a.erase('section')
    a.sleep(5)
    pg.quit()
    
if __name__ == '__main__':
    main()
