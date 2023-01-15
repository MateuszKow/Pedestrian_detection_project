import numpy as np
import pandas as pd
import os
#bounding=np.load("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/nagrania_do_przejrzenia/duzy_czlowiek")
path="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/prophesee-automotive-dataset-toolbox/sae/val"
os.chdir(path)
labels_list=os.listdir("labels")
image_list=os.listdir("images")
print(labels_list)
#for file in file_list:
 #   if file.endswith(".npy"):
  #      bounding=np.load(file)
   #     bounding=bounding[bounding["class_id"]==1]
    #    bounding["class_id"]=0
     #   np.save(file,bounding)
for file in labels_list:
    if file[:-4]+".png" in image_list:
        os.remove("images/"+file[:-4]+".png")
        
#bounding=np.load("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/G1/train/17-03-30_12-53-58_122500000_182500000_bbox.npy")
#delta_t=50000
#print(type(bounding[0]))
#new_bounding=bounding
#print(bounding)
#print(new_bounding)
#df=pd.DataFrame(bounding)
#for e in []:
#   new_bounding=new_bounding[new_bounding["track_id"]!=e]
#new_bounding=new_bounding[new_bounding["class_id"]==2]
#new_bounding["class_id"]=0
#for e in [1000]:
#          new_bounding=new_bounding[new_bounding["track_id"]!=e]

#new_bounding.dtype.names=('ts', 'x', 'y', 'w', 'h', 'class_id', 'confidence', 'track_id')
#print(new_bounding)

#np.save("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_v3/train/moorea_2019-06-26_test_02_000_1220500000_1280500000_bbox.npy",new_bounding)

#for e in [1000]:
#new_bounding=new_bounding[new_bounding["ts"]>=42300746]
#np.save("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_my_choice/done/moorea_2019-02-19_005_td_549500000_609500000_bbox.npy",new_bounding)
# for file in file_list:
    #if file.endswith('.npy'):
    #    new_bounding=np.load(path+file)
   #     new_bounding.dtype.names=('ts', 'x', 'y', 'w', 'h', 'class_id', 'confidence', 'track_id')
  #      for e in [1,2,3,4,5,6]:
 #           new_bounding=new_bounding[new_bounding["class_id"]!=e]
#        np.save("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/nagrania_do_przejrzenia/duzy_czlowiek/new_labels/"+file,new_bounding)

#print(bounding.dtype.names)
#print(bounding2.dtype.names)
#print(new_bounding[new_bounding["track_id"]==3042])
#w=new_bounding[new_bounding["track_id"]>=3107]
#print(df)
#index_names = df[(df.track_id==3082) & (df.ts>=18969330)].index
#df.drop(index_names,inplace=True)
#index_names = df[(df.track_id==3107) & (df.ts>=35084343) & (df.ts<=47078850)].index
#df.drop(index_names,inplace=True)
#new_bounding=np.asarray(df)
#print(new_bounding)
#np.save("/home/lsriw/pedestrian_detection_Mateusz_Kowalski/mini_dataset_check/val/moorea_2019-02-21_001_td_2318500000_2378500000_bbox.npy",new_bounding)
