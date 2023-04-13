from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view
import datetime
from collections import defaultdict
from django.db.models import Q
import time
import operator
from functools import reduce
from geopy.geocoders import Nominatim

def dt_funct():
    dict=defaultdict(list)
    return dict

def get_query(dict_query):
    query_start_time = time.time()
    #tutorials = Tutorial.objects.filter(Q(date__gte=dict_query['date1'])&Q(date__lte=dict_query['date2']))
    print(dict_query.keys())
    #l1=dict_query.keys() - ['date1','date2'] 
    for keyk in dict_query.keys() - ['date1','date2'] :
        print(keyk,dict_query[keyk])
    tutorials = Tutorial.objects.filter(**dict_query)

    tutorials= tutorials.values_list('state_name','district_name','count','lattitude','longitude')
    cnt1=0
    cnt2=0
    dict=defaultdict(dt_funct)
    for item in tutorials:
        if(len(dict[item[0]][item[1]])==0):
            dict[item[0]][item[1]].append(item[2])
            dict[item[0]][item[1]].append(item[3])
            dict[item[0]][item[1]].append(item[4])
        else:
            dict[item[0]][item[1]][0]=dict[item[0]][item[1]][0]+item[2]
        cnt1=cnt1+1
        cnt2=cnt2+item[2]
    print("---Finished querying db in %s seconds ---" % (time.time() - query_start_time))
    print('---Count of total records     = {0}---'.format(cnt1))
    print('---Count of total query count = {0}---'.format(cnt2))
    return dict


def get_column_names(str):
    query_start_time = time.time()
    tutorials = Tutorial.objects.values_list(str)
    st1 = set()
    cnt=0
    for item in tutorials:
        st1.add(item)
    print("---Finished querying db in %s seconds ---" % (time.time() - query_start_time))
    list1=[]
    for item in st1:
        list1.append(item)
        cnt+=1

    print('---Count of total unique enteries     = {0}---'.format(cnt))
    return list1

def get_max_cropORpest_state(colmn1,colmn1_val):
    colmn2='crop'
    if(colmn1=='crop'):
        colmn2='pest'
    tutorials = Tutorial.objects.filter(**{colmn1:colmn1_val})
    tutorials= tutorials.values_list(colmn2,'count')

    dict2=defaultdict(int)
    for item in tutorials:
        dict2[item[0]]+= item[1]
    
    colmn2_val=''
    for w in sorted(dict2, key=dict2.get, reverse=True):
        colmn2_val= w
        break
    print('\n////////// crop OR pest //////////')
    for w in sorted(dict2, key=dict2.get, reverse=True):
        print(w,dict2[w])

    tutorials2= Tutorial.objects.filter(Q( **{colmn1:colmn1_val})&Q(**{colmn2:colmn2_val}))
    tutorials2= tutorials2.values_list('state_name','count')

    dict2=defaultdict(int)
    for item in tutorials2:
        dict2[item[0]]+= item[1]
    
    state_nm=[]
    cnt=0
    for w in sorted(dict2, key=dict2.get, reverse=True):
        if(cnt==5):
            break
        state_nm.append(w)
        cnt+=1
    
    ans=[colmn2_val]
    print('\n////////// states //////////')
    for w in sorted(dict2, key=dict2.get, reverse=True):
        print(w,dict2[w])
    
    for item in state_nm:
        ans.append(item)
    return ans

def get_top5_cropORpest(str):
    query_start_time = time.time()
    tutorials = Tutorial.objects.filter(**{str+"__isnull":False})

    tutorials= tutorials.values_list(str,'count')
    qcnt=0
    dict1= defaultdict(int)
    for item in tutorials:
        qcnt+= item[1]
        dict1[item[0]]+=item[1]
    print("---Finished querying db in %s seconds ---" % (time.time() - query_start_time))
    print(dict1)
    dict2=defaultdict(float)

    i=0
    for item in sorted(dict1, key=dict1.get, reverse=True):
        if(i==5):
            break
        dict2[item]= dict1[item]/qcnt*100
        i+=1
    return dict2

def get_location(Latitude ,Longitude):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(Latitude+","+Longitude)

        address = location.raw['address']

        # traverse the data
        return address.get('state', '')