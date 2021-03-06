# STEP 4 C 
# updated process from above

#input
tfile ="april2019/2019-02-27-12-19-36_Velodyne-HDL-32-Data-BF1-CL1-Traj.csv"

import math
import csv

trajnum = 0 
obnum = 1

irow =0

outlier =0

#settimestamp={0}
#setx ={0}
#sety ={0}

#settimestamp.clear()
#setx.clear()
#sety.clear()

# change settimestamp to a normal array
settimestamp= []
setx =[]
sety =[]

with open(tfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        irow=irow+1
        trajnum = row[0]
        frameindex = row[17]          
        # check first row
        if line_count==0:
            line_count=line_count+1
            continue       
        # check first row of data 
        if line_count==1:
            line_count=line_count+1
            prevrow = row
            prevx = float(prevrow[6])
            prevy = float(prevrow[7])
            pfx = math.floor(prevx)
            pfy = math.floor(prevy)
            prevtimestamp = float(prevrow[2])
            continue        
        # check if is vehicle
        vp = row[1]
        if vp == 1:
            continue
        # load current info
        currx =float(row[6])
        curry =float(row[7])
        fx = math.floor(currx)
        fy = math.floor(curry)
        # debug -6, 17
        if fx==-6 and fy==17:
            print("actual x:",currx)
            print("actual y:",curry)
            print("row",irow)
        timestamp = float(row[2])
        # compare current + previous timestamps 
        ts = timestamp*0.000001
        pts = prevtimestamp*0.000001
        diff = ts - pts 
        
        # first check if in the same trajectory
        if obnum != trajnum:
            pfx = fx
            pfy= fy
            obnum = trajnum
            prevframe=frameindex
            prevtimestamp = timestamp
            # if in diff traj, delete settimestamp /clear 
            settimestamp=[]
            setx= []
            sety=[]
            continue
        #print("frame:",frameindex)
        
        # check if there is difference
        if pfx==fx and pfy==fy:
            prevtimestamp = timestamp
            continue
        # check for zero valued timestamp
        if timestamp==0:
            prevtimestamp=0
            # set previous x, y
            pfx = fx
            pfy = fy
            continue
        # check for zero valued previous timestamp 
        if prevtimestamp==0:
            prevtimestamp=timestamp
            pfx = fx
            pfy= fy
            continue
        # test the diff in set 
        if len(settimestamp) != 0:
            #print some info 
            #print("settimestamp at", irow)
            setlen = len(settimestamp)
            for i in range(0, setlen-1):
                sts1 = settimestamp[i]
                pfx1 = setx[i]
                pfy1 = sety[i]
                #test current time stamp
                ts1 = sts1*0.000001
                #pts1 = prevtimestamp*0.000001
                diff1 = ts - ts1
            # if current distance greater than 0.15, discard
                if diff1 > 0.15:
                    #settimestamp.remove(sts1)
                    del settimestamp[i]
                    # also remove from setx and sety
                    del setx[i]
                    del sety[i]
                    continue
                if diff1< 0.05:
                    continue
                # if falls within 0.05 to 0.15 
                pfx1 = setx[i]
                pfy1 = sety[i]
                fromi1 = invlookupdict[(pfx1,pfy1)]
                toi1 = invlookupdict[(fx, fy)]                
                # debug -12, 29 and -6, 17
                if pfx1==-6 and pfy1 ==17:
                    print('to x:',fx)
                    print('to y:',fy)
                    print("row",irow)
                # change to not count when prev pt equals current pt 
                
                mcount1 = trajcount1[(fromi1,toi1)]
                trajcount1[(fromi1, toi1)] = mcount1+1
                #print("from coord at", pfx1, pfy1)
                #print("to coord at", fx, fy)
                # add to the trajectory 
        # higher than 0.15
        if diff > 0.15:
            # set previous values
            pfx = fx
            pfy = fy
            prevtimestamp = timestamp
            # clear the sets?
            continue
        # lower than 0.05
        if diff < 0.05:   
            #print("settimestamp at", irow)
            #print("current time stamp", timestamp)
            #print("previous time stamp", prevtimestamp)
            # add to sets 
            #prevtimestamp stays the same 
            # pfx and pfy stay the same 
            settimestamp.append(prevtimestamp)
            prevtimestamp =timestamp
            setx.append(pfx)
            pfx =fx
            sety.append(pfy)
            pfy = fy
            continue  # continue 
        # if falls within 0.05 to 0.15 
        #print('current timestamp:',ts)
        
        
        # now save to the map(i,j)
        
        fromi = invlookupdict[(pfx,pfy)]
        #topt = []
        toi = invlookupdict[(fx,fy)]
        
        # debug -12, 29 and -6, 17
        if pfx==-6 and pfy==17:
            print('outer loop to x:',fx)
            print('outer loop to y:',fy)
            #print('real x val',currx)
            #print('real y val',curry)
            print("row",irow)
        mcount = trajcount1[(fromi,toi)]
        trajcount1[(fromi, toi)] = mcount+1
        # set previous
        pfx = fx
        pfy = fy
        #prevframe = frameindex
        #prevtrajnum= trajnum
        prevtimestamp = timestamp 
        
        # condition break for testing
        #if irow > 10000:
            # print 
         #   print("fx", fx)
          #  print("fy", fy)
           # break  
            
