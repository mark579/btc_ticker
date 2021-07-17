# crypto_ticker

Simple Crypto Ticker with a sense of Humor.

This uses the Luma Library to display to a MAX7219 display that would be connected to a Raspberry PI

## Config

Configuration is done in the config.yaml file.

Select as many cryptos as you'd like in the config.yaml. Only one vs_currency is supported, and it only shows in $'s right now. So really it's just usd. 

There are currently logos that will show for Bitcoin, Dogecoin, and Ethereum. If it's not one of those a logo will not display on the left most 8x8 panel. 

The selected IDs need to exist in the [Coingeck API](https://api.coingecko.com/api/v3/coins/list).

Then each one will drop in, and display the price and 24H price change. At the end of showing all cryptos. A joke will be displayed if enabled.

## Usage

Once your MAX7219 is connected to your raspberry PI with an internet connection, run main.

```bash
pip install -r requirements.txt
python3 main.py
```

There are different modes for ways to display the information.

### Console

Displays display methods calls in the console. This is useful for headless environments which don't have a way to display the information other than the console.

```bash
MODE=CONSOLE python3 main.py
```

Example output:

```
⟩ MODE=CONSOLE python3 main.py
{'ticker': {'crypto': 'bitcoin', 'vs_currency': 'usd', 'tell_jokes': True}}
display_message(message:Bitcoin, type:MessageType.FALLING, logo:/home/mark/github/btc_ticker/images/logos/bitcoin-8px.bmp, delay:15
display_message(message:$31,823.0 -0.69%%, type:MessageType.BOUNCING, logo:/home/mark/github/btc_ticker/images/logos/bitcoin-8px.bmp, delay:30
display_message(message:$31,823.0 -0.69%%, type:MessageType.BOUNCING, logo:/home/mark/github/btc_ticker/images/logos/bitcoin-8px.bmp, delay:30
display_message(message:$31,823.0 -0.69%%, type:MessageType.BOUNCING, logo:/home/mark/github/btc_ticker/images/logos/bitcoin-8px.bmp, delay:30

```

### Pygame

Displays information in a Pygame Emulator.

This is useful for when you are in an environment other than a raspberry pi and you do not have a SPI/MAX7219 physical device.

```bash
MODE=PYGAME python3 main.py
```
Here is a screenshot of window with pygame emulator running


![Pygame Emulator](./images/readme/pygame_emulator.gif)
