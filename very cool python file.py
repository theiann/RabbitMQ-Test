import pika, sys, os, time, math
import xml.etree.ElementTree as ET

rabbitmq_host = 'murabbitmq.ghhsdadqfycscha9.northcentralus.azurecontainer.io'
rabbitmq_port = "5672"
rabbitmq_username = 'imchrc'
rabbitmq_password = 'imchrc'
rabbitmq_vhost = '/'

rabbitmq_username2 = 'gadtbg'
rabbitmq_password2 = 'gadtbg'
credentials2 = pika.PlainCredentials(rabbitmq_username2, rabbitmq_password2)

credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)

parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host=rabbitmq_vhost,
    credentials=credentials
)

parameters2 = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host=rabbitmq_vhost,
    credentials=credentials2
)


def main():

    # receiving message 
    # ===========================================================================
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    print("running")


    method_frame, header_frame, body = channel.basic_get(queue='imchrc_STEP0', auto_ack=False)

    if method_frame:
        print(f"Received message: {body.decode()}")
        
        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned from the queue.")

    
    connection.close()
    # ===========================================================================

    print()

    # parse message from step0
    # ===========================================================================
    tree = body.decode()
    tree = ET.ElementTree(ET.fromstring(tree))
    root = tree.getroot()
    operandList = []
    print(root)
    print("root tag:", root.tag)

    for item in root.findall('Operand'):
        print(f"Item value: {item.text}")
        operandList.append(int(item.text))
    
    if (root.tag == "Add"):
        result = operandList[0] + operandList[1]
    
    else:
        result = operandList[0] * operandList[1]
    
    print("result:", result)
    # ===========================================================================

    print()

    # push new xml message to step1
    # ===========================================================================
    body = (f"<Factorial><Operand>{result}</Operand></Factorial>")
    print(body)

    connection2 = pika.BlockingConnection(parameters2)
    channel2 = connection2.channel()

    channel2.basic_publish(exchange='STEP1_WORK_EXCHANGE', routing_key='gadtbg', body=body)
    print("sent message")
    # ===========================================================================

    print()

    # parse message from step1
    # ===========================================================================
    method_frame, header_frame, body = channel2.basic_get(queue='gadtbg_STEP1', auto_ack=False)

    tree = body.decode()
    tree = ET.ElementTree(ET.fromstring(tree))
    root = tree.getroot()
    result = -1

    if method_frame:
        print(f"Received message: {body.decode()}")
        
        channel2.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned from the queue.")


    print(root)
    print("root tag:", root.tag)

    for item in root.findall('Operand'):
        print(f"result value: {item.text}")
        result = int(item.text)
    # ===========================================================================

    print()

    # compute factorial for result item (pulled from step1)
    # ===========================================================================
    # ===========================================================================
    

if __name__ == "__main__":
    main()




