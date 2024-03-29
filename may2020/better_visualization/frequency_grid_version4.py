# 2/2/21 version
# do not initialize countmap, but check if val is none
# added predict method

# run algorithm on input

# test initializing

import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


# december highest 
# step 4 b 


class frequency_grid(object):
    
    def __init__(self): # initialize forward and back map outside of init
        #self.numpoints = numpoints
        self.time_elapsed= 0 # 0
        self.numcells = 160000
        
        self.thres = 10 # for hybrid 2 method
        self.angles = [] 
        
        self.xmin =-200
        self.xmax = 200
        self.ymin =-200
        self.ymax =200
        
        self.forwardmap = {}  # dcmap1
        self.backmap = {}
        
        ind_temp = 0
        for ix in range(int(self.xmin), int(self.xmax)):
            for iy in range(int(self.ymin), int(self.ymax)):
                myvec = []
                myvec.append(ix)
                myvec.append(iy)
                self.forwardmap[ind_temp] = myvec
                self.backmap[(ix, iy)]= ind_temp
                ind_temp=ind_temp+1
                
        self.countmap = {}
        
        self.current_position = []
        self.prevmap = {} # set to current map at end of frame 
        self.currentmap = {}
        
        self.tracking_list = {} # list of objects that are tracked 
        
        self.range = 10
        
        # initialize grid count map
        self.countmap = {}
        
        # tracked array?
        self.trackinglist = {}
    
        
    # set up based on trajectories file : training method 
    def setup_grid(self): 
        
        fileind = 1
        for filename in os.listdir('24hrdata'):
            print("file", filename)
            fname = '24hrdata/'+filename
            fileind =fileind+1
            #irow=0
            obnum=1
            with open(fname) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    trajectory_num = row[0]
                    if line_count==0:
                        line_count = line_count+1 # skip header
                        continue
                    if line_count==1:
                        prevrow = row
                        prevx = float(prevrow[6])
                        prevy = float(prevrow[7])
                        pfx = round(prevx)
                        pfy = round(prevy)
                        line_count = line_count+1
                        continue
                    currentx = float(row[6])
                    currenty = float(row[7])
                    fx = round(currentx)
                    fy = round(currenty)
                    if pfx == fx and pfy ==fy:
                        #prevframe = frameindex
                        continue
                    if obnum != trajectory_num:
                        pfx = fx
                        pfy = fy
                        obnum = trajectory_num
                        continue
                    #save
                    fromi = self.backmap[(pfx, pfy)]
                    toi = self.backmap[(fx, fy)]
                    #print("fromi is", fromi)
                    #print("toi is", toi)
                    if abs(pfx - fx)>10 or abs(pfy - fy)>10:
                        continue
                    # check if it is none 
                    val = self.countmap.get((fromi, toi))
                    if val == None:
                        #print("none val for fromi", fromi,"to toi ", toi)
                        self.countmap[(fromi, toi)] = 1
                    else:
                        
                        mcount = self.countmap[(fromi, toi)]
                        self.countmap[(fromi, toi)] = mcount+1
                        # check by printing
                        if mcount >600:
                            print("countmap from i: ", fromi, " toi:", toi)
                    pfx=fx
                    pfy=fy
    
    def highestfreq(self, fromi):
        highest = 0
        indexhighest = fromi
        (px, py) = self.forwardmap[fromi]
        for j in range(-10, 11):
            jx = px+j
            if jx>self.xmax-1 or jx<self.xmin: # check if pts in range
                continue
            for k in range(-10, 11):
                jy = py+k
                # check if pts are in range
                if jy>self.ymax-1 or jy<self.ymin:
                    continue
                toi = self.backmap[(jx, jy)]
                # check if value is none 
                val = self.countmap.get((fromi, toi))
                if val == None:
                    t = 0
                else:
                    t = self.countmap[(fromi, toi)]
                #if t>0:
                    #print(t)
                if t > highest:
                    highest=t
                    indexhighest=toi
        return highest, indexhighest
    
    def predict(self, frame_gen, ind): # ind: current index
        # frame gen is 
        next_frame = next(frame_gen)
        #print("len of next frame", len(next_frame))
        lenframe = len(next_frame)
        mf = defaultdict(list)
        
        mx = lenframe
        for j in range(0, mx):
            mf[j] = 0
            
        matchfreq = mf
        
        f= 0
        currentmap = {} # temporary currentmap
        currentmap_freq = {} # holds freq scores
        
        xvalues=[]
        yvalues=[]
        
        for i in range(0, lenframe):
            #if i>1:
            #    break # test out 
            ptcloud = next_frame[i].point_cloud
            for p in ptcloud:
                # extract x and y values
                px =p[0]
                py =p[1]
                xvalues.append(px)
                yvalues.append(py)
                print("pc of x", px)
                print("pc of y", py)
                xr = round(px)
                yr = round(py)
                fromi = self.backmap[(xr, yr)]
                h1, i1 = self.highestfreq(fromi)
                # save to map
                currentmap[i1] = 1
                currentmap_freq[i1] = h1 
                val = self.prevmap.get(fromi)
                if val ==None:
                    pass
                else:
                    matchfreq[i] = matchfreq[i] +1
            if matchfreq[i] > f:
                ky = i
                hxvalues = xvalues
                hyvalues = yvalues
                totalmap[ky]= currentmap
                
            if len(hxvalues)==0:
                break
            else:
                # return ky
                self.trackinglist[ind] = ky 
                return ky
                
        
        
