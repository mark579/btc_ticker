from ticker import Ticker


def main():
    try:
        Ticker().start()
    except KeyboardInterrupt:
        print('Shutting Down.')


main()
