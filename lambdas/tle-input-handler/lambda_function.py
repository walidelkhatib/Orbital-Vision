import json
import tle2czml
from decimal import Decimal
import os
from datetime import datetime, timedelta
import pytz


def lambda_handler(event, context):
    #1. Parse out query string params
    # satelliteName = event['satelliteName']
    # tle1 = event['tle1']
    # tle2 = event['tle2']
    satelliteName = event['queryStringParameters']['satelliteName']
    tle1 = event['queryStringParameters']['tle1']
    tle2 = event['queryStringParameters']['tle2']

    
    print('satelliteName=' + satelliteName)
    print('tle1=' + tle1)
    print('tle2=' + tle2) 

    if os.path.exists('/tmp/tle.txt'):
        os.remove('/tmp/tle.txt')
    
    #2. Construct the body of the response object
    start_time = (datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(hours=24))
    end_time = (datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(hours=48))
    
    with open('/tmp/tle.txt', 'a') as tle_file:
        tle_file.write(satelliteName + '\n') 
        tle_file.write(tle1 + '\n')
        tle_file.write(tle2)
        tle_file.close()
    tle2czml.create_czml('/tmp/tle.txt', start_time=start_time, end_time=end_time, outputfile_path= '/tmp/' + 'orbit.czml')     #Get czml object using tle data from local storage and store the output locally
    
    
    path_test = '/tmp/orbit.czml'
    with open(path_test, 'r') as myfile:                   #open and read the .czml file
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
    
    
    #4. Return the response object
    #return responseObject
    try:
        return responseObject
        #return responseObject['headers']
        #return responseObject['body']
    except Exception as e:
        if e.response['Error']['Code'] == "400":
            print("The object does not exist")
    else: 
        raise Exception('TLE Format Error')