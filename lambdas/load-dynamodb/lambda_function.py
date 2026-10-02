from decimal import Decimal
import boto3
import json
import os


def lambda_handler(event,context):
    
    dynamodb=boto3.resource('dynamodb')                                 #define the DynamoDB SDK resource
    table = dynamodb.Table('orbits-czml-V2')                            #define the DynamoDB table
    
    s3 = boto3.resource('s3')                                           #define the S3 SDK resource
    bucket = s3.Bucket('orbital-vision-data-and-code')                  #define the S3 bucket

    in_key_aqua = 'outputs-V2/aqua/Orbits_aqua.czml'                    #define key of AQUA's Orbit.czml file in s3
    in_key_noaa = 'outputs-V2/noaa/Orbits_noaa.czml'                    #define key of NOAA's Orbit.czml file in s3
    in_key_snpp = 'outputs-V2/snpp/Orbits_snpp.czml'                    #define key of SNPP's Orbit.czml file in s3
    
    for record in event['Records']:
        key = record['s3']['object']['key']
    
    if key == in_key_aqua:
        local_orbit_dir = '/tmp/' + 'Orbits_aqua.czml'                 #define where AQUA's Orbit.czml file will be temporarily stored
        bucket.download_file(in_key_aqua, local_orbit_dir)             #download AQUA's Orbit.czml file from s3 to local storage
        path_test = '/tmp/Orbits_aqua.czml'                            #define path to access AQUA's .czml file saved in temp storage
        with open(path_test, 'r') as myfile:                           #open and read AQUA's .czml file
            data=myfile.read()
        obj = json.loads(data, parse_float=Decimal)                    #parse the JSON file 
        UTC = obj[0]['clock']['currentTime']                           #define the UTC (sort key) for AQUA
        for item in event:                                             #add an item with AQUA's attributes to the table
            response=table.put_item(
                                    Item={
                                        'ItemName': 'aquaOrbit',
                                        'UTC': UTC,
                                        'NORADid': '27424',            #add the NORAD ID attribute for AQUA
                                        'orbitsJson':obj
                                        }
                                    )
        return("AQUA Item Was Added To Table Successfully")
                                    
    if key == in_key_noaa:
        local_orbit_dir = '/tmp/' + 'Orbits_noaa.czml'                 #define where NOAA's Orbit.czml file will be temporarily stored
        bucket.download_file(in_key_noaa, local_orbit_dir)             #download NOAA's Orbit.czml file from s3 to local storage
        path_test = '/tmp/Orbits_noaa.czml'                            #define path to access NOAA's .czml file saved in temp storage
        with open(path_test, 'r') as myfile:                           #open and read NOAA's .czml file
            data=myfile.read()
        obj = json.loads(data, parse_float=Decimal)                    #parse the JSON file 
        UTC = obj[0]['clock']['currentTime']                           #define the UTC (sort key) for NOAA
        for item in event:                                             #add an item with NOAA's attributes to the table
            response=table.put_item(
                                    Item={
                                        'ItemName': 'noaaOrbit',
                                        'UTC': UTC,
                                        'NORADid': '43013',            #add the NORAD ID attribute for NOAA
                                        'orbitsJson':obj
                                        }
                                    )
        return("NOAA Item Was Added To Table Successfully")
        
    if key == in_key_snpp:
        local_orbit_dir = '/tmp/' + 'Orbits_snpp.czml'                 #define where SNPP's Orbit.czml file will be temporarily stored
        bucket.download_file(in_key_snpp, local_orbit_dir)             #download SNPP's Orbit.czml file from s3 to local storage
        path_test = '/tmp/Orbits_snpp.czml'                            #define path to access SNPP's .czml file saved in temp storage
        with open(path_test, 'r') as myfile:                           #open and read SNPP's .czml file
            data=myfile.read()
        obj = json.loads(data, parse_float=Decimal)                    #parse the JSON file 
        UTC = obj[0]['clock']['currentTime']                           #define the UTC (sort key) for SNPP
        for item in event:                                             #add an item with SNPP's attributes to the table
            response=table.put_item(
                                    Item={
                                        'ItemName': 'snppOrbit',
                                        'UTC': UTC,
                                        'NORADid': '37849',            #add the NORAD ID attribute for SNPP
                                        'orbitsJson':obj
                                        }
                                    )
        return("SNPP Item Was Added To Table Successfully")
                                    

    return 'success!'







    # local_orbit_dir_aqua = '/tmp/' + 'Orbits_aqua.czml'                 #define where AQUA's Orbit.czml file will be temporarily stored
    # local_orbit_dir_noaa = '/tmp/' + 'Orbits_noaa.czml'                 #define where NOAA's Orbit.czml file will be temporarily stored     
    # local_orbit_dir_snpp = '/tmp/' + 'Orbits_snpp.czml'                 #define where SNPP's Orbit.czml file will be temporarily stored     

    # bucket.download_file(in_key_aqua, local_orbit_dir_aqua)             #download AQUA's Orbit.czml file from s3 to local storage
    # bucket.download_file(in_key_noaa, local_orbit_dir_noaa)             #download NOAA's Orbit.czml file from s3 to local storage
    # bucket.download_file(in_key_snpp, local_orbit_dir_snpp)             #download SNPP's Orbit.czml file from s3 to local storage

    
    # #if os.path.isfile('/tmp/' + 'Orbits.czml'):                        #Check if tle file was downloaded to ephemeral (temp) storage
    #     #print("Orbit file is in local storage")

 
    
    # path_test_aqua = '/tmp/Orbits_aqua.czml'                            #define path to access AQUA's .czml file saved in temp storage
    # path_test_noaa = '/tmp/Orbits_noaa.czml'                            #define path to access NOAA's .czml file saved in temp storage
    # path_test_snpp = '/tmp/Orbits_snpp.czml'                            #define path to access SNPP's .czml file saved in temp storage

    # #LOAD AQUA DATA TO DDB
    # with open(path_test_aqua, 'r') as myfile_a:                         #open and read AQUA's .czml file
    #     data_aqua=myfile_a.read()
    # obj_aqua = json.loads(data_aqua, parse_float=Decimal)               #parse the JSON file 
    # UTC_aqua = obj_aqua[0]['clock']['currentTime']                      #define the UTC (sort key) for AQUA
    # for item in event:                                                  #add an item with AQUA's attributes to the table
    #     response=table.put_item(
    #                             Item={
    #                                 'ItemName': 'aquaOrbit',
    #                                 'UTC': UTC_aqua,
    #                                 'NORADid': '27424',                 #add the NORAD ID attribute for AQUA
    #                                 'orbitsJson':obj_aqua
    #                                  }
    #                             )
                                
    # #LOAD NOAA DATA TO DDB                           
    # with open(path_test_noaa, 'r') as myfile_n:                         #open and read NOAA's .czml file
    #     data_noaa=myfile_n.read()
    # obj_noaa = json.loads(data_noaa, parse_float=Decimal)               #parse the JSON file 
    # UTC_noaa = obj_noaa[0]['clock']['currentTime']                      #define the UTC (sort key) for NOAA
    # for item in event:                                                  #add an item with NOAA's attributes to the table
    #     response=table.put_item(
    #                             Item={
    #                                 'ItemName': 'noaaOrbit',
    #                                 'UTC': UTC_noaa,
    #                                 'NORADid': '43013',                 #add the NORAD ID attribute for NOAA
    #                                 'orbitsJson':obj_noaa
    #                                  }
    #                             )
                                
    # #LOAD SNPP DATA TO DDB                           
    # with open(path_test_snpp, 'r') as myfile_s:                         #open and read SNPP's .czml file
    #     data_snpp=myfile_s.read()
    # obj_snpp = json.loads(data_snpp, parse_float=Decimal)               #parse the JSON file 
    # UTC_snpp = obj_snpp[0]['clock']['currentTime']                      #define the UTC (sort key) for SNPP
    # for item in event:                                                  #add an item with SNPP's attributes to the table
    #     response=table.put_item(
    #                             Item={
    #                                 'ItemName': 'snppOrbit',
    #                                 'UTC': UTC_snpp,
    #                                 'NORADid': '37849',                 #add the NORAD ID attribute for SNPP
    #                                 'orbitsJson':obj_snpp
    #                                  }
    #                             )
                                
    
   