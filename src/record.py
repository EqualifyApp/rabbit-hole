from utils.watch import logger
from utils.auth import catch_rabbits
import json
from utils.process.axe import process_axe
from utils.process.crawler import process_crawler
from utils.process.erros import process_crawl_errors

# queues_to_check = ["landing_axe", "landing_crawler", "landing_uppies"]
queue_processors = {
    "landing_crawler": process_crawler,
    "landing_axe": process_axe,
    "error_crawler": process_crawl_errors
    }


def process_message(processor):
    def wrapper(channel, method, properties, body):
        logger.info(f'Processing new message: {channel}')
        message = json.loads(body)
        processor(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug(
            f'Message processed and acknowledged: {method.delivery_tag}')
    return wrapper


def main():
    logger.info('Starting main function')
    try:
        for queue_name, processor in queue_processors.items():
            logger.info(f'Starting processing for queue: {queue_name}')
            catch_rabbits(queue_name, processor)
    except Exception as e:
        logger.error(f'Error in main function: {e}')
    finally:
        logger.info('Main function finished')


if __name__ == "__main__":
    logger.info('Starting script')
    main()

# /Users/Shared/GitHub/Orgs/EqualifyApp/rabbit-hole/src/record.py
# {"url": "https://www.governor.pa.gov", "url_id": 322}
# {"url": "http://medicaid.gov", "url_id": 26}
# {"url": "https://civicaction.com", "url_id": 1}
# queues_to_check = ["landing_axe", "landing_crawler", "landing_uppies"]