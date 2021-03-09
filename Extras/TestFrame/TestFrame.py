from PIL import Image,ImageDraw,ImageFont
import random 
from waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()
img = Image.open("test-frame.BMP")
img = img.convert(mode='1',dither=Image.FLOYDSTEINBERG)
epd.display(epd.getbuffer(img))
epd.sleep()
exit()