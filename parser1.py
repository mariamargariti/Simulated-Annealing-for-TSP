import pandas as pd
import numpy as np

cities_dict={}
data = r"C:\Users\maria\FinalProject-Maria Margariti\a280.tsp"

#anoigw to arxeio kai typwnw tis plirofories, afairw ta kena me th methodo strip()
def read_tsp_data(tsp_name):
    with open(tsp_name) as f:
        content=f.read().splitlines()
        info=[x.lstrip() for x in content if x != ""]
        for item in info:
            if 'NAME' in item.split():
                print(item)
            if 'COMMENT' in item.split():
                print(item)
            if 'TYPE' in item.split():
                print (item)
            if 'DIMENSION' in item.split():
                print (item)
            if 'EDGE_WEIGHT_TYPE' in item.split():
                print (item)    
        return info
    
    #elegxw an to prwto stoixeio einai arithmos
    #an einai arithmos me th methodo split() dimiourgw th lista kai krataw to prwto stoixeio
    #to ekxwrw ws key sto cities me values ta alla dyo stoixeia tis listas(kathe polh einai ena key)
    #elegxw gia kena kai ta afairw    
def dict(ct):
    cities={}
    index=0
    for item in ct:
        if (item.split(' ')[0].isdigit()):
            cities[int(ct[index].split(' ')[0])]=ct[index].split(' ')[1:]
            index=index+1
        else:
            index=index+1
            continue 
    for key in cities:
        if '' in cities[key]:
            cities[key]=list(filter(lambda x: x != '', cities[key]))
    return cities 

#ypologizei tin apostash metaksy dyo polewn
def find_diff(c1, c2):
    if c1 in cities_dict and c2 in cities_dict:
        x_diff=(int(cities_dict[c1][0]) - int(cities_dict[c2][0]))**2
        y_diff=(int(cities_dict[c1][1]) - int(cities_dict[c2][1]))**2
        diff=np.sqrt(x_diff + y_diff)
        return (diff)

    #ypologizei tin apostash kathe polis me oles tis ypoloipes
    #eisagei tis apostaseis se enan pandas dataframe 
def find_all_differences(cities_dict):
    differences={}
    diff_temp=[]
    for key in cities_dict:
        for key_2 in cities_dict:
            x_diff=abs((int(cities_dict[key][0]) - int(cities_dict[key_2][0]))**2)
            y_diff=abs((int(cities_dict[key][1]) - int(cities_dict[key_2][1]))**2)
            diff=np.sqrt(x_diff + y_diff)
            diff_temp.append(diff)
        differences[key]=diff_temp 
        diff_temp=[]
    distances=pd.DataFrame.from_dict(differences)
    return distances

    #kalw tis sunarthseis kai typwnw ta apotelesmata
def built_all(data):
    data_file=read_tsp_data(data)      
    global cities_dict 
    cities_dict=dict(data_file)
    diff=find_all_differences(cities_dict)
    #print(diff)
    return cities_dict

#built_all(data)


    #vriskei tis apostaseis pou epilegei o xrhsths an aytes vriskontai sto lexiko
    #o xrhsths epilegei an tha synexisei h' oxi
"""
while True:
    city_1 = int(input('Give city_1 '))
    city_2 = int(input('Give city_2 '))
    
    if city_1 in cities_dict.keys() and city_2 in cities_dict.keys():
        print(find_diff(city_1, city_2))   
        ans = input('Do you want to continue? Give "y" for yes or "n" for no: ')
    else:
        print('Give keys again ')
        continue
    
    if ans == 'y':
        continue
    else:
        break
"""             