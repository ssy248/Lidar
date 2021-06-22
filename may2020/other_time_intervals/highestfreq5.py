def highestfreq5(fromi):
    highest = 0
    indexhighest = fromi
    
    list5 =trajcount5[fromi]
    indexhighest= max(list5.items(), key=operator.itemgetter(1))[0]
    return indexhighest
