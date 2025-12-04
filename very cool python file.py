import pika, sys, os, time


rabbitmq_host = 'murabbitmq.ghhsdadqfycscha9.northcentralus.azurecontainer.io'
rabbitmq_port = "5672"
rabbitmq_username = 'imchrc'
rabbitmq_password = 'imchrc'
rabbitmq_vhost = '/'

credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)

parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host=rabbitmq_vhost,
    credentials=credentials
)

def main():

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='imchrc_STEP0')
    print("running")
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='imchrc_STEP0', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()




