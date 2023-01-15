import math
import numpy as np
import cv2
import argparse
from glob import glob
from src.io.psee_loader import PSEELoader
import src.io.dat_events_tools as dat_tools
import copy as cp

EV_TYPE = [('t', 'u4'), ('_', 'i4')]  # Event2D
EV_STRINGS = 'Event2D'

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(
        description='visualize one or several event files along with their boxes')
    parser.add_argument('records', nargs="+",
                        help='input event files, annotation files are expected to be in the same folder')
    parser.add_argument('-s', '--skip', default=0, type=int, help="skip the first n microseconds")
    parser.add_argument('-d', '--delta_t', default=20000, type=int, help="load files by delta_t in microseconds")

    return parser.parse_args()





def search_between(x_start,x_stop,y_start,y_stop,all_events):
    x=all_events[all_events['x']<x_stop]
    x=x[x['x']>=x_start]
    x=x[x['y']>=y_start]
    return x[x['y']<y_stop]
    

def cutting(datfile):
    psee=PSEELoader(datfile)
    all_events=psee.load_n_events(psee.event_count())
    sensor_sizes=psee.get_size()
    rows,cols=(3,4)
    height,width=(sensor_sizes[0]//rows,sensor_sizes[1]//cols)
    
    #print((all_events[-1]),psee.total_time())
    #print(all_events[all_events['x']<100])
    #dictionary_of_streams={
    ##    1: search_between(0, 320, 0, 240, all_events),
      #  2: search_between(320, 640, 0, 240, all_events),
       # }
    list_of_streams=[]
    for i in range(rows):
        for j in range(cols):
            print(i,j)
            slice_image=search_between(j*width, width*(j+1), i*height, height*(i+1), all_events)
            slice_image['x']=slice_image['x']-width*j
            slice_image['y']=slice_image['y']-height*i
            list_of_streams.append(slice_image)
    return list_of_streams,height,width


def get_areas(left_top,right_bottom,width,height):
    areas={(0,0):0,
           (1,0):1,
           (2,0):2,
           (3,0):3,
           (0,1):4,
           (1,1):5,
           (2,1):6,
           (3,1):7,
           (0,2):8,
           (1,2):9,
           (2,2):10,
           (3,2):11
           }
   # left_top_area=areas[(math.floor(left_top[0]/width),math.floor(left_top[1]/height))]
   # right_bottom_area=areas[(math.floor(right_bottom[0]/width),math.floor(right_bottom[1]/height))]
    
    #if left_top_area==right_bottom_area:
    #    return [left_top_area]
    if right_bottom[0]>=1280:
        right_bottom=(1279,right_bottom[1])
    if right_bottom[1]>=720:
        right_bottom=(right_bottom[0],719)
    if right_bottom[0]<0 or right_bottom[1]<0 or left_top[0]<0 or left_top[1]<0:
        return []
    #print(right_bottom,left_top)
    
    cols=[c for c in range(math.floor(left_top[0]/width),math.floor(right_bottom[0]/width)+1)]
    rows=[r for r in range(math.floor(left_top[1]/height),math.floor(right_bottom[1]/height)+1)]
    lista=[]
    for c in cols:
        for r in rows:
            lista.append(areas[(c,r)])
    return lista

def calculate_area_in_slice(event,slice_index):
    boundries={0:([0,320],[0,240]),1:([320,640],[0,240]),2:([640,960],[0,240]),
               3:([960,1280],[0,240]),
               4:([0,320],[240,480]),5:([320,640],[240,480]),6:([640,960],[240,480]),
               7:([960,1280],[240,480]),
               8:([0,320],[480,720]),9:([320,640],[480,720]),10:([640,960],[480,720]),
               11:([960,1280],[480,720])}
    
    bound=boundries[slice_index]    
    p=[(event["x"],event["y"]),(event["x"]+event['w'],event["y"]),(event["x"],event["y"]+event["h"]),(event["x"]+event['w'],event["y"]+event["h"])]
    
    if bound[0][0]<=event['x']<bound[0][1]:
        x=event['x']
    col=[320,640,960,1280]
    row=[240,480,720]
    
def cut_slice(event,slice_index):
    boundries={0:([0,320],[0,240]),1:([320,640],[0,240]),2:([640,960],[0,240]),
               3:([960,1280],[0,240]),
               4:([0,320],[240,480]),5:([320,640],[240,480]),6:([640,960],[240,480]),
               7:([960,1280],[240,480]),
               8:([0,320],[480,720]),9:([320,640],[480,720]),10:([640,960],[480,720]),
               11:([960,1280],[480,720])}
    
    #p=[(event["x"],event["y"]),(event["x"]+event['w'],event["y"]),(event["x"],event["y"]+event["h"]),(event["x"]+event['w'],event["y"]+event["h"])]
    bound=boundries[slice_index]
    changed_event=cp.deepcopy(event)
    #if changed_event["ts"]==54986216:
    #    print(changed_event)
    #print("zwykly",event,slice_index)
    if changed_event["x"]<bound[0][0]:
        x1=bound[0][0]
    else:
        x1=event["x"]
    if changed_event["x"]+changed_event["w"]>bound[0][1]:
        x2=bound[0][1]
    else:
        x2=changed_event["x"]+changed_event["w"]
    if changed_event["y"]<bound[1][0]:
        y1=bound[1][0]
    else:
        y1=changed_event["y"]
    if changed_event["y"]+changed_event["h"]>bound[1][1]:
        y2=bound[1][1]
    else:
        y2=changed_event["y"]+changed_event["h"]
    #x1=max(event["x"],bound[0][0])
    #x2=min(event["x"]+event['w'],bound[0][1])
    #print(x1,x2)
    #print(y1,y2)
    #print(event,slice_index)
    #y1=max(event["y"],bound[1][0])
    #y2=min(event["y"]+event['h'],bound[1][1])
    w=x2-x1
    h=y2-y1
    #changed_event=event
    changed_event['x']=x1
    changed_event['y']=y1
    changed_event['w']=w
    changed_event['h']=h
    #print("zmieniony",changed_event)
    return w*h,changed_event
    
def offset(lista_area,i,width,height):
    areas={0:(0,0),
               1:(1,0),
               2:(2,0),
               3:(3,0),
               4:(0,1),
               5:(1,1),
               6:(2,1),
               7:(3,1),
               8:(0,2),
               9:(1,2),
               10:(2,2),
               11:(3,2)
               }
    c,r=areas[i]
    lista=[]
    for event in lista_area:
        new_event=cp.deepcopy(event)
        new_event["x"]=event["x"]-width*c
        new_event["y"]=event["y"]-height*r  
        lista.append(new_event)
    return lista
        
   
def bounding_box_processing(bbox,width=320,height=240):
    BBOX_DTYPE = np.dtype({'names':['ts','x','y','w','h','class_id','confidence','track_id'], 'formats':['<u8','<f4','<f4','<f4','<f4','<u1','<f4','<u4']})
    bbox=bbox[bbox['x']>=0]
    bbox=bbox[bbox['class_id']==0]
    lists = [[] for _ in range(12)]
    dic={0:[],
               1:[],
               2:[],
               3:[],
               4:[],
               5:[],
               6:[],
               7:[],
               8:[],
               9:[],
               10:[],
               11:[]
               }
    #print(len(lists))
    list_of_events=[]
    for event in bbox:
        area=event["w"]*event["h"]
        #print(event)
        lista_areas=get_areas((event["x"],event["y"]),(event["x"]+event["w"],event["y"]+event["h"]),width,height)
        for index in lista_areas:
            (area_in_slice,changed_event)=cut_slice(event,index)
            if area_in_slice/area>0.25:
                #(lists[index]).append(changed_event)
                #dic[index].append(changed_event)
                list_of_events.append((changed_event,index))
                
        
    for elem in list_of_events:
        lists[elem[1]].append(elem[0])
    for x in range(12):
        lists[x]=offset(lists[x], x, width, height)  
    for x in range(12):
        #pass
        print(lists[x],"lista")
        new = np.array(lists[x], dtype=BBOX_DTYPE)
        print(new)
        np.save("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_cut_cars/train/moorea_2019-06-26_test_02_000_1220500000_1280500000_"+str(x)+"_bbox.npy",new)
        
        
        
            

if __name__ == '__main__':
    #datfile="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_v3/val/moorea_2019-02-19_005_td_549500000_609500000_td.dat"
    bounding_box=np.load("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_v3/train/moorea_2019-06-26_test_02_000_1220500000_1280500000_bbox.npy")
    #file_h=open(datfile,"rb")
    #print(dat_tools.parse_header(file_h))
    #new_bounding=np.load("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_my_choice/moorea_2019-02-21_001_td_488500000_548500000_bbox.npy")
    bounding_box_processing(bounding_box)
    #np.save("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/prophesee-automotive-dataset-toolbox/pociete_reprezentacje/0_bbox.npy",y)    
    #(streams,height,width)=cutting(datfile)
    #file="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_cut_cars/val/moorea_2019-02-19_005_td_549500000_609500000_"
    #for i in range(len(streams)):
        #handler_file=dat_tools.write_header(file+str(i)+"_td.dat",height,width)
    
        #dat_tools.write_event_buffer(handler_file, streams[i])
   # ARGS = parse_args()
 #   play_files_parallel(ARGS.records, skip=ARGS.skip, delta_t=ARGS.delta_t)