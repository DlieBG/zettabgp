from adapters.rabbitmq import RabbitMQAdapter
from parser import BGPParser
import time, sys

parser = BGPParser()

RabbitMQAdapter(
    parser=parser,
)

while True:
    for line in sys.stdin:
        parser.parse(
            line=line,
        )

    time.sleep(1)
