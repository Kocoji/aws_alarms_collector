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
                alert_name = metrics['AlarmName']
                sdesc = metrics['StateReason']
                sns = metrics['Namespace']
                metric = GaugeMetricFamily("aws_alarms", 'Get the CW alarm', labels=['alarm_name','status','description','namespace'])
                alerts = GaugeMetricFamily("ALERTS", 'Alt metric name used in alert', labels=['alarm_name','status','alertstate','namespace'])
                metric.add_metric([str(alert_name), str(svalue),str(sdesc), str(sns)], 1 )
                alerts.add_metric([str(alert_name), str(svalue),"firing", str(sns)], 1 )
                yield metric
                yield alerts

def main():
    start_http_server(8899)
    
    REGISTRY.register(AWSCollector())
    while True:
        time.sleep(60)

main()


