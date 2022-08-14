import time, boto3
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily

class AWSCollector(object):
    def __init__(self):
        pass

    def collect(self):
        cloudwatch = boto3.client('cloudwatch')
        paginator = cloudwatch.get_paginator('describe_alarms')
        for response in paginator.paginate(StateValue='ALARM'):
            for metrics in response['MetricAlarms']:
                svalue = metrics['StateValue']
                sdesc = metrics['StateReason']
                sns = metrics['Namespace']
                metric = GaugeMetricFamily("aws_alarms", 'Help text', labels=['status','description','namespace'])
                metric.add_metric([str(svalue),str(sdesc), str(sns)], 1 )
                yield metric

def main():
    start_http_server(8899)
    
    REGISTRY.register(AWSCollector())
    while True:
        time.sleep(60)

main()


