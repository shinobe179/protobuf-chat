import socket

import argparse
import protobuf_chat_pb2

def socket_handler(me, dst_ip, dst_port):
    peer = protobuf_chat_pb2.Chat()

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((dst_ip, dst_port))
    print('[*] Connect to {}:{}.'.format(dst_ip, dst_port))

    while(1):
        raw_recv_data = soc.recv(1024)
        print('raw recieve data:', raw_recv_data)
        peer.ParseFromString(raw_recv_data)
        recv_data = peer.content
        print('Server>', recv_data)
        me.content = input('Client> ')
        #if me.content == 'bye':
        #    print('[*] Bye.')
        #    soc.close()
        #    break
        send_data = me.SerializeToString()
        print('raw send data:', send_data)
        soc.send(send_data)
        if me.content == 'bye':
            print('[*] Bye.')
            soc.close()
            break

def main():
    # argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('name', help='')
    parser.add_argument('--dst-ip', help='', default='localhost')
    parser.add_argument('--dst-port', help='', default=17917)
    args = parser.parse_args()

    chat = protobuf_chat_pb2.Chat()
    chat.name = args.name

    socket_handler(chat, args.dst_ip, int(args.dst_port))

if __name__ == '__main__':
    main()
