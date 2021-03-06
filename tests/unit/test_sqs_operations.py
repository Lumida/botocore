#!/usr/bin/env python
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from tests import unittest, BaseSessionTest
import botocore.session


class TestSQSOperations(BaseSessionTest):

    def setUp(self):
        super(TestSQSOperations, self).setUp()
        self.sqs = self.session.get_service('sqs')
        self.queue_url = 'https://queue.amazonaws.com/123456789012/testcli'
        self.receipt_handle = """MbZj6wDWli%2BJvwwJaBV%2B3dcjk2YW2vA3%2BSTFFljT
M8tJJg6HRG6PYSasuWXPJB%2BCwLj1FjgXUv1uSj1gUPAWV66FU/WeR4mq2OKpEGY
WbnLmpRCJVAyeMjeU5ZBdtcQ%2BQEauMZc8ZRv37sIW2iJKq3M9MFx1YvV11A2x/K
SbkJ0="""

    def test_add_permission(self):
        op = self.sqs.get_operation('AddPermission')
        params = op.build_parameters(queue_url=self.queue_url,
                                     label='testLabel',
                                     aws_account_ids=['125074342641',
                                                      '125074342642'],
                                     actions=['SendMessage',
                                              'ReceiveMessage'])
        result = {'QueueUrl': self.queue_url,
                  'Label': 'testLabel',
                  'AWSAccountId.1': '125074342641',
                  'ActionName.1': 'SendMessage',
                  'AWSAccountId.2': '125074342642',
                  'ActionName.2': 'ReceiveMessage'}
        self.assertEqual(params, result)

    def test_change_message_visibility(self):
        op = self.sqs.get_operation('ChangeMessageVisibility')
        params = op.build_parameters(queue_url=self.queue_url,
                                     visibility_timeout=60,
                                     receipt_handle=self.receipt_handle)
        result = {'QueueUrl': self.queue_url,
                  'VisibilityTimeout': '60',
                  'ReceiptHandle': self.receipt_handle}
        self.assertEqual(params, result)

    def test_change_message_visibility_batch(self):
        self.maxDiff = None
        prefix = 'ChangeMessageVisibilityBatchRequestEntry'
        op = self.sqs.get_operation('ChangeMessageVisibilityBatch')
        params = op.build_parameters(queue_url=self.queue_url,
                                     entries=[{'ReceiptHandle':self.receipt_handle,
                                               'VisibilityTimeout':45,
                                               'Id':'change_visibility_msg_2'},
                                              {'ReceiptHandle':self.receipt_handle,
                                               'VisibilityTimeout':45,
                                               'Id':'change_visibility_msg_3'}])
        result = {'QueueUrl': self.queue_url,
                  '%s.1.Id' % prefix: 'change_visibility_msg_2',
                  '%s.1.ReceiptHandle' % prefix: self.receipt_handle,
                  '%s.1.VisibilityTimeout' % prefix: '45',
                  '%s.2.Id' % prefix: 'change_visibility_msg_3',
                  '%s.2.ReceiptHandle' % prefix: self.receipt_handle,
                  '%s.2.VisibilityTimeout' % prefix: '45'}
        self.assertEqual(params, result)

    def test_set_queue_attribute(self):
        op = self.sqs.get_operation('SetQueueAttributes')
        params = op.build_parameters(queue_url=self.queue_url,
                                     attributes={'VisibilityTimeout': '15'})
        result = {'QueueUrl': self.queue_url,
                  'Attribute.1.Name': 'VisibilityTimeout',
                  'Attribute.1.Value': '15'}
        self.assertEqual(params, result)

    def test_list_dead_letter_source_queues(self):
        op = self.sqs.get_operation('ListDeadLetterSourceQueues')
        params = op.build_parameters(queue_url=self.queue_url)
        result = {'QueueUrl': self.queue_url}
        self.assertEqual(params, result)
        for param in op.params:
            if param.name == 'QueueUrl':
                self.assertEqual(getattr(param, 'no_paramfile', None), True)
