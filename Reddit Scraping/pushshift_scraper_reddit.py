import datetime
from datetime import timedelta  
import time
import sys
import requests
import json
import os
import pickle




def logger(txt):
    ans = str(datetime.datetime.now())+" "+str(txt)+"\n"

    print(ans)

    with open("logs.txt", "a+") as myfile:
        myfile.write(ans)



def readStartDate():
    if 'startDate.pickle' in os.listdir():
            
        logger("Reading from file")
        f=open("startDate.pickle","rb")
        dt=pickle.load(f)
        f.close()

    return dt


def mainMethod(initialDate,timer):
    
    try:
        


        endDate = initialDate+timedelta(days=1)

        users = ['trump','biden']
        ansDict = {}


        dayCount=0
        errorList=[]
        successList=[]



        for dayCount in range(0,20):

            startDate = initialDate+timedelta(days=dayCount)
            endDate = startDate+timedelta(days=1)

            start=str(round(startDate.timestamp()))
            end = str(round(endDate.timestamp()))

            logger("Start: "+start)
            logger("Start Date: "+str(startDate))
 

            ansDict[start]={}

            for user in users:
                ansDict[start][user]={}


                logger(user)
                urlDict= {
                    "submission" : 'https://api.pushshift.io/reddit/search/submission/?q='+user+'&after='+start+'&before='+end+'&size=100&sort=asc',
                    "comment" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&size=100&sort=asc',
                    "created_agg" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&aggs=created_utc&frequency=hour&size=0',
                    "subreddit_agg" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&aggs=subreddit&size=0',
                    "link_agg" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&aggs=link_id&size=0'}

                for url in urlDict:

                    logger(url)
                    r = requests.get(urlDict[url], headers = {'User-agent': 'your bot 0.1'})
                        
                    ansDict[start][user][url]=r.json()
                        
                    
            f=open('backup/'+start+'.json','w+')
            f.write(json.dumps(ansDict[start],indent=2))
            f.close()

            logger("Sleeping for "+str(timer)+"seconds")
            time.sleep(timer)
            print("#", end = '', flush = True)


            logger("Resumed")
            
            
            result_message = requests.put('https://data-management-ac8c8.firebaseio.com/'+start+'.json',json.dumps(ansDict[start]))
            print("Success "+start)
            ans = ans + "Success "+start+"\n"
            successList.append(start)

            

            ans = ans + "Error in "+str(dayCount)+"\n"
            logger("Error in "+str(dayCount))
            
            logger(ans)

            f=open("startDate.pickle","wb")
            pickle.dump(initialDate+timedelta(days=dayCount),f)
            f.close()

    
    except Exception as e:
        logger(str(e))
        logger("Error in TIME:"+start+"\nURL:"+url+"\nExiting\n")


    finally:
        f=open("startDate.pickle","wb")
        pickle.dump(initialDate+timedelta(days=dayCount),f)
        f.close()
        sleep(60)
        print("#", end = '', flush = True)



import sys

c=1
while c<40:
    c=c+1
    print(c)
    if len(sys.argv)>1:
        xv = sys.argv[1].split('_')
        initialDate = datetime.datetime(xv[0],xv[1],xv[2])
    else:
        initialDate = readStartDate();

    mainMethod(initialDate,5)
    logger("Sleeping for 60")
    time.sleep(60)
