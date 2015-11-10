#! /usr/bin/env python
#coding=utf-8

 

 ### the simple programe structure###
 ##version 1  by Frank Han at 2015/10/31##
import sys,time
import calendar as cal

def fun_get_url(PROJECT,TYPE,YEAR,MONTH):
    FORMAT = '%d-%d-%d'
    YEAR = int(YEAR)
    MONTH = int(MONTH)
    S_DATE = FORMAT %(YEAR,MONTH,1)
    E_DATE = FORMAT %(YEAR,MONTH,cal.monthrange(YEAR,MONTH)[1])
    API_URL = 'https://jira1.srv.volvo.com:8443/rest/api/2/search?maxResults=9999&jql='
    JQL = 'project in (%s)  AND issuetype in (%s)  AND status=Closed AND resolutiondate>=%s and resolutiondate<=%s ORDER BY Rank ASC' %(PROJECT,TYPE,S_DATE,E_DATE)
    URL = API_URL + JQL
    return URL


if __name__=='__main__':
        from optparse import OptionParser    
        parser = OptionParser()  
        parser.add_option("-p", "--project", dest="PROJECT",help="project name")  
        parser.add_option("-t", "--type", dest="TYPE",help="jira ticket type")
        parser.add_option("-y","--year",dest="YEAR",help="The year you want")
        parser.add_option("-m","--month",dest="MONTH",help="The month you want")
        (options, args) = parser.parse_args()
        

if None in [options.PROJECT,options.TYPE,options.YEAR,options.MONTH]:
    print "Error: Parameter is not correct \n"
    print "Usage: %s [options] \n" % sys.argv[0]
    print 'Try "%s -h" to get more tips' % sys.argv[0]
    exit()     
    

    


FULL_URL = fun_get_url(options.PROJECT,options.TYPE,options.YEAR,options.MONTH)
#print 'fun_get_url is %s' %FULL_URL
print 'program is trying to get data'
import requests

def fun_get_jira_data(FULL_URL):
    FULL_URL = fun_get_url(options.PROJECT,options.TYPE,options.YEAR,options.MONTH)
    USERNAME = 'james.huang'
    PASSWD = 'happydays'
    requests.packages.urllib3.disable_warnings()
    try:
        response=requests.get(FULL_URL,verify=False, auth=(USERNAME, PASSWD))
    except requests.exception.ConnectTimeout as e:
        print "Error: Failed to access/login Jira portal from your side. Please check"
        time.sleep(10)
        sys.exit(0)
    return response.json()['total']

FILENAME = "proj%s-%s-%s%s.txt" %(options.PROJECT,options.TYPE,options.YEAR,options.MONTH)
CASENUM = fun_get_jira_data(FULL_URL)
print CASENUM
print FILENAME

SAVE_FILE = open(FILENAME,'w')
SAVE_FILE.write(bytes(CASENUM))
SAVE_FILE.close()

print "job done!"
print "Please check the result in %s" % FILENAME
time.sleep(10)