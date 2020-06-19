# -*- coding: utf-8 -*-
"""
This sample is designed for client module debugging.

Prepare for Beebotte access information in the config file 'config.py'
including:
    channel_token : str
        Channel token.
    ca_cert : str
        Path to a SSL server certificate.
    topic_base : str
        Topic name, i.e., 'channel/resource'.
        None to use non-SSL connection.
    unit : int
        Unit number.
"""

#
# Copyright (c) 2020, Shigemi ISHIDA
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import mqbeebotte
import csv
import datetime

#=========================================================================
# This sample comes with config.py.
# Please modify config.py before executing this sample.
#=========================================================================
def on_connect(client, userdata, flags, respons_code):
    print('Connected to Beebotte')
    return

#--------------------------------------------------------------------------
def on_message(client, userdata, msg):
    print('[{}] {}'.format(msg.topic, str(msg.payload)))
    print(type(msg.payload))
    if (msg.topic == 'pbl1/sensors/envsensor/1'):
        dt_now = datetime.datetime.now()
        dict = json.loads(msg.payload)
        data_list = [dict['temperature'], dict['pressure'], dict['humidity']]
        '''
        with open('csv/sensor_data_test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['month','hour','temperature','pressure','humidity'])
            writer.writerow([dt_now.month, dt_now.hour, dict['temperature'], dict['pressure'], dict['humidity']])

        with open('original_sensor_data.json', 'w') as f:
            json.dump(dict, f, indent=2)
        '''

    # Stop network loop thread.
    # When block_wait is set to True, stop() blocks until the thread stops.
    # Default block_wait is False.  In a non-blocking manner, you need to
    # wait until the thead stops using client.join().
    client.stop(block_wait=True)

    # Disconnect and removes the client instance.
    del client

    # ここでmainとかを呼ぶ？(main(data_list))

    return 

#=========================================================================
# Before execute any MQTT client code, you need to create a channel and resource
# on Beebotte.

# Load config file.
import config
import json

def subscribe_sensor_data():
    # Create an client instance.
    try:
        ca_cert = config.ca_cert
    except AttributeError:
        ca_cert = None
    # client = mqbeebotte.client(ca_cert=ca_cert)
    # 非ssl接続
    client = mqbeebotte.client()

    # And connect to Beebotte.
    client.connect(config.channel_token, on_connect=on_connect, on_message=on_message)
    # Start network loop thread.
    # Thread is running in a non-blocking manner.
    client.start()

    # Subscribe to mutiple topics.
    # Generate target topic names.
    topics = [
        'envsensor/1',
    ]
    # subscribe to sensor data topics
    sub_topics = list(map(lambda x: config.topic_base + '/' + x, topics))
    print('Subscribe to {}'.format(', '.join(sub_topics)))
    # Give a list to subscribe() to subscribe to multiple topics.
    client.subscribe(sub_topics)
    time.sleep(3600)

    # Stop network loop thread.
    # When block_wait is set to True, stop() blocks until the thread stops.
    # Default block_wait is False.  In a non-blocking manner, you need to
    # wait until the thead stops using client.join().
    client.stop(block_wait=True)

    # Disconnect and removes the client instance.
    del client