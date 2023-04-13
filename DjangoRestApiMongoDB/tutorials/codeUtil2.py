from pymongo import MongoClient
from pprint import pprint
import datetime
import time
from random import sample
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view
import datetime
from collections import defaultdict
from django.db.models import Q
import time
import operator
from functools import reduce

#db cred
client = MongoClient(port=27017)
db_name="test1"
db=client[db_name]

def exponential_smoothing(series, alpha):
    """
        series - dataset with timestamps
        alpha - float [0.0, 1.0], smoothing parameter
    """
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def plotExponentialSmoothing(x_axis,series, alphas):
    """
        Plots exponential smoothing with different alphas
        
        series - dataset with timestamps
        alphas - list of floats, smoothing parameters
        
    """
    series= pd.Series(series)
    with plt.style.context('seaborn-white'):    
        plt.figure(figsize=(15, 7))
        #for alpha in alphas:
            #plt.plot(x_axis,exponential_smoothing(series, alpha), label="Alpha {}".format(alpha))
        #plt.plot(x_axis,series, "c", label = "Actual")
        plt.legend(loc="best")
        plt.axis('tight')
        plt.title("Exponential Smoothing")
        plt.xticks(rotation=270)
        plt.ylabel('count per month',fontsize=14)
        plt.grid(True)

def moving_average(series, n):    
    return np.average(series[-n:])

def plotMovingAverage(x_axis,series, window, plot_intervals=False, scale=1.96, plot_anomalies=False):

    """
        series - dataframe with timeseries
        window - rolling window size 
        plot_intervals - show confidence intervals
        plot_anomalies - show anomalies 

    """
    series= pd.Series(series)
    rolling_mean = series.rolling(window=window).mean()
    y_axis=[]
    #print(rolling_mean)
    for item in rolling_mean:
        y_axis.append(item)
    #plt.figure(figsize=(15,5))
    #plt.title("Moving average\n window size = {}".format(window))
    #plt.plot(x_axis,y_axis, "g", label="Rolling mean trend")
    
    if plot_intervals:
        print('heelo')
        mae = mean_absolute_error(series[window:], rolling_mean[window:])
        deviation = np.std(series[window:] - rolling_mean[window:])
        lower_bond = rolling_mean - (mae + scale * deviation)
        upper_bond = rolling_mean + (mae + scale * deviation)
        #plt.plot(upper_bond, "r--", label="Upper Bond / Lower Bond")
        #plt.plot(lower_bond, "r--")
    #plt.show()


def fill_inBetween(prev_m, prev_year, month, year, x_axis, y_axis ):
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',]
    prev_m+=1
    if(prev_m==13):
        prev_year= (str)((int)(prev_year)+1)
        prev_m=1
    
    while(prev_year!=year):
        x_axis.append(month_names[prev_m-1]+'-'+prev_year)
        y_axis.append(0) 
        print(month_names[prev_m-1]+'-'+prev_year+'----',0)
        if(prev_m==12):
            prev_m=1
            prev_year= (str)((int)(prev_year)+1)
        prev_m+=1

        
    while(prev_m<(month)):
        x_axis.append(month_names[prev_m-1]+'-'+year)
        y_axis.append(0) 
        print(month_names[prev_m-1]+'-'+year+'----',0)
        prev_m+=1




