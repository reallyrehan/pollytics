import datetime
from datetime import timedelta  
from time import sleep
import sys
import requests
import json
import os
import pickle




def logger(txt):
    ans = str(datetime.datetime.now())+" "+str(txt)+"\n"

    with open("logs.txt", "a+") as myfile:
        myfile.write(ans)

def meth():
    try:
        if 'startDate.pickle' in os.listdir():
            print("Reading from file")
            logger("Reading from file")
            f=open("startDate.pickle","rb")
            initialDate=pickle.load(f)
            f.close()
        else:
            print("initializing date from 2019-12-31")
            logger("initializing date from 2019-12-31")

            initialDate=datetime.datetime(2019,12,31,0,0)
        endDate = initialDate+timedelta(days=1)
        users = ['trump','biden']
        ansDict = {}
        timer=2

        dayCount=0
        errorList=[]
        successList=[]





        for dayCount in range(0,20):
            ans = ""
            startDate = initialDate+timedelta(days=dayCount)
            endDate = startDate+timedelta(days=1)

            start=str(round(startDate.timestamp()))
            end = str(round(endDate.timestamp()))
            ans = ans + start+"\n"
            print(start)
            print(str(startDate))
            ans = ans +str(startDate)+"\n"

            ansDict[start]={}
            for user in users:
                ansDict[start][user]={}
                ans = ans + str(user)+"\n"
                print(user,end=" ")
                urlDict= {
                    "submission" : 'https://api.pushshift.io/reddit/search/submission/?q='+user+'&after='+start+'&before='+end+'&size=100&sort=asc',
                    "comment" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&size=100&sort=asc',
                    "created_agg" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&aggs=created_utc&frequency=hour&size=0',
                    "subreddit_agg" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&aggs=subreddit&size=0',
                    "link_agg" : 'https://api.pushshift.io/reddit/search/comment/?q='+user+'&after='+start+'&before='+end+'&aggs=link_id&size=0'}

                for url in urlDict:
                    ans = ans + str(url)+"\n"
                    print(url,end = " ")
                    try:
                        r = requests.get(urlDict[url], headers = {'User-agent': 'your bot 0.1'})
                    except:
                        ans = ans + "Error in TIME:"+start+"\nURL:"+url+"\nExiting\n"
                        print("Error in TIME:"+start+"\nURL:"+url+"\nExiting\n")
                        logger(ans)
                        
                        f=open("startDate.pickle","wb")
                        pickle.dump(initialDate+timedelta(days=dayCount),f)
                        f.close()
                        sys.exit()
                        
                    ansDict[start][user][url]=r.json()
                        
            print()
                    
            f=open('backup/'+start+'.json','w+')
            f.write(json.dumps(ansDict[start],indent=2))
            f.close()
            print("Sleeping for "+str(timer)+"seconds", end = '', flush = True)
            ans = ans +"Sleeping for "+str(timer)+"seconds"+"\n"
            time.sleep(timer)
            print("Resumed")
            ans = ans + "Resumed"+"\n"
            
            # try:
            result_message = requests.put('https://data-management-ac8c8.firebaseio.com/'+start+'.json',json.dumps(ansDict[start]))
            print("Success "+start)
            ans = ans + "Success "+start+"\n"
            successList.append(start)

            # except:
            #     errorList.append(start)

            #     ans = ans + "Error in "+str(dayCount)+"\n"
            #     print("Error in "+str(dayCount))
            
            



        f=open("startDate.pickle","wb")
        pickle.dump(initialDate+timedelta(days=dayCount),f)
        f.close()
        return True
    except:
        f=open("startDate.pickle","wb")
        pickle.dump(initialDate+timedelta(days=dayCount),f)
        f.close()
        errorList.append(start)

        ans = ans + "Error in "+str(dayCount)+"\n"
        print("Error in "+str(dayCount))

        return False
    finally:
        logger(ans)


c= 0 

while c<40:
    c=c+1
    
    if meth():
        print("Sleeping for 60", end = '', flush = True)
        sleep(60)
    else:
        print("Error, sleeping for 30")
        sleep(30)