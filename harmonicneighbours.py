pitch_class = {0:'C',1:['C#', 'Db'],2:'D',3:['D#', 'Eb'],\
               4:['E','Fb'] ,5:'F',6:['F#', 'Gb'],7:'G',\
               8:['G#','Ab'],9:'A',10:['A#','Bb'] ,11:'B'}
mode = {0:'major', 1:'minor'}


camelot = {'01A': [['G#','Ab'], 'minor'],
           '02A': [['D#','Eb'], 'minor'],
           '03A':[['A#','Bb'], 'minor'],
           '04A':['F', 'minor'],
           '05A':['C', 'minor'],
           '06A':['G', 'minor'],
           '07A':['D', 'minor'],
           '08A':['A', 'minor'],
           '09A':['E', 'minor'],
           '10A':['B', 'minor'],
           '11A':[['F#','Gb'], 'minor'],
           '12A':[['C#', 'Db'], 'minor'],
           '01B':['B', 'major'],
           '02B':[['F#', 'Gb'], 'major'],
           '03B':[['C#','Db'], 'major'],
           '04B':[['G#','Ab'], 'major'],
           '05B':[['D#','Eb'], 'major'],
           '06B':[['A#','Bb'], 'major'],
           '07B':['F', 'major'],
           '08B':['C', 'major'],
           '09B':['G', 'major'],
           '10B':['D', 'major'],
           '11B':['A', 'major'],
           '12B':[['E','Fb'], 'major']}

def translate_pc_cam(key_pc, mode_pc):
    """takes a key in pitch class notation and the mode and return the key in camelot notation"""
    key = pitch_class[key_pc]
    tonality = mode[mode_pc]
    key_cam = [k for k,v in camelot.items() if v == [key, tonality]]
    return key_cam[0:1][0]

def translate_cam_pc(key_cam):
    """takes a key in camelot notation and return the key in pitch class notation and the mode"""
    key = camelot[key_cam][0]
    tonality = camelot[key_cam][1]
    print(key, tonality)
    key_pc = [k for k,v in pitch_class.items() if v == key]
    mode_pc = [k for k,v in mode.items() if v == tonality]
    return key_pc, mode_pc

def harmonic_sibblings(key_cam):
    """takes a key in camelot notation and returns the 4 harmonic neighbours"""
    dict_trans={'01':'07','02':'08','03':'09','04':'10','05':'11','06':'12','07':'01','08':'02','09':'03','10':'04','11':'05','12':'06'}
    
    
    if key_cam[2] =='A':
        pos_keys = [str(int(key_cam[0:2])+1)+key_cam[2],\
        str(int(key_cam[0:2])-1)+key_cam[2],\
        str(int(dict_trans[key_cam[0:2]]))+key_cam[2],\
        key_cam[0:1]+'B']
    else:
        pos_keys = [str(int(key_cam[0:2])+1)+key_cam[2],\
        str(int(key_cam[0:2])-1)+key_cam[2],\
        str(int(dict_trans[key_cam[0:2]]))+key_cam[2],\
        key_cam[0:1]+'A']
    for key in range(0,len(pos_keys)):
        if len(pos_keys[key]) == 2:
            pos_keys[key]= '0'+ pos_keys[key]
            
    for i in range(0,len(pos_keys)):
        if int(pos_keys[i][0:2])>12:
            pos_keys[i] = pos_keys[i].replace('13','01')
        elif int(pos_keys[i][0:2]) < 1:
            pos_keys[i]=pos_keys[i].replace('00','12')
    return pos_keys