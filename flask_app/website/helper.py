import pika


def captionGen(imageID):
    connection3 = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel3 = connection3.channel()
    channel3.queue_declare(queue='CaptionGen', durable=True)

    channel3.basic_publish(
        exchange='',  # This publishes the thing to a default exchange
        routing_key='CaptionGen',
        body=imageID,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    connection3.close()
