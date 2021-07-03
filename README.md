# btc_ticker
Simple Bitcoin Ticker with a sense of Humor. 

This uses the Luma Library to display to a MAX7219 display that would be connected to a Raspberry PI

## Usage

Once your MAX7219 is connected to your raspberry PI with an internet connection, run main. 

```bash
pip install -r requirements.txt
python3 main.py
```

If you want to development while not on a Raspberry Pi setting the DEV environment variable will mock the interfaces for the display and show the text to the console. 

```bash
DEV=1 python3 main.py
```

