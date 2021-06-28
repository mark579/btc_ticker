import time
import requests
import os

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.interface.serial import noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

if (os.environ.get('DEV', None)):
  from mocks import mock_spi, mock_max7219, mock_canvas, mock_text, mock_show_message

  spi = mock_spi
  max7219 = mock_max7219
  canvas = mock_canvas
  text = mock_text
  show_message = mock_show_message

TICKER_API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=8, block_orientation=-90,
                 rotate=0, blocks_arranged_in_reverse_order=False)

def get_latest_btc_price():
  try:  
    response = requests.get(TICKER_API_URL)
    response_json = response.json()
    return "${:,.0f}".format(float(response_json['bpi']['USD']['rate_float'])), 1
  except requests.exceptions.ConnectionError:
    return 'Could not get the current price :(', 2

def get_joke():
  try:
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    response_json = response.json()
    joke = response_json['setup'] + '.....' + response_json['punchline']
    #joke = joke.replace("’", "'").replace("‘", "'")
    joke = joke.encode("ascii", errors="ignore").decode()
    return joke, 2
  except requests.exceptions.ConnectionError:
    return 'Could not get a joke :(', 2 

def main():
  
  last_price = -1
  i = 0
  while True:
    i = i+1
    message = ""
    text_type = 0

    if(i >= 50):
      i = 0
      message, text_type = get_joke()
    else:
      message, text_type = get_latest_btc_price()
    
    if message == -1:
      message = ":( No internet"
      show_message(device, message, fill="white", font=proportional(CP437_FONT),scroll_delay=0.05)
    else:  
      if text_type == 1:
        with canvas(device) as draw:
            text(draw, (0, 0), message, fill="white", font=proportional(CP437_FONT)) 
            time.sleep(5)
      elif text_type == 2:
        show_message(device, message, fill="white", font=proportional(CP437_FONT),scroll_delay=0.03)
main()
