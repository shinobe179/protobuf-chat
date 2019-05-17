import socket

import argparse
import protobuf_chat_pb2

def socket_handler(me, use_ip, use_port):
    peer = protobuf_chat_pb2.Chat()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((use_ip, use_port))
    s.listen(1)
    print('[*] Ready to listen.')
    soc, addr = s.accept()
    print('[*] Connected by {}:{}.'.format(addr[0], addr[1]))

    while(1):
        me.content = input('Server> ')
        send_data = me.SerializeToString()
        print('raw send data:', send_data)
        soc.send(send_data)
        raw_recv_data = soc.recv(1024)
        print('raw recieve data:', raw_recv_data)
        peer.ParseFromString(raw_recv_data)
        recv_data = peer.content
        if recv_data == 'bye':
            print('[*] Bye.')
            soc.close()
            break
        print('Client>', recv_data)

def main():
    # argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('name', help='')
    parser.add_argument('--use-ip', help='', default='localhost')
    parser.add_argument('--use-port', help='', default=17917)
    args = parser.parse_args()

    chat = protobuf_chat_pb2.Chat()
    chat.name = args.name

    socket_handler(chat, args.use_ip, int(args.use_port))

if __name__ == '__main__':
    main()
