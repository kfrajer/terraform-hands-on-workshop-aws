import json
import os
import time

import boto3
from decimal import Decimal

## RESOURCES: Master tutorial hellow world for API-Gateway/Lambda: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html?icmpid=apigateway_console
## RESOURCES: Interacting with DynamoDB: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-dynamo-db.html
## Docs/Read:
##   * https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-integration-types.html?icmpid=apigateway_console
##   * https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html

project_name = os.environ.get("PROJECT_NAME", "UnknownProjectName")
env = os.environ.get("ENV_NAME", "UnknownEnv")

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
tableName = 'dynamodb-' + env
table = dynamodb.Table(tableName)


def lambda_handler(event, context):
    print(event)

    body = {}
    status_code = 200
    headers = {
        "Content-Type": "application/json",
        "isBase64Encoded": "false",
    }

    #REF: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    http_method = event['httpMethod'] ## event['requestContext']['http']['method']
    path = event['path']

    greeter = 'World by method ' + http_method + " from path " + path

    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['greeter']) and (
                event['queryStringParameters']['greeter'] is not None):
            greeter = event['queryStringParameters']['greeter']
    except KeyError:
        print('No greeter')

    try:
        if (event['multiValueHeaders']) and (event['multiValueHeaders']['greeter']) and (
                event['multiValueHeaders']['greeter'] is not None):
            greeter = " and ".join(event['multiValueHeaders']['greeter'])
    except KeyError:
        print('No greeter')

    try:
        if (event['headers']) and (event['headers']['greeter']) and (
                event['headers']['greeter'] is not None):
            greeter = event['headers']['greeter']
    except KeyError:
        print('No greeter')

    if (event['body']) and (event['body'] is not None):
        body = json.loads(event['body'])
        try:
            if (body['greeter']) and (body['greeter'] is not None):
                greeter = body['greeter']
        except KeyError:
            print('No greeter')

    body_val = "Hello, " + greeter + "!"



    if path == "/helloworld/toc":
        body_val = f"Options are /toc  /   ?greeter=foobar   /?greeter=alien   /health   /info   /sleep1   /sleep5   /delay?duration=2"

    if path == "/helloworld/health":
        time_sec = time.time()
        body_val = f"OK @ {time_sec}"

    if path == "/helloworld/info":
        body_val = f"project name: {project_name} path::method => {path}::{http_method}"

    if path == "/helloworld/sleep1":
        time.sleep(1)
        body_val = f"Successfully executed one-second sleep!"

    if path == "/helloworld/sleep5":
        time_sec = time.time()
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_sec))
        time.sleep(5)
        time_diff = time.time() - time_sec
        body_val = f"Executed sleep {time_diff} that started at {formatted_time}"

    if path == "/helloworld/delay":
        if (event['queryStringParameters']) and (event['queryStringParameters']['duration']) and (
                event['queryStringParameters']['duration'] is not None):
            duration = event['queryStringParameters']['duration']

        if duration is not None:
            try:
                duration = int(duration)
            except ValueError:
                print(f'Invalid integer at /delay path, read: {duration}')
        else:
            print("Duration not provided, using default 5 seconds")
            duration = 5

        formatted_time_start = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        time.sleep(duration)
        formatted_time_end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        body_val = f"Executed custom sleep {duration}  that started at {formatted_time_start} until {formatted_time_end}"

    ## REFERENCE: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-dynamo-db.html
    try:
        ##Possible values for path are either "/items", "/items/" or "/items/an_id"
        if path.startswith("/items"):

            #item_id = path.replace("/items/", "") if path.startswith("/items/") else ""
            if (event['pathParameters']) and (event['pathParameters']['id']) and (
                event['pathParameters']['id'] is not None):
                item_id = event['pathParameters']['id']

            ## Handler: GET /items 
            if http_method == 'GET' and not item_id:
                body = table.scan()
                body = body["Items"]
                print("ITEMS----")
                print(body)
                responseBody = []
                for items in body:
                    responseItems = {'price': float(items['price']), 'id': items['id'], 'name': items['name']}
                    responseBody.append(responseItems)
                body_val = json.dumps(responseBody)

            elif http_method == 'GET':
                #TODO: Ensure item_id is not None
                body = table.get_item(Key={'id': item_id })
                #TODO: Does entry exist in the first place?
                body = body["Item"]
                responseBody = {'price': float(body['price']), 'id': body['id'], 'name': body['name']}
                body_val = json.dumps(responseBody)

            elif http_method == 'POST':
                entries = [
                    {
                        "id": "fake108",
                        "price": 105108,
                        "name": "QuaZ400108",
                    },
                    {
                        "id": "fake109",
                        "price": 105109,
                        "name": "QuaZ400109",
                    },
                    {
                        "id": "fake110",
                        "price": 105110,
                        "name": "QuaZ400110",
                    },
                ]
                inserted_ids = []
                for entry in entries:
                    inserted_ids.append(entry["id"])
                    table.put_item(Item=entry)
                body_val = 'Post item ' + ", ".join(inserted_ids)

            elif http_method == 'PUT':
                #TODO: Validate inpit values
                #TODO: Are we updating or rewritting an existent object, expected?
                requestJSON = json.loads(event['body'])
                table.put_item(
                    Item={
                        'id': requestJSON['id'],
                        'price': Decimal(str(requestJSON['price'])),
                        'name': requestJSON['name']
                    })
                body_val = 'Put item ' + requestJSON['id']

            elif http_method == 'DELETE':
                #TODO:  Does the item exist in the firt place?
                #TODO: Ensure item_id is not None
                table.delete_item(Key={'id': item_id})
                body_val = 'Deleted item ' + item_id

    except KeyError:
        status_code = 400
        body_val = 'Unsupported route: ' + path

    ##body = json.dumps(body_val)
    res = {
        "statusCode": status_code,
        "headers": headers,
        "body": body_val
    }

    return res
