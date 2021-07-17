# SQSSendAndReceiveMessagePython
Using Python Boto3 API SDK to send and receive messages from AWS SQS. 

SQS in AWS forms an integral part of Event Driven Architecture. 

SQS according to Wikipedia - 
Amazon Simple Queue Service is a distributed message queuing service introduced by Amazon.com in late 2004. It supports programmatic sending of messages via web service applications as a way to communicate over the Internet.

SQS is one of the most earliest service provided by AWS. 

This project details utilisation of SQS messaging service in AWS Environment. 

# Usage -
SendMessage - python SQSSendAndReceiveMessage.py 1 0 "Hello world" "test" "1"

ReceiveMessage - python SQSSendAndReceiveMessage.py 0 1

Send and ReceiveMessage  - python SQSSendAndReceiveMessage.py 1 1

Additionaly, testCode has also been updated for the same. 

Note - 

In order to utilise the SQS in another service like EC2, Lambda etc. , traffic must go through the SQS VPC Endpoint.  
