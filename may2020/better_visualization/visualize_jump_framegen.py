# jump ahead to future next frame gen

# reset frame gen
frame_gen = FrameGen(pcap_file_path,detecting_range,bck_voxel_path,with_bf=False).DBSCAN_pcap_frame_generator(eps,min_samples)

# find a way to find longest trajectory ?
#fg1 = frequency_grid()
#fg2 = frequency_grid()
#fg3 = frequency_grid()

fgs = []

totlen = 40

# start from future frame
future= 10 

nframe_gen = frame_gen
for i in range(0, future):
    nframe_gen = next(nframe_gen)

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
    nframe_gen = frame_gen
    for i in range(0, future):
        nframe_gen = next(nframe_gen)
    t = True
    fg1 = fgs[i]
    while t:
        t= fg1.continueboolean
        nframe_gen = next(frame_gen)
        fg1.predict(nframe_gen)
        c=c+1
    counternums.append(c)

# total length of frame gen? 