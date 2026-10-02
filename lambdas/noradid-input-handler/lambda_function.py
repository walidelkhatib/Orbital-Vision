import json
import configparser
import requests
from tle2czml import tle2czml
from decimal import Decimal
from datetime import datetime, timedelta
import pytz


def lambda_handler(event, context):
    
    #1. Parse out query string params
    noradID = event['queryStringParameters']['noradID']
    print('noradID=' + noradID)

    #2. Construct the body of the response object
    uriBase = "https://www.space-track.org"
    requestLogin = "/ajaxauth/login"
    requestCmdAction = "/basicspacedata/query" 
    requestFindTle = "/class/tle_latest/NORAD_CAT_ID/"+noradID+"/orderby/ORDINAL asc/limit/1/format/3le/emptyresult/show"

    # Use configparser package to pull in the ini file (pip install configparser)
    config = configparser.ConfigParser()
    config.read("./SLTrack.ini")
    configUsr = config.get("configuration","username")
    configPwd = config.get("configuration","password")
    configOut = config.get("configuration","output")
    siteCred = {'identity': configUsr, 'password': configPwd}
    
    # run the session in a with block to force session to close if we exit
    with requests.Session() as session:

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            print("POST fail on login")

        # this query picks up TLE for the satellite based on the specified NORADID. Note - a 401 failure shows you have bad credentials 
        resp_sat = session.get(uriBase + requestCmdAction + requestFindTle)
        if resp_sat.status_code != 200:
            print(resp_sat)
            print("GET fail on TLE request for the specified satellite")    

        # define directories in temp for the .txt file and write content from api response
        with open('/tmp/'+'tle.txt', 'wb') as f:
            f.write(resp_sat.content)
        
        session.close()
        print("Completed session")
        
        start_time = (datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(hours=24))
        end_time = (datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(hours=48))
        
        # Get czml object using tle data from local storage and store the output locally
        tle2czml.create_czml('/tmp/tle.txt', start_time=start_time, end_time=end_time, outputfile_path= '/tmp/' + 'orbit.czml')     
        # Open and read the .czml file
        path_test = '/tmp/orbit.czml'
        with open(path_test, 'r') as myfile:
            data=myfile.read()
        obj = json.dumps(data)
        #obj = json.loads(data, parse_float=Decimal)

    
    #3. Construct response object
        responseObject = {}
        responseObject['statusCode'] = 200
        responseObject['headers'] = {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        }
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = obj
        #responseObject['body'] = str(obj).replace('\'','"') 
        
    
    #4. Return the response object
        try:
            return responseObject
        except Exception as e:
            if e.response['Error']['Code'] == "400":
                print("The object does not exist")
        else: 
            raise Exception('Unexpected Error')