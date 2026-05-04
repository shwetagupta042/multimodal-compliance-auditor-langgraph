# azure opentelemetry integration

import os
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

logger = logging.getLogger("brand-guardian-telemetry")

def setup_telemetry():
    '''
    Initializes Azure monitor opentelemetry
    Tracks: HTTP requests, database queries, errors, performance metrics
    send the data to azure monitor

    it auto-captures every api request
    no need to manually log each endpoint
    '''

    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not connection_string:
        logger.warning("No instrumentation key found. Telemetry is DISABLED!")
        return

    # configure the azure monitor
    try:
        configure_azure_monitor(
            connection_string=connection_string,
            logger_name = "brand-guardian-tracer"
        )
        logger.info("Azure Monitor tracking enabled and connected")
    except Exception as e:
        logger.error(f"Failed to initialize azure monitor {str(e)}")


'''
why do we use telemetry?

without: API is slow
how many users today? no visibility
with : which part of API is slow?
- how many users today?
- /audit endpoint averages to 4.5s and /indexer endpoint avg to 3.5s
- Error logs show : 12% of audits failed due to youtube download errors
- Metrics show: 450 API calls today, 89% success rate

'''






