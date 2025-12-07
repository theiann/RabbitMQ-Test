import pika, sys, os, time
import xml.etree.ElementTree as ET

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

    # parse message
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

if __name__ == "__main__":
    main()




