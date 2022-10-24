# import module
import sys

from PIL.Image import Resampling
from pdf2image import convert_from_path
from PIL import Image
from PIL import ImageFilter

# PDF Qualities
# Full Cards 1 - 94, 109 - 110
# Half Cards 95 - 108
starting_page = 1
ending_page = 6
dpi = 300

# Page Qualities
rows_per_page = 3
columns_per_page = 3
cards_per_page = rows_per_page * columns_per_page

# Card qualities (300 DPI import)
# Full Cards
origin = 119, 44
width = 754
height = 1054
x_offset = 779
y_offset = 1079
real_width = 2.75
real_height = 3.75
# Mini Cards
# origin = 252, 197
# width = 488
# height = 748
# x_offset = 779
# y_offset = 1079
# real_width = 1.875
# real_height = 2.75

# Store Pdf with convert_from_path function
images = convert_from_path('BattleCON V4 Errata.pdf', dpi=dpi, first_page=starting_page, last_page=ending_page)
cards = []
fronts = []
backs = []


def is_blank(img):
    offset = 50
    white = (255, 255, 255)
    return img[offset, offset] == img[width - offset, offset] == img[offset, height - offset] == img[width - offset, height - offset] == white


# Go through each page in the pdf.
if ending_page > images.__sizeof__():
    print("PDF is not long enough for the requested range.")
    sys.exit()

card_count = 0

for i in range(ending_page - starting_page + 1):
    # Save pages as images in the pdf
    image = images[i]
    selection = [origin[0], origin[1]]
    # Go through each of the cards on the page
    # X is for rows of cards.
    for x in range(rows_per_page):
        # Y is for columns of cards.
        for y in range(columns_per_page):
            card = image.crop((selection[0], selection[1], selection[0] + width, selection[1] + height))
            if not is_blank(card.load()):
                if i % 2 == 0:
                    fronts.append(card.resize((int(real_width * dpi), int(real_height * dpi)), Resampling.LANCZOS))
                else:
                    backs.append(card.resize((int(real_width * dpi), int(real_height * dpi)), Resampling.LANCZOS))
            selection[0] = selection[0] + x_offset
        selection[0] = origin[0]
        selection[1] = selection[1] + y_offset

for i in range(len(fronts)):
    cards.append(backs[i])
    cards.append(fronts[i])

if cards.__sizeof__() > 1:
    cards[0].save('out/ReformattedPDF.pdf', save_all=True, append_images=cards[1:], quality=100, resolution=dpi)
