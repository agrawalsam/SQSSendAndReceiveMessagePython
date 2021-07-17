import unittest

from SQSSendAndReceiveMessage import getEndpoints, sendMessages, getAndDeleteMessages

class TestSum(unittest.TestCase):
    def endpoints(self):
        """
        Test that if there are SQS Endpoints or not
        """
        result = getEndpoints()
        self.assertEqual(result, True)

    def sendMessages(self):
        """
        Test that if script can sendMessage to SQS or not
        """
        result = sendMessages("Hello World", "test", "1")
        self.assertEqual(result, '1321243312124234')

    def getAndDeleteMessages(self):
        """
        Test that if script can deleteMessage in SQS or not
        """
        result = getAndDeleteMessages()
        self.assertEqual(result, {
                                     'Successful': [
                                         {
                                             'Id': 'string'
                                         },
                                     ],
                                     'Failed': [
                                         {
                                             'Id': 'string',
                                             'SenderFault': True|False,
                                             'Code': 'string',
                                             'Message': 'string'
                                         },
                                     ]
                                 }
                                 )

if __name__ == "__main__":
    unittest.main()