import time
from signal_generator import run_signals

def main():
    while True:
        try:
            run_signals()
            time.sleep(60)
        except Exception as e:
            print('Error:', e)
            time.sleep(30)

if __name__ == '__main__':
    main()