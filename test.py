import os

import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps

# infile = r"C:\Users\Роман\Downloads\G0051586.jpg"
infile = r"C:\Users\Роман\Downloads\1.png"
# infile = r"C:\Users\Роман\Downloads\plakat.jpg"
logo_file = r"C:\vKalendare\GitHub\django_project\django_project\mysite\static\logo\vkalendare_logo_only.png"
new_text = 'Информационная поддержка: Проект "Афиша вКалендаре" www.vkalendare.com'

im = Image.open(infile)
logo = Image.open(logo_file)
# im = Image.open(StringIO.StringIO(buffer))


# font = ImageFont.load_default()
# draw.text((x, y),"Sample Text",(r,g,b))
# draw.text((0, 0),"Sample Text",(255,255,255),font=font)
# draw.line((0, 10, 200, 200), fill=100, width=100)
# q = ImageOps.expand(im, border=100, fill=100)
(width, height) = im.size
p_height = int(height*0.05)
ltrb_border = (0, 0, 0, p_height)
im_with_border = ImageOps.expand(im, border=ltrb_border, fill='black')
print('border size:', width, p_height)

size = int(p_height*0.8), int(p_height*0.8)
logo.thumbnail(size, Image.ANTIALIAS)

ttf = r'C:\vKalendare\GitHub\django_project\django_project\mysite\static\fonts\roboto\Roboto-Regular.ttf'
font = ImageFont.truetype(ttf, int(height*0.025))
if font.getsize(new_text)[0] > width:
    q = width / font.getsize(new_text)[0]
    print(q)
    font = ImageFont.truetype(ttf, int(height * 0.022 * q))

draw = ImageDraw.Draw(im_with_border)
# PIL.ImageFont.ImageFont.getsize(text)
print(font.getsize(new_text))
draw.text((width*0.01+p_height, height+(p_height/2 - font.getsize(new_text)[1]/2)), new_text, fill='white', font=font)
# draw.text((10, height), "Support: vKalendare.com", fill='black', font=font)

im_with_border.paste(logo.convert('RGB'), (int(width*0.01), int(height+p_height*0.1)), logo)
im_with_border.show()

# img.save('C:\\tmp\\sample-out.jpg', "JPEG")

# size = 128, 128
# outfile = os.path.splitext(infile)[0] + "_thumbnail.jpg"
# im.thumbnail(size, Image.ANTIALIAS)
# im.save(outfile, "JPEG")