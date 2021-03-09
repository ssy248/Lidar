# reset frame gen
frame_gen = FrameGen(pcap_file_path,detecting_range,bck_voxel_path,with_bf=False).DBSCAN_pcap_frame_generator(eps,min_samples)

# find a way to find longest trajectory ?
#fg1 = frequency_grid()
#fg2 = frequency_grid()
#fg3 = frequency_grid()

fgs = []

totlen = 20

# start from future frame
future= 20 

for i in range(0, future):
    nframe_gen = next(frame_gen)

print("length of starting frame is", len(nframe_gen))
    
for i in range(0, totlen):
    fgi = frequency_grid()
    fgi.setup_grid()
    fgi.set_first_coordinates(nframe_gen, i)
    fgs.append(fgi)

    
counternums = []

for i in range(0, totlen):
    c = 1
    # reset frame gen 
    # reset frame gen
    frame_gen = FrameGen(pcap_file_path,detecting_range,bck_voxel_path,with_bf=False).DBSCAN_pcap_frame_generator(eps,min_samples)
    
    for j in range(0, future):
        nframe_gen =next(frame_gen)
        
    t = True
    fg1 = fgs[i]
    while t:
        t= fg1.continueboolean
        nframe_gen = next(frame_gen)
        fg1.predict(nframe_gen)
        c=c+1
    counternums.append(c)

# total length of frame gen? 
