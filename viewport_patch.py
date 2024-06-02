# flake8: noqa

# This is a monkey patch of refresh in luma.core.virtual
# It adds an ability to draw a logo on the first panel of the display
# Because of patching flake8 and pylance are ignored in here

from PIL import Image, ImageDraw


def draw_logo(im, logo_file):
    eraser = Image.new('1', (8, 8))
    im.paste(eraser, (0, 0))
    draw = ImageDraw.Draw(im)
    img = Image.open(logo_file)
    draw.bitmap((0, 1), img, fill='white')


def refresh(self):
    should_wait = False
    for hotspot, xy in self._hotspots:
        if hotspot.should_redraw() and self.is_overlapping_viewport(hotspot, xy):
            pool.add_task(hotspot.paste_into,
                          self._backing_image, xy)  # type: ignore
            should_wait = True

    if should_wait:
        pool.wait_completion()  # type: ignore

    im = self._backing_image.crop(box=self._crop_box())
    if self._dither:
        im = im.convert(self._device.mode)

    if hasattr(self, 'logo') and self.logo:
        draw_logo(im, self.logo)
    self._device.display(im)
    del im
