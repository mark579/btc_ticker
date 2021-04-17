import time
import requests

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

TICKER_API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=8, block_orientation=-90,
                 rotate=2, blocks_arranged_in_reverse_order=False)

def get_latest_btc_price():
  
  response = requests.get(TICKER_API_URL)
  response_json = response.json()
  
  return float(response_json['bpi']['USD']['rate_float'])

def main():
  
  last_price = -1
  
  while True:
    price = get_latest_btc_price()
  
    if price != last_price:
      pshow_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
      last_price = price

main()