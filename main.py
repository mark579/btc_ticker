from ticker import Ticker


def main():
    try:
        Ticker("./config").start()
    except KeyboardInterrupt:
        print('Shutting Down.')


main()
