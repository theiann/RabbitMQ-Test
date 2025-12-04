import pika, sys, os, time


rabbitmq_host = 'murabbitmq.ghhsdadqfycscha9.northcentralus.azurecontainer.io'
rabbitmq_port = "5672"
rabbitmq_username = 'gadtbg'
rabbitmq_password = 'gadtbg'
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

    print("running")


    method_frame, header_frame, body = channel.basic_get(queue='gadtbg_STEP0', auto_ack=False)

    if method_frame:
        print(f"Received message: {body.decode()}")
        
        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned from the queue.")

    
    connection.close()

if __name__ == "__main__":
    main()




