# btc_ticker
Simple Bitcoin Ticker with a sense of Humor. 

This uses the Luma Library to display to a MAX7219 display that would be connected to a Raspberry PI

## Config
Configuration is done in the config.yaml file. 

Currently only one currency and vs_currency is supported at a time

## Usage

Once your MAX7219 is connected to your raspberry PI with an internet connection, run main. 

```bash
pip install -r requirements.txt
python3 main.py
```

There are different modes for ways to display the information. 

### Console

Displays display methods calls in the console. 

```bash
MODE=CONSOLE python3 main.py
```

### Pygame

Displays information in a Pygame Emulator. 

This is useful for when you are in an environment other than a raspberry pi and you do not have a SPI/MAX7219 physical device. 

```bash
MODE=PYGAME python3 main.py
```
