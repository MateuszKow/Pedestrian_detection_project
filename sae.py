import math
import numpy as np
import cv2
import argparse
from glob import glob
from src.io.psee_loader import PSEELoader
import src.io.dat_events_tools as dat_tools
from src.visualize import vis_utils as vis
import copy as cp
import cv2
import os
import shutil

def draw_bboxes(img, boxes, labelmap):
    """
    draw bboxes in the image img
    """
    colors = cv2.applyColorMap(np.arange(0, 255).astype(np.uint8), cv2.COLORMAP_HSV)
    colors = [tuple(*item) for item in colors.tolist()]
    print(boxes)
    for i in range(boxes.shape[0]):
        pt1 = (int(boxes['x'][i]), int(boxes['y'][i]))
        size = (int(boxes['w'][i]), int(boxes['h'][i]))
        pt2 = (pt1[0] + size[0], pt1[1] + size[1])
        score = boxes['class_confidence'][i]
        class_id = boxes['class_id'][i]
        class_name = labelmap[class_id % len(labelmap)]
        color = colors[class_id * 60 % 255]
        center = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
        cv2.rectangle(img, pt1, pt2, color, 1)
        cv2.putText(img, class_name, (center[0], pt2[1] - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
        cv2.putText(img, str(score), (center[0], pt1[1] - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
        
        
def convert_frame_bbox_TO_yolo_format(frame_bbox,height,width):
    #print(height,width)
    list_bboxes=[]
    for bbox in frame_bbox:
        list_bboxes.append("0 "+str((bbox["x"]+bbox["w"]/2)/width)+" "+str((bbox["y"]+bbox["h"]/2)/height)+" "+str((bbox["w"])/width)+" "+str((bbox["h"])/height))
    return list_bboxes

def to_txt(path_to_save,name,labels):
    with open(path_to_save+"labels/"+name+".txt","w+") as f:
        if labels:
            for label in labels[:-1]:
                f.write(f'{label}\n')
            f.write(f'{labels[-1]}')
    
    
def sae(datfile,bounding,path):
    psee=PSEELoader(path+datfile)
    bbox=PSEELoader(path+bounding)
    path_to_save="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/prophesee-automotive-dataset-toolbox/sae/val/"
    #psee.seek_time(4000000)
    #bbox.seek_time(4000000)
    accumulation_time=5000
    height,width=psee.get_size()
    counter=0
    while psee.current_time<psee.total_time():
        image=(np.ones((psee.get_size()[0],psee.get_size()[1],3)))*(psee.current_time)
        start=psee.current_time
        frame_events=psee.load_delta_t(accumulation_time)
        frame_bbox=bbox.load_delta_t(accumulation_time)
        for event in frame_events:
            if event["x"]<1280 and event["y"]<720:
                image[event['y']][event["x"]]=event["t"]
        image=np.floor(255*(image-start)/(accumulation_time)).astype('uint8')
        counter+=1
        Yolo_labels=convert_frame_bbox_TO_yolo_format(frame_bbox,psee.get_size()[0],psee.get_size()[1])
        #draw_bboxes(image, frame_bbox,vis.LABELMAP_LARGE)
        print(counter)
        if counter%2==0:
            if Yolo_labels:
                cv2.imwrite(path_to_save+"images/"+datfile[:-4]+"_"+str(counter)+".png", image)
                to_txt(path_to_save,datfile[:-4]+"_"+str(counter),Yolo_labels)
                
if __name__ == '__main__':
    path="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_v2/val/"
    
    os.chdir(path)
    dat_list=[file for file in os.listdir() if file.endswith(".dat") ]
    #dat_list=["moorea_2019-06-21_000_854500000_914500000_td.dat"]
    boxes_list = [glob(td_file.split('_td.dat')[0] +  '*.npy')[0] for td_file in dat_list]
    for i in range(len(boxes_list)):
        sae(dat_list[i],boxes_list[i],path)
    
    path="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_v2/train/"
    os.chdir(path)
    dat_list=[file for file in os.listdir() if file.endswith(".dat") ]
    #dat_list=["moorea_2019-06-21_000_854500000_914500000_td.dat"]
    boxes_list = [glob(td_file.split('_td.dat')[0] +  '*.npy')[0] for td_file in dat_list]
    for i in range(len(boxes_list)):
        sae(dat_list[i],boxes_list[i],path)