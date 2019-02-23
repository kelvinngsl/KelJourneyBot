import json
import urllib.parse
import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


class Bus():
    def __init__(self, busstopcode):
        self.busstopcode = busstopcode
        self.api_url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?'
        self.accountkey = config.get('API', 'LTA_KEY')
        self.content_type = 'application/json'

    def get_json(self):
        parameters = {'BusStopCode': self.busstopcode}
        headers = {'AccountKey': self.accountkey, 'Content-Type' : self.content_type}

        result = requests.get(self.api_url, headers=headers, params=parameters)

        result_json = result.json()['Services']
        return result_json
        
    def check_legit(self):
        result = self.get_json()
        return len(result) >0


    def get_bus_List(self):
        result = self.get_json()
        return [bus["ServiceNo"] for bus in result]

    def get_bus(self, busno):
        parameters = {'BusStopCode': self.busstopcode, 'ServiceNo':busno}
        headers = {'AccountKey': self.accountkey, 'Content-Type' : self.content_type}

        result = requests.get(self.api_url, headers=headers, params=parameters)

        result_json = result.json()['Services']
        return result_json

    def get_time(self,busno,duration):
        bus = self.get_bus(busno)[0]

        bus_details = {'SEA': 'Seats Avail', 'SDA':'Standing Avail', 'SD':'Single Deck', 'DD':'Double Deck','BD': 'Bendy' }



        reply = ''
        nextbus = "NextBus"
        for number in range(1,4):
            
            if bus[nextbus]['EstimatedArrival'] != '':

                bus_type = bus_details[bus[nextbus]["Type"]]
                bus_load = bus_details[bus[nextbus]["Load"]]

                import datetime
                now = datetime.datetime.now()

                from datetime import datetime, timedelta
                time_arrival = bus[nextbus]["EstimatedArrival"].replace("T"," ")
                time_arrival = time_arrival[0:19]
                time_arrival = datetime.strptime(time_arrival, '%Y-%m-%d %H:%M:%S')
               
                import datetime
                time_to_leave = time_arrival - datetime.timedelta(seconds=(duration*60)+90)

                if time_to_leave < now:
                    reply += "<b>Bus {} \U0000274C </b>\nYou might not make it, please catch <b>the next Bus!</b>\n\n".format(str(number))
                else:
                    reply += "<b>Bus {} \U00002705 </b>\nYou can leave house at <b>{}</b>! ({} & {})\n\n".format(number,time_to_leave.time(),bus_type,bus_load)
            else:
                reply += "<b> No more bus available after this! </b>"
                break

            nextbus = nextbus[0:7] + str(number+1)

        return reply

            

    def get_busstop(self):
        headers = {'AccountKey': self.accountkey, 'Content-Type' : self.content_type}
        results = []
        for skip in range(0,5001,500):
            result = requests.get('http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip='+str(skip), headers=headers)

            result_json = result.json()["value"]
            results += result_json
        return results

 
    