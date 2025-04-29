import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from api.config import settings
import logging


class InfluxConnector:
    def __init__(self, bucket):
        self.client = influxdb_client.InfluxDBClient(
            url=f"{settings.INFLUX_HOST}:{settings.INFLUX_PORT}",
            token=settings.INFLUX_TOKEN,
            org=settings.INFLUX_ORG,
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket

    def __enter__(self):
        if not self.get_bucket(self.bucket):
            try:
                self.client.buckets_api().create_bucket(bucket_name=self.bucket)
            except Exception as e:
                logging.error(f"Error creating bucket {self.bucket}: {e}")
                raise
        return self

    def get_bucket(self, bucket_name):
        """
        Get a bucket by name.
        :param bucket_name: The name of the bucket to retrieve.
        :return: The bucket object if found, None otherwise.
        """
        try:
            return self.client.buckets_api.find_bucket_by_name(bucket_name)
        except Exception as e:
            logging.error(f"Error retrieving bucket {bucket_name}: {e}")
            return None

    def write_data(self, bucket, data):
        """
        Write data to InfluxDB.
        :param bucket: The name of the bucket to write to.
        :param data: The data to write. Should be list of Points, line protocol, or valid dicts.
        """
        try:
            self.write_api.write(bucket=bucket, record=data)
        except Exception as e:
            print(f"Error writing data to InfluxDB: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
