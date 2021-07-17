# Usage -
# SendMessage - python SQSProd.py 1 0 "Hello world" "test" "1"
# ReceiveMessage - python SQSProd.py 0 1
# Send and ReceiveMessage  - python SQSProd.py 1 1

#import config from **
import boto3
import logging
region='us-east-1' # to come from Config File
sqsendpoints=[]

def getEndpoints():
    """
        Get All the VPC Endpoints
        And check if there is SQS Endpoint present or not.
        Output:
        If yes, return True
        else return False
    """
    client = boto3.client('ec2', region_name=region)
    response = client.describe_vpc_endpoints()
    for vpc_endpoints in response['VpcEndpoints']:
        if 'sqs' in vpc_endpoints['ServiceName']:
            for ve in vpc_endpoints['DnsEntries']:
                sqsendpoints.append(ve['DnsName'])
    #if no SQS Endpoint Return False
    if len(sqsendpoints)==0:
        return False
    return True

def sendMessages(Message: str, MessageGroupId: str, MessageDeduplicationId: str):
    """
        Send Message to SQS with
        Input:
        Message - Content of message
        MessageGroupId - If any classification is present.
        MessageDeduplicationId - to prevent reading/processing duplicate messages
        Output:
        Return MessageID of the message send
    """
    queue = sqs_client.send_message(
        QueueUrl=SQSQueueUrl,
        MessageBody=Message,
        MessageGroupId=MessageGroupId,
        MessageDeduplicationId=MessageDeduplicationId
    )
    logger.info('Send Message Id : %s' % json.dumps(queue.get('MessageId')))
    return queue.get('MessageId')

def getAndDeleteMessages():
    """
        Receive all the Message present in SQS.
        Messages can be further segregated based on Group Id.
        Delete all the Messages in SQS which have been received.
        Output:
        return True, if received and deleted successfully.
        return False, if some error occurred.
    """
    try:
        queue = sqs_client.receive_message(
            QueueUrl=SQSQueueUrl,
            AttributeNames=['All'],
            ReceiveRequestAttemptId='1'
        )
        entries=[{'Id':msg['MessageId'], 'ReceiptHandle':msg['ReceiptHandle']} for msg in queue['Messages']]
        response = sqs_client.delete_message_batch(
            QueueUrl=SQSQueueUrl,
            Entries=entries
        )
        logger.info('Deleted Message Entries : %s' % json.dumps(entries))
        return response
    except Exception:
        print(traceback.print_exc())

if __name__ == "__main__":
    send_Code = sys.argv[1]
    receive_Code = sys.argv[2]

    message = sys.argv[3]
    messageGroupId = sys.argv[4]
    messageDeduplicationId = sys.argv[5]

    if getEndpoints():
        try:
            #make sqs session
            session = boto3.session.Session()
            sqs_client = session.client(service_name='sqs', region_name=region, endpoint_url='https://'+sqsendpoints[0])
            queueUrl = sqs_client.list_queues()['QueueUrls']

            #get the QueueUrl of Desired SQS Queue
            SQSName = "" # to come from Config
            SQSQueueUrl = ""
            index=0
            for SQSName in queueUrl:
                index=index+1
                SQSQueueUrl=queueUrl[index]

            #For sending Message -
            if(send_Code==1):
                Message = message
                MessageGroupId = messageGroupId
                MessageDeduplicationId = messageDeduplicationId
                sendMessages(Message, MessageGroupId, MessageDeduplicationId)

            #For receiving and Deleting Message -
            if(receive_Code==1):
                getAndDeleteMessages()
        except Exception:
            print(traceback.print_exc())
            print("Error Occurred")
    else:
        print("No SQS VPC Endpoint")
        # Email Sent through Email Module
        pass