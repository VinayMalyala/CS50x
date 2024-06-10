import qrcode
img = qrcode.make("https://youtu.be/BddP6PYo2gs?feature=shared")
img.save("qr.png", "PNG")
