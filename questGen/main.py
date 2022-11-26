import cProfile
import io
import os
import pstats

from pipelines import pipeline
import pika
from sqlalchemy_orm import ImageSQL, QuestionAnsSQL


class QuestionGen:
    def __init__(self):
        # Define Pipeline
        self.nlp = pipeline("e2e-qg")

    def processText(self, text):
        """
        Process and print the stored text
        """
        return self.nlp(text)


# Connection for Question Generator (Listen)
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=600,
                                                               blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue="QuestGen", durable=True)


def queueAnswerJob(questionID):
    # Connection for Answer Generator (Send)
    connection2 = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=600,
                                                                    blocked_connection_timeout=300))
    channel2 = connection2.channel()
    channel2.queue_declare(queue="AnswerGen", durable=True)

    channel2.basic_publish(
        exchange="",  # This publishes the thing to a default exchange
        routing_key="AnswerGen",
        body=questionID,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
    connection2.close()
    print("Inserted AnsJob" + questionID)


# Initiate Question Generation Pipeline
QG = QuestionGen()

# Initiate SQLConnector
IMG_control = ImageSQL("root", "root", "db", "3306", "02db")
QA_control = QuestionAnsSQL("root", "root", "db", "3306", "02db")


def callback(ch, method, properties, body):
    # Decode the ID
    ID = body.decode()
    if 'test' in ID:  # Testing Route
        # Remove test
        ID = ID.replace("test", "")
        # Retrieve the caption
        caption = IMG_control.findById(ID)[2]

        # Generate Questions
        numberofCharacters = len(caption)
        pr = cProfile.Profile()
        pr.enable()
        result = QG.processText(caption)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.strip_dirs()  # Remove directory path
        ps.sort_stats('tottime')
        ps.print_stats()

        if not os.path.exists("./TestResults/"):
            os.makedirs("./TestResults/")

        filename = "./TestResults/test_" + ID + ".txt"
        with open(filename, 'w+') as f:
            f.write("Number of characters: " + str(numberofCharacters) +
                    "\nNumber of Questions Generated: " + str(len(result)) +
                    "\n" + s.getvalue())

        for question in result:
            # print("Question: " + question)
            print("Completed" + ID)
    else:  # Commercial Route
        # Retrieve the caption
        caption = IMG_control.findById(ID)[2]
        # print("Caption: " + caption)
        # Generate Questions
        result = QG.processText(caption)
        # Insert Questions
        for question in result:
            # print("Question: " + question)
            # Insert question into DB
            questionID = QA_control.insertQuestion(ID, question)[0]
            # print(questionID)
            # Generate Answer Queue Job
            queueAnswerJob(str(questionID))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="QuestGen", on_message_callback=callback)

print("ReadyToConsume")

channel.start_consuming()
