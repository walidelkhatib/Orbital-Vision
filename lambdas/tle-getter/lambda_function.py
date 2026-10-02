import os
import boto3
import requests
import configparser

def lambda_handler(event, context):
    uriBase = "https://www.space-track.org"
    requestLogin = "/ajaxauth/login"
    requestCmdAction = "/basicspacedata/query" 
    requestFindTleAQUA = "/class/tle_latest/NORAD_CAT_ID/27424/orderby/ORDINAL asc/limit/1/format/3le/emptyresult/show"
    requestFindTleSNPP = "/class/tle_latest/NORAD_CAT_ID/37849/orderby/ORDINAL asc/limit/1/format/3le/emptyresult/show"
    requestFindTleNOAA = "/class/tle_latest/NORAD_CAT_ID/43013/orderby/ORDINAL asc/limit/1/format/3le/emptyresult/show"

    # Use configparser package to pull in the ini file (pip install configparser)
    config = configparser.ConfigParser()
    config.read("./SLTrack.ini")
    configUsr = config.get("configuration","username")
    configPwd = config.get("configuration","password")
    configOut = config.get("configuration","output")
    siteCred = {'identity': configUsr, 'password': configPwd}

    # Define the S3 bucket resource and desired output keys for each tle.txt file
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('orbital-vision-data-and-code')
    out_key_aqua = 'tle_aqua.txt'
    out_key_snpp = 'tle_snpp.txt'
    out_key_noaa = 'tle_noaa.txt'
    
    # run the session in a with block to force session to close if we exit
    with requests.Session() as session:

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            print("POST fail on login")

        # this query picks up TLE for AQUA. Note - a 401 failure shows you have bad credentials 
        resp_aqua = session.get(uriBase + requestCmdAction + requestFindTleAQUA)
        if resp_aqua.status_code != 200:
            print(resp_aqua)
            print("GET fail on TLE request for satellite AQUA")
            
        # this query picks up TLE for SNPP. Note - a 401 failure shows you have bad credentials 
        resp_snpp = session.get(uriBase + requestCmdAction + requestFindTleSNPP)
        if resp_snpp.status_code != 200:
            print(resp_snpp)
            print("GET fail on TLE request for satellite SNPP")
            
        # this query picks up TLE for NOAA. Note - a 401 failure shows you have bad credentials 
        resp_noaa = session.get(uriBase + requestCmdAction + requestFindTleNOAA)
        if resp_noaa.status_code != 200:
            print(resp_noaa)
            print("GET fail on TLE request for satellite NOAA")
    
        # define directories in temp for each .txt file and write content from api response
        with open('/tmp/'+'tle_aqua.txt', 'wb') as f:
            f.write(resp_aqua.content)
        with open('/tmp/'+'tle_snpp.txt', 'wb') as f:
            f.write(resp_snpp.content)
        with open('/tmp/'+'tle_noaa.txt', 'wb') as f:
            f.write(resp_noaa.content)
        
        # upload each .txt file to S3
        bucket.upload_file('/tmp/tle_aqua.txt', 'tle-data-V2/aqua/'+out_key_aqua)
        bucket.upload_file('/tmp/tle_snpp.txt', 'tle-data-V2/snpp/'+out_key_snpp)
        bucket.upload_file('/tmp/tle_noaa.txt', 'tle-data-V2/noaa/'+out_key_noaa)

        session.close()
            
    print("Completed session")
