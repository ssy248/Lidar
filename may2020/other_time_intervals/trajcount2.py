# 0.2, 0.3, 0.5 
trajcount2 ={}

# train trajcount2

fileind = 1
import os
for filename in os.listdir('24hrdata'):
    goforward=0
    #entries = os.listdir()
    print(filename)
    fileind = fileind+1
    #if fileind > 3:
    #    break
    fname = '24hrdata/'+filename
    irow=0
    obnum=1
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            irow=irow+1
            trajnum = row[0]
            frameindex = row[17]
            #print("frame:",frameindex)
            if line_count==0:
                line_count=line_count+1
                continue
            if line_count==1:
                line_count=line_count+1
                prevrow = row
                prevx = float(prevrow[6])
                prevy = float(prevrow[7])
                print(prevx)
                print(prevy)
                # use round instead of floor
                pfx1 = round(prevx) # use pfx1, pfx2 
                pfy1 = round(prevy)
                continue
            if line_count==2:
                line_count=line_count+1
                pfx2 = pfx1
                pfy2 = pfy1
                pfx1 = round(float(row[6]))
                pfy1 = round(float(row[7]))
                continue
            currentx = float(row[6])
            currenty = float(row[7])
            fx = round(currentx)
            fy = round(currenty)
            
            if goforward==1:
                goforward=0
                pfx2 = pfx1
                pfy2 =pfy1
                pfx1 =fx
                pfy1 =fy
                line_count=line_count+1
                continue
            
            if obnum != trajnum:
                pfx1 = fx
                pfy1 = fy
                # reset pfx2 , pfy2 : go forward 1 row
                goforward=1
                obnum = trajnum
                prevframe = frameindex
                line_count = line_count+1
                continue
            # save to map
            fromi = dinvlookupdict[(pfx2,pfy2)]
            toi = dinvlookupdict[(fx,fy)]
            
            # check if it is in range : exclude outliers dictionary
            """if abs(pfx - fx)>10 or abs(pfy - fy)>10:
                line_count= line_count+1
                continue"""
            list2 = trajcount2.get(fromi) # list of maps
            if list2 ==None:
                #newlist2 = []
                #newmap2 = {}
                #newmap2[toi] = 1
                newmapfrom = {}
                newmapfrom[toi]= 1
                trajcount2[fromi]= newmapfrom
            else:
                getcount= list2.get(toi)
                if getcount==None:
                    list2[toi] = 1
                    trajcount2[fromi] = list2
                else:
                    count2 = list2[toi]
                    newcount = count2+1
                    list2[toi] = newcount
                    trajcount2[fromi] = list2
                
            
            #mcount = trajcount2[(fromi, toi)]
            #if mcount>5000:
            #    print("fromi:", fromi, " toi:", toi)
            #dtrajcount[(fromi, toi)]= mcount+1
            pfx2 = pfx1
            pfy2 = pfy1
            pfx1 = fx
            pfy1 = fy 
            prevframe= frameindex
            line_count = line_count+1
            
            
