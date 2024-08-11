from threading import local
import influxdb
import datetime

# Configuration of InfluxDB
DB_HOST = 'localhost'
DB_PORT = 8086
DB_USERNAME = 'SideChannel_Parser'
DB_PASSWORD = 'abcd1234'


class DatabaseClient:
    def __init__(self, db_host, db_port):
        # Create InfluxDB Client Object
        self.__client = influxdb.InfluxDBClient(host=db_host, port=db_port)
        
        # Create InfluxDB Database
        self.__create_database(name='side_channel')

    def __create_database(self, name):
        # Delete old Database (if existed)
        self.__client.drop_database(name)
        # Create new Database
        self.__client.create_database(name) 

    def insert_data(self, timestamp, id, msg_freq_time, msg_freq, data_len, tav):
        json_data = [
        {
            "measurement": "side_channel",
            "tags": {
                "host": "Unknown",
                "region": "Unknown",
                "id": "Unknown"
            },
            "time": "2022-07-01T14:00:00Z",
            "fields": {

            }
        }
        ]

        curr_time = datetime.datetime.utcfromtimestamp(timestamp)
        json_data[0]['time'] = curr_time
        json_data[0]['tags']['id'] = id
        json_data[0]['fields']['arbitration_id'] = id
        json_data[0]['fields']['msg_freq_time'] = msg_freq_time
        json_data[0]['fields']['msg_freq'] = msg_freq
        json_data[0]['fields']['data_len'] = data_len
        json_data[0]['fields']['bit_flips_msg'] = tav.count(1)

        # Write JSON Object in Database
        self.__client.write_points(json_data, database='side_channel')