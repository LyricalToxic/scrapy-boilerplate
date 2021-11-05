import json

from rmq.extensions import RPCTaskConsumer
from rmq.spiders import TaskToSingleResultSpider
from scrapy import Request

from rmq.utils.decorators import rmq_callback, rmq_errback


class ExampleSpider(TaskToSingleResultSpider):

    name ="example_spider"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.task_queue_name = spider.settings["RABBITMQ_EXAMPLE_TASKS"]
        spider.completion_strategy = RPCTaskConsumer.CompletionStrategies.REQUESTS_BASED
        return spider

    def next_request(self, delivery_tag, message_body):
        parsed_body = json.loads(message_body)
        self.processing_tasks.set_code(delivery_tag, 1)
        self.processing_tasks.set_status(delivery_tag, 12)
        self.processing_tasks.set_message(delivery_tag, "Test_message")
        self.processing_tasks.add_extra_data(delivery_tag, {"key1":"value1"})
        try:
            raise Exception("test exception")
        except Exception as e:
            self.processing_tasks.set_exception(delivery_tag, e)
        return Request(url="https://ident.me", callback=self.parse, errback=self.errback)


    @rmq_callback
    def parse(self, response):
        yield None
        print(response.body)
        return

    @rmq_errback
    def errback(self, failure):
        print(failure)
