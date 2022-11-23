import os
import sys

from blip_vqa import blip_vqa
from blip import blip_decoder
import torch
import pika
from models import ImageSQL, QuestionAnsSQL
from PIL import Image
from torchvision import transforms
from torchvision.transforms import InterpolationMode


# import requests


def VQA():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=600,
                                                                   blocked_connection_timeout=300))  # Connect to CloudAMQP
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue='CaptionGen', durable=True)  # Declare a queue
    channel.queue_declare(queue='AnswerGen', durable=True)

    # Initiate SQLConnector
    IMG_control = ImageSQL("root", "root", "db", "3306", "02db")
    QA_control = QuestionAnsSQL("root", "root", "db", "3306", "02db")

    def captionGen(imageID):
        connection2 = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
        channel2 = connection2.channel()
        channel2.queue_declare(queue='QuestGen', durable=True)

        channel2.basic_publish(
            exchange='',  # This publishes the thing to a default exchange
            routing_key='QuestGen',
            body=imageID,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        connection2.close()

    def answerGen(questionID):
        connection3 = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
        channel3 = connection3.channel()
        channel3.queue_declare(queue='AnswerGen', durable=True)

        channel3.basic_publish(
            exchange='',  # This publishes the thing to a default exchange
            routing_key='AnswerGen',
            body=questionID,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        connection3.close()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_demo_image(image_url, image_size, device):
        # img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
        raw_image = Image.open(image_url, mode='r').convert('RGB')

        transform = transforms.Compose([
            transforms.Resize((image_size, image_size), interpolation=InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ])
        image = transform(raw_image).unsqueeze(0).to(device)
        return image

    # ch, method, properties, body
    def caption_callback(ch, method, properties, body):
        image_size = 384
        ID = int(body.decode())
        image = IMG_control.findById(ID)
        image_url = image[1]
        print(image_url)
        image_file = load_demo_image(image_url, image_size, device)
        # image_url = load_demo_image(image_size=image_size, device=device)

        model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'

        model = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
        model.eval()
        model = model.to(device)
        with torch.no_grad():
            # beam search
            caption = model.generate(image_file, sample=False, num_beams=3, max_length=20, min_length=5)
            # nucleus sampling
            # caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5)
            print(caption)
            result = IMG_control.updatecaption(ID, caption[0])
            captionGen(str(result[0]))
            print('caption: ' + caption[0])

    # ch, method, properties, body
    def answer_callback(ch, method, properties, body):
        image_size = 480
        message = body.decode()
        image = ImageSQL.findById(message[0])
        QA = QA_control.getDataByID(message[1])
        image_url = image[1]
        # image_url = load_demo_image(image_size=image_size, device=device)

        model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_vqa_capfilt_large.pth'

        model = blip_vqa(pretrained=model_url, image_size=image_size, vit='base')
        model.eval()
        model = model.to(device)

        question = QA[2]
        # question = 'where is the woman sitting?'

        with torch.no_grad():
            answer = model(image_url, question, train=False, inference='generate')
            QA_control.updateAnswers(message[1], answer[0])
            answerGen(str(message[1]))
            print('answer: ' + answer[0])

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='CaptionGen', on_message_callback=caption_callback)
    channel.basic_consume(queue='AnswerGen', on_message_callback=answer_callback)
    print(' [*] VQA container waiting for messages.')
    channel.start_consuming()


# caption_callback()
# answer_callback()
if __name__ == '__main__':
    try:
        VQA()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
