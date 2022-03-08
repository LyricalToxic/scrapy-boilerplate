import logging
from typing import Type

from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from rmq.utils import get_import_full_name
from rmq_twisted.spiders import RMQSpider
from rmq_twisted.schemas.messages.base_rmq_message import BaseRMQMessage
from rmq_twisted.utils import signals as CustomSignals
from rmq_twisted.utils.pika_blocking_connection import PikaBlockingConnection
from tests.rmq_twisted_tests.constant import QUEUE_NAME


class CustomSpiderMiddleware:
    def process_spider_output(self, response, result, spider):
        raise Exception('CustomSpiderMiddleware.process_spider_output exception')


class MySpider(RMQSpider):
    name = 'myspider'
    message_type: Type[BaseRMQMessage] = BaseRMQMessage
    task_queue_name: str = QUEUE_NAME

    custom_settings = {
        "SPIDER_MIDDLEWARES": {
            get_import_full_name(CustomSpiderMiddleware): 999,
        }
    }

    def parse(self, response, **kwargs):
        self.logger.info("PARSE METHOD")
        yield from ()

    def next_request(self, message: BaseRMQMessage) -> Request:
        return Request('https://httpstat.us/200', dont_filter=True)


class TestSpiderParseException:
    def test_crawler_successfully(self, rabbit_setup: PikaBlockingConnection, crawler: CrawlerProcess):
        successfully_handled = False

        def on_before_ack_message(rmq_message: BaseRMQMessage, spider: RMQSpider):
            logging.info('BEFORE ACK_CALLBACK %s:%s', spider.name, rmq_message.deliver.delivery_tag)

        def on_after_ack_message(rmq_message: BaseRMQMessage, spider: RMQSpider):
            logging.info('AFTER ACK_CALLBACK %s:%s', spider.name, rmq_message.deliver.delivery_tag)
            crawler.stop()

        def on_before_nack_message(rmq_message: BaseRMQMessage, spider: RMQSpider):
            logging.info('BEFORE NACK_CALLBACK %s:%s', spider.name, rmq_message.deliver.delivery_tag)

        def on_after_nack_message(rmq_message: BaseRMQMessage, spider: RMQSpider):
            nonlocal successfully_handled
            successfully_handled = True

            logging.info('AFTER NACK_CALLBACK %s:%s', spider.name, rmq_message.deliver.delivery_tag)
            crawler.stop()

        dispatcher.connect(on_before_ack_message, CustomSignals.before_ack_message)
        dispatcher.connect(on_after_ack_message, CustomSignals.after_ack_message)
        dispatcher.connect(on_before_nack_message, CustomSignals.before_nack_message)
        dispatcher.connect(on_after_nack_message, CustomSignals.after_nack_message)
        crawler.crawl(MySpider)
        crawler.start()

        assert successfully_handled

        queue = rabbit_setup.rabbit_channel.queue_declare(queue=QUEUE_NAME, durable=True)
        assert queue.method.message_count == 1