def plot_graph_all(field_name1,field_value1,field_name2,field_value2,query_type_flag):
    '''user_st_name= '_'    #state
    user_pest_name= 'Paddy (Dhan)'    #crop'''
    user_interval=[3,4,6,12]

    end =   datetime.datetime.strptime("2016-12-31"+"T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")     #last date
    last_year=2016
    
    dict_query = {'date__lte':end, 'state_name':field_value1, 'pest': field_value2}
    query1= Tutorial.objects.filter(**dict_query)
    query1= query1.values_list('date','count')
    if(len(query1) == 0):
            return -1,-1
    cnt=0
    prev_m=1
    prev_year="2013"    
    x_axis=[]
    y_axis=[]
    flag=0
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',]
    per_month_total_count={str(val): ([0 for i in range (12)]) for val in range (2013,last_year+1) }
    for obj in query1:
        #print("inside")
        #print(obj)
        month= (int)(obj[0].strftime("%m"))
        year= (obj[0].strftime("%Y"))
        if(flag==0):
            while(prev_m<(month)):
                x_axis.append(month_names[prev_m-1]+'-'+year)
                y_axis.append(cnt) 
                per_month_total_count[prev_year][prev_m-1]+=cnt
                print(month_names[prev_m-1]+'-'+year+'----',cnt)
                prev_m+=1
            flag=1


        if(month!=prev_m):
            x_axis.append(month_names[prev_m-1]+'-'+prev_year)
            y_axis.append(cnt)
            per_month_total_count[prev_year][prev_m-1]+=cnt
            print(month_names[prev_m-1]+'-'+prev_year+'----',cnt)
            cnt=0
            fill_inBetween(prev_m, prev_year, month, year, x_axis, y_axis)
            cnt=obj[1]

        else:
            cnt+=obj[1]
        prev_m=month
        prev_year= year
    print("here")
    x_axis.append(month_names[prev_m-1]+'-'+prev_year)
    y_axis.append(cnt)
    per_month_total_count[prev_year][prev_m-1]+=cnt
    print(month_names[prev_m-1]+'-'+prev_year+'----',cnt)
    cnt=0
    prev_m+=1
    while(prev_m<=12):
        x_axis.append(month_names[prev_m-1]+'-'+prev_year)
        y_axis.append(cnt) 
        per_month_total_count[prev_year][prev_m-1]+=cnt
        print(month_names[prev_m-1]+'-'+prev_year+'----',cnt)
        prev_m+=1



    if(query_type_flag==0):      
        alpha_val=0.75
        test_list= [0 for i in range (12)]
        for i in range (12):

            val= per_month_total_count["2013"][i]
            for cur_year in range(2014,last_year+1):                
                val=(alpha_val * per_month_total_count[str(cur_year-1)][i] + (1 - alpha_val) * val)
                #val+= per_month_total_count[str(cur_year)][i]

            print(month_names[i]+'-2019----',val)
            test_list[i]=val
            #test_list[i]= (val-per_month_total_count[str(last_year)][i])/(last_year-2013)
        return x_axis,y_axis,test_list
    
    #fig,ax=plt.subplots(figsize=(16,9))
    if(field_value1==field_value2 and query_type_flag==1):
        for i in range(len(user_interval)):
            plt.figure(figsize=(16,9))
            #plt.plot(x_axis, y_axis)    

            plt.xticks(rotation=270)
            plt.title(field_value2+'/'+'-interval='+str(user_interval[i])+'months')
            plt.ylabel('count per month',fontsize=14)
            #plt.savefig(user_st_name+'-'+user_pest_name+'.png')
            plt.grid(True)
            #print(moving_average(y_axis, 12))
            plotMovingAverage(x_axis,y_axis, user_interval[i]) 
            #plt.savefig(user_st_name+'-'+user_pest_name+'-'+'-interval='+str(user_interval)+'months'+'.png')
            #plt.savefig('./'+field_value2+'/'+'-interval='+str(user_interval[i])+'months'+'.png')
            plt.clf()
        plotExponentialSmoothing(x_axis,y_axis, [0.3, 0.05])
        #plt.savefig('./'+field_value2+'/'+'ExponentialSmoothing'+'.png')
        plt.clf()
    return x_axis,y_axis

def get_crops_for_pest():
    pest_name= 'aphid'
    crop_top= my_funct(pest_name)
    plt.figure(figsize=(16,9))
    x_axis,y_axis=plot_graph_all('pest',pest_name,'pest',pest_name,1)
    plt.plot(x_axis,y_axis,label=pest_name)

    for item in crop_top:
        if(item[1]>=5):
            print(item[0],item[1])
            x_axis,y_axis=plot_graph_all('crop',item[0],'pest',pest_name,1)
            plt.plot(x_axis,y_axis, label=item[0])

    plt.legend(loc="upper left")
    plt.xticks(rotation=270)
    plt.ylabel('count per month',fontsize=14)
    plt.grid(True)
    #plt.show()
    plt.savefig('./'+pest_name+'/'+'top_crop_trends'+'.png')


def predict_pest(pest_name, st_name):
        last_year=2016

        #x_axis,y_axis,test_list=plot_graph_all('pest',pest_name,'pest',pest_name,0)

        upper_bnd, lower_bnd = list(), list()

        
        print(pest_name, st_name)
        x_axis,y_axis=plot_graph_all('state_name',st_name,'pest',pest_name,1)
        if (x_axis == -1):
                return -1,-1,-1,-1
        list_rand = [5, 7.5, 10, 12.5, 15, -5, -7.5, -10, -12.5, -15]

        y_temp = list()

        for val in range(12, 0, -1):
                rnd =   sample(list_rand, 1)
                tmp = (y_axis[-(val)] * 0.60 + y_axis[-(val) - 12] * 0.40 )
                y_temp.append(tmp + (tmp * (rnd[0]) / 100) )
        
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',]
        for i in range(12):
                y_axis.append(y_temp[i])
                x_axis.append(month_names[i]+'-'+'2017')
        
        list_rand2 = [2.5, 5, 7.5, 10]
        for val in y_axis[-12:]:
                rnd =   sample(list_rand2, 1)
                upper_bnd.append(val + (val * (rnd[0]) / 100))
                lower_bnd.append(val - (val * (rnd[0]) / 100))


        print("//////////////////")
        print(x_axis)
        print(upper_bnd)
        print(y_axis)
        print(lower_bnd)
        return x_axis, y_axis, upper_bnd, lower_bnd
        '''
        #plt.plot(x_axis[:(12*(last_year-2013))+1],y_axis[:(12*(last_year-2013))+1], label="train")
        #plt.plot(x_axis[(12*(last_year-2013)):],y_axis[(12*(last_year-2013)):], label="original")
        #plt.plot(x_axis[(12*(last_year-2013)):],test_list, label="test")
        plt.plot(x_axis, y_axis, label = "original")
        plt.plot(x_axis[-12:], upper_bnd, label = "upper_bnd")
        plt.plot(x_axis[-12:], lower_bnd, label = "lower_bnd")
        #plt.plot(x_axis,y_axis,label=pest_name)
        plt.legend(loc="upper left")
        plt.xticks(rotation=270)
        plt.ylabel('count per month',fontsize=14)
        plt.grid(True)
        #plt.savefig('./'+pest_name+'/'+'test_train1'+'.png')
        plt.show()
        '''
if __name__ == "__main__":
    #get_crops_for_pest()
    predict_pest()

