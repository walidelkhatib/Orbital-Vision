import os
import boto3
import tle2czml
from datetime import datetime, timedelta
import pytz

    
def lambda_handler(event,context):
    
    s3 = boto3.resource('s3')                                               #define the S3 SDK resource
    bucket = s3.Bucket('orbital-vision-data-and-code')                      #define the S3 bucket
    
    in_key_aqua = 'tle-data-V2/aqua/tle_aqua.txt'                           #define key of tle data for AQUA in s3
    in_key_noaa = 'tle-data-V2/noaa/tle_noaa.txt'                           #define key of tle data for NOAA in s3
    in_key_snpp = 'tle-data-V2/snpp/tle_snpp.txt'                           #define key of tle data for SNPP in s3
    
    #start_time=(datetime.today() - timedelta(days=2))                     #define start time for orbit 
    #end_time=(datetime.today() + timedelta(days=2))                         #define end time for orbit
    start_time = (datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(hours=24))
    end_time = (datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(hours=48))


    for record in event['Records']:
        key = record['s3']['object']['key']
    
    if key == in_key_aqua:                                                  #if function triggered from S3 PUT of AQUAA tle data
        local_tle_dir = '/tmp/' + 'tle_aqua.txt'                            #define where tle data for AQUA will be temporarily stored
        bucket.download_file(in_key_aqua, local_tle_dir)                    #download AQUA's tle data from s3 to local storage
        tle2czml.create_czml('/tmp/'+'tle_aqua.txt', start_time=start_time, end_time=end_time, outputfile_path= '/tmp/' + 'orbit_aqua.czml')    
        #tle2czml.create_czml('/tmp/'+'tle_aqua.txt', outputfile_path= '/tmp/' + 'orbit_aqua.czml')     #Get AQUA's czml object using tle data from local storage and store the output locally
        path_test = '/tmp/orbit_aqua.czml'                                  #define path to access the AQUA's czml object saved in temp storage
        out_key = 'Orbits_aqua.czml'                                        #define output key for AQUA's czml object
        bucket.upload_file(path_test, 'outputs-V2/aqua/' + out_key)         #upload AQUA's czml object to S3 bucket
        return("AQUA's Orbit File Was Uploaded Successfully")


    if key == in_key_noaa:                                                  #if function triggered from S3 PUT of NOAA tle data
        local_tle_dir = '/tmp/' + 'tle_noaa.txt'                            #define where tle data for NOAA will be temporarily stored
        bucket.download_file(in_key_noaa, local_tle_dir)                    #download NOAA's tle data from s3 to local storage
        tle2czml.create_czml('/tmp/'+'tle_noaa.txt', start_time=start_time, end_time=end_time, outputfile_path= '/tmp/' + 'orbit_noaa.czml')
        #tle2czml.create_czml('/tmp/'+'tle_noaa.txt', outputfile_path= '/tmp/' + 'orbit_noaa.czml')     #Get NOAA's czml object using tle data from local storage and store the output locally
        path_test = '/tmp/orbit_noaa.czml'                                  #define path to access the NOAA's czml object saved in temp storage
        out_key = 'Orbits_noaa.czml'                                        #define output key for NOAA's czml object
        bucket.upload_file(path_test, 'outputs-V2/noaa/' + out_key)         #upload NOAA's czml object to S3 bucket
        return("NOAA's Orbit File Was Uploaded Successfully")
        
        
    if key == in_key_snpp:                                                  #if function triggered from S3 PUT of NOAA tle data
        local_tle_dir = '/tmp/' + 'tle_snpp.txt'                            #define where tle data for SNPP will be temporarily stored
        bucket.download_file(in_key_snpp, local_tle_dir)                    #download NOAA's tle data from s3 to local storage
        tle2czml.create_czml('/tmp/'+'tle_snpp.txt', start_time=start_time, end_time=end_time, outputfile_path= '/tmp/' + 'orbit_snpp.czml')
        #tle2czml.create_czml('/tmp/'+'tle_snpp.txt', outputfile_path= '/tmp/' + 'orbit_snpp.czml')     #Get NOAA's czml object using tle data from local storage and store the output locally
        path_test = '/tmp/orbit_snpp.czml'                                  #define path to access the NOAA's czml object saved in temp storage
        out_key = 'Orbits_snpp.czml'                                        #define output key for NOAA's czml object
        bucket.upload_file(path_test, 'outputs-V2/snpp/' + out_key)         #upload NOAA's czml object to S3 bucket
        return("SNPP's Orbit File Was Uploaded Successfully") 
        
        
    return "Success!"