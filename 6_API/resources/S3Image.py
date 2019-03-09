# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request
import boto3
import botocore

BUCKET_NAME = 'bpcalender' # replace with your bucket name

class S3ImageDownload(Resource):
    def get(self):
        fromfile = request.args.get('fromfile')
        tofilename = request.args.get('tofilename')
        print(fromfile, tofilename)
        get_image_from_s3(fromfile, tofilename)
        return {"message": "success"}
    
    def post(self):
        fromfile = request.args.get('fromfile')
        tofilename = request.args.get('tofilename')
        print(fromfile, tofilename)
        get_image_from_s3(fromfile, tofilename)
        return {"message": "success"}

class S3ImageUpload(Resource):
    def get(self):
        fromfile = request.args.get('fromfile')
        uploadfilename = request.args.get('uploadfilename')
        print(fromfile, uploadfilename)
        put_image_to_s3(fromfile, uploadfilename)
        return {"message": "success"}
    
    def post(self):
        fromfile = request.args.get('fromfile')
        uploadfilename = request.args.get('uploadfilename')
        print(fromfile, uploadfilename)
        put_image_to_s3(fromfile, uploadfilename)
        return {"message": "success"}
    
    
def get_bucket_list(self):
    client = boto3.client('s3')
    response = client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    print("Bucket List: %s" % buckets)
    return buckets

def get_Object_list(self):
    s3 = boto3.resource('s3')
    for page in s3.Bucket(BUCKET_NAME).objects.pages():
        for obj in page:
            print(obj.key)

def get_image_from_s3(fromfile, tofilename):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file(fromfile, tofilename)
        print("download complete " + tofilename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
            
def put_image_to_s3(fromfile, uploadfilename):          
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(fromfile, BUCKET_NAME, uploadfilename)
    s3.ObjectAcl(BUCKET_NAME, uploadfilename).put(ACL='public-read')
    print("upload complete " + fromfile)
