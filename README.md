# RabbitMQ Pika daemon

## Quick start

NOTICE this package is only supporting python3.5 +


```
import pika_client

pika_client.create(url=config.AMQP_URL,
                   port=config.AMQP_PORT,
                   username=config.AMQP_USERNAME,
                   password=config.AMQP_PASSWORD,
                   payload_callback=dispatcher).run(queue=config.AMQP_QUEUE)
```

### Repackage pip package
`python3 setup.py bdist_wheel bdist_egg`
