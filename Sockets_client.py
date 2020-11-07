import socket
import sys
import pickle
from time import sleep

to_send = []


def show_tasks():
    index = 1
    to_send = ['h']
    tmp = pickle.dumps(to_send)
    s.sendall(tmp)

    data = pickle.loads(s.recv(4096))
    for i in data:
        print('%d. %s. Priorytet: %s' % (index, i[0], i[1]))
        index += 1
    print('\n')
    sleep(1.5)
    return 0


def add_task():
    print('Podaj tresc zadania: \n')
    content = raw_input()
    print('Podaj priorytet zadania: \n'
          '3. Nie pilne \n'
          '2. Pilne \n'
          '1. Bardzo pilne \n')
    priority = raw_input()
    to_send = ['j', content, priority]
    tmp = pickle.dumps(to_send)
    s.sendall(tmp)
    data = s.recv(1024)
    print >> sys.stderr, '"%s"' % data
    sleep(1.5)
    return 0


def delete_task():
    print('Podaj ID zadania do usuniecia: \n')
    content = raw_input()
    to_send = ['k', content]
    tmp = pickle.dumps(to_send)
    s.sendall(tmp)
    data = s.recv(1024)
    print >> sys.stderr, '"%s"' % data
    sleep(1.5)


def show_exact_priority():
    index = 1
    print('Zadania o jakim priorytecie chcesz wyswietlic? \n')
    content = raw_input()
    to_send = ['l', content]
    tmp = pickle.dumps(to_send)
    s.sendall(tmp)
    data = pickle.loads(s.recv(4096))
    for i in data:
        print('%d. %s. Priorytet: %s' % (index, i[0], i[1]))
        index += 1
    print('\n')
    sleep(1.5)


def menu_loop():
    choice = None
    while True:
        print('1. Wyswietl zadania.\n')
        print('2. Dodaj zadanie.\n')
        print('3. Usun zadanie.\n')
        print('4. Wyswietl zadania z danym priorytetem.\n')
        print('5. Wyjscie.\n')
        choice = raw_input("Co chcialbys zrobic?\n")

        if choice == '1':
            show_tasks()

        elif choice == '2':
            add_task()

        elif choice == '3':
            delete_task()

        elif choice == '4':
            show_exact_priority()

        elif choice == '5':
            sys.exit()


# main function
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print ('Usage : python telnet.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host'

    menu_loop()


    try:

        # Send data
        message = 'Message sent.'
        print >> sys.stderr, 'sending "%s"' % message
        s.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = s.recv(1024)
            amount_received += len(data)
            print >> sys.stderr, 'received "%s"' % data

    finally:
        print >> sys.stderr, 'closing socket'
        s.close()
