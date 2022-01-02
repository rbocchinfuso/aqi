#!/usr/bin/env python
"""aqi.py: Air Quality Index Monitor"""

# owned
__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Air Quality Index Monitor'
__credits__ = ['Rich Bocchinfuso', 'Eden Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

import serial, time, configparser
from colorama import Fore, Back, Style
from serial import Serial
from texttable import Texttable
from tqdm import tqdm
from ISStreamer.Streamer import Streamer
from Adafruit_IO import Client as adaClient
from pushover import Client as poClient
from paho.mqtt import client as mqtt_client


def alert(pmtwofive, pmten):

    if (pmtwofive <= 12) and (pmten <= 54):
        print(Fore.GREEN + '--- Air quality levels are good. --- ' + Style.RESET_ALL)
    elif (pmtwofive > 12) or (pmten > 54):  
            if (pushovercheck !="xxxxxxxxxxxxxxxxxxxxxxx"):
                po = poClient(config['pushover']['user_key'], api_token=config['pushover']['api_token'])
            if (pmtwofive > 12):
                print(Fore.RED + '!!! PM2.5 air quality reading above acceptable levels; triggering alert !!! ' + Style.RESET_ALL)
                if (pushovercheck !="xxxxxxxxxxxxxxxxxxxxxxx"):
                    po.send_message("!!! PM2.5 AQI above acceptable level; check environment !!!", title="PM2.5 AQI Alert")
            if (pmten > 54):
                print(Fore.RED + '!!! PM10 air quality reading above acceptable levels; triggering alert !!! ' + Style.RESET_ALL)
                if (pushovercheck !="xxxxxxxxxxxxxxxxxxxxxxx"):
                    po.send_message("!!! PM2.5 AQI above acceptable level; check environment !!!", title="PM10 AQI Alert")
    else:
        print(Fore.RED + '!!! Unknown AQI reading; triggering alert !!! ' + Style.RESET_ALL)
        po.send_message("!!! Unknown AQI reading; check monitor !!!", title="AQI Unknown Alert")
    

def publish(svc, client, pmtwofive, pmten):    
    print(Back.GREEN + '\nStreaming to '+ svc + Style.RESET_ALL)
    if svc == 'initialstate':
        initialstate(pmtwofive, pmten)
    elif svc == 'adafruitio':
        adafruitio(pmtwofive, pmten)
    elif svc == 'both':
        initialstate(pmtwofive, pmten)
        adafruitio(pmtwofive, pmten)
    else: 
        print('Invalid Service')
    
    result = client.publish(topic_pm25, pmtwofive)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{pmtwofive}` to topic `{topic_pm25}`")
    else:
        print(f"Failed to send message to topic {topic}")
    result = client.publish(topic_pm10, pmten)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{pmten}` to topic `{topic_pm10}`")
    else:
        print(f"Failed to send message to topic {topic}")

def initialstate(pmtwofive, pmten):
    streamer.log("PM_2.5", pmtwofive)
    streamer.log("PM_10", pmten)
    # flush data (force the buffer to empty and send)
    streamer.flush()
    # close the stream
    streamer.close()

def adafruitio(pmtwofive, pmten):
    pmtwofive_feed = aio.feeds(config['adafruit_io']['pmtwofive_feed'])
    pmten_feed = aio.feeds(config['adafruit_io']['pmten_feed'])
    aio.send(pmtwofive_feed.key, pmtwofive)
    aio.send(pmten_feed.key, pmten)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def main():
    client = connect_mqtt()
    client.loop_start()
    while True:
        data = []
        for index in range(0,10):
            datum = ser.read()
            data.append(datum)
        pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10   
        pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

        publish(config['local']['services'], client, pmtwofive, pmten)
        t = Texttable()
        t.add_rows([['Desc', 'Metric'], ['PM2.5', pmtwofive], ['PM10', pmten]])
        print(t.draw())
        alert(pmtwofive, pmten)
        
        # visual cycle time
        for i in tqdm(range(cycle_time)):
            time.sleep(1)
    
if __name__ == '__main__':
    # read and parse config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    # create a Streamer instance
    streamer = Streamer(bucket_name=config['initialstate']['is_bucket_name'], bucket_key=config['initialstate']['is_bucket_key'], access_key=config['initialstate']['is_access_key'])
    # create a adafruit.io instance
    aio = adaClient(config['adafruit_io']['adafruitio_username'], config['adafruit_io']['adafruitio_key'])
    # set port for air quality monitor
    ser = serial.Serial(config['local']['device'])
    # set pushover availability check
    pushovercheck =  config['pushover']['api_token']
    # set cycle time
    cycle_time = int(config['local']['cycle_time'])    
    
    #mqtt settings:
    broker = config['mqtt']['broker']
    port = int(config['mqtt']['port'])
    topic_pm10 = config['mqtt']['topic_pm10']
    topic_pm25 = config['mqtt']['topic_pm25']
    client_id = config['mqtt']['client_id']
    username = config['mqtt']['username']
    password = config['mqtt']['password']
    
    main()
