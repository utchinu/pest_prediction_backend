from django.shortcuts import render

from django.http.response import JsonResponse
from django.http.response import HttpResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view
from tutorials.utils import  get_query,get_column_names,get_max_cropORpest_state,get_top5_cropORpest, get_location
import datetime
from collections import defaultdict
from django.db.models import Q
import time
from tutorials.codeUtil2 import predict_pest


@api_view(['GET','POST'])
def chatbot_general_query(request):
    if(request.method=='GET'):
        qname= request.GET.get('crop',None)
        if(qname!=None):
            return JsonResponse( get_top5_cropORpest('crop'), safe=False)

        qname= request.GET.get('pest',None)
        if (qname!=None):
            return JsonResponse( get_top5_cropORpest('pest'), safe=False)
            
        else:
            return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def chatbot_specific_query(request):
    if(request.method=='GET'):
        qname= request.GET.get('crop',None)
        if(qname!=None):
            return JsonResponse( get_max_cropORpest_state('crop',qname), safe=False)

        qname= request.GET.get('pest',None)
        if (qname!=None):
            return JsonResponse( get_max_cropORpest_state('pest',qname), safe=False)
            
        else:
            return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def column_names(request):
    if(request.method=='GET'):
        list1= ['crop','pest','state_name','district_name']
        for item in list1:
            str=request.GET.get(item,None)
            if (str!=None):
                str=item
                break;
        if(str==None):
            return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)
        print("column",str)
        list_l1= get_column_names(str)
        list_l1=sorted(list_l1)
        return JsonResponse(list_l1,safe=False)

@api_view(['GET','POST'])
def district_of_state(request):
    if(request.method=='GET'):
        return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def prediction(request):
    if request.method=='GET':
        stName = request.GET.get('state_name', None)
        pestName = request.GET.get('pest', None)

        if (stName == None or pestName == None):
                return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)
        x_axis, y_axis, upper_bnd, lower_bnd = predict_pest(pestName, stName)
        if (x_axis == -1):
                return HttpResponse("No query for this combo in dataset", status=status.HTTP_400_BAD_REQUEST)
        dict1 = {'x_axis': x_axis, 'y_axis': y_axis, 'upper_bnd': upper_bnd, 'lower_bnd': lower_bnd}
        return JsonResponse(dict1,safe=False)

@api_view(['GET','POST'])
def user_location(request):
    if request.method=='GET':
        Latitude = request.GET.get('Latitude', None)
        Longitude = request.GET.get('Longitude', None)

        if (Latitude == None or Longitude == None):
                return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)
        state_name = get_location(Latitude, Longitude)
        dict1 = {"state_name": state_name}
        return JsonResponse(dict1,safe=False)


@api_view(['GET','POST'])
def home_page(request):
    if request.method=='GET':
        dict={}
        dict['date__gte']= request.GET.get('date1', None)
        dict['date__lte']= request.GET.get('date2', None)
        dict['crop']=  request.GET.get('crop', None)
        dict['pest']=  request.GET.get('pest', None)
        dict['state_name']= request.GET.get('state_name', None)
        dict['district_name']= request.GET.get('district_name', None)

        dict2={}
        flag=0
        for item in dict.items():
            print(item[1])
            if (item[1]!="all"):        #important
                dict2[item[0]]=item[1]
            if (item[1]==None):
                flag=1
                break
        print(flag)
        if(flag==1):
            return HttpResponse("HTTP_400_BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)
        dict= get_query(dict2)
        return JsonResponse(dict,safe=False)

def dt_funct():
    dict=defaultdict(int)
    return dict

@api_view(['GET', 'POST'])
def tutorial_list_1(request):
    if request.method == 'GET':
        print("///////////////////////////////")
        check()
        title = request.GET.get('date1', None)
        title1 = request.GET.get('date2', None)
        print(title1)
        if title is not None:
            print("true")
            query_start_time = time.time()

            tutorials = Tutorial.objects.filter(Q(date__gte=title)&Q(date__lte=title1)).values_list('state_name','district_name','count')
            cnt1=0
            cnt2=0
            dict=defaultdict(dt_funct)
            for item in tutorials:
                print(item)
                dict[item[0]][item[1]]=dict[item[0]][item[1]]+item[2]
                cnt1=cnt1+1
                cnt2=cnt2+item[2]
            print("---Finished querying db in %s seconds ---" % (time.time() - query_start_time))
            print(cnt1)
            print(cnt2)
            return JsonResponse(dict,safe=False)
        else:
            tutorials= Tutorial.objects.all()
        tutorials_serializer = TutorialSerializer(tutorials,many=True)
        print(tutorials_serializer.data[0])
        return JsonResponse(tutorials_serializer,safe=False)


    if request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        print(tutorial_data['date'])
        tutorial_data['date'] = datetime.datetime.strptime(tutorial_data['date']+"T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        print(tutorial_data['date'])
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            print("inside")
            #return JsonResponse(tutorial_serializer.validated_data)
            return HttpResponse(tutorial_serializer.data['date'])
        else:
            print(tutorial_serializer.errors)
            return HttpResponse("yo mannn  ")
    
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        tutorial = Tutorial.objects.get(pk=pk) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE tutorial
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    # GET all published tutorials