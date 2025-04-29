# TODO: Message Handler needs to be implemented. Just trying to test the influx db connection

from api.services.influx_service import InfluxConnector


def add_cpu_data(data):
    with InfluxConnector() as influx:
        influx.write_data(data)
