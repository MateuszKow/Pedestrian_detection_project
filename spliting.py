import os
import shutil

if __name__ == '__main__':
    path="/home/lsriw/pedestrian_detection_Mateusz_Kowalski/prophesee-automotive-dataset-toolbox/sae/val/"
    os.chdir(path)
    dat_list=[file[:-4] for file in os.listdir("images") ]
    lista_5485=[]
    lista_4265=[]
    lista_23785=[]
    lista_9145=[]
    dsf_list=[file[:-4] for file in os.listdir("labels") ]
    #dat_list=["moorea_2019-06-21_000_854500000_914500000_td.dat"]
    #boxes_list = [glob(td_file.split('_td.dat')[0] +  '*.npy')[0] for td_file in dat_list]
    #w=list(set(dsf_list)-set(dat_list))
    #os.chdir("images")
   # for file in w:
   #     file=file+".png"
   #     os.remove(file)
    for file in dat_list:
        if file[:40]=="moorea_2019-02-21_001_td_488500000_54850":
            lista_5485.append(file)
        elif file[:40]=="moorea_2019-06-14_001_366500000_42650000":
            lista_4265.append(file)
        elif file[:40]=="moorea_2019-02-21_001_td_2318500000_2378":
            lista_23785.append(file)
        elif file[:40]=="moorea_2019-06-21_000_854500000_91450000":
            lista_9145.append(file)
    print(len(lista_23785))
    a=lista_23785
    for i in range(len(a)):
        if i%5==0 :
           #print(lista_5485[i],glob("labels/"+lista_5485[i]+".txt"))
            shutil.move("images/"+a[i]+".png","test_im2/"+a[i]+".png")
            shutil.move("labels/"+a[i]+".txt","test_lab2/"+a[i]+".txt")