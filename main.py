# import module
import sys

from pdf2image import convert_from_path
from PIL import Image
from PIL import ImageFilter

# PDF Qualities
# Full Cards 1 - 94, 109 - 110
# Half Cards 95 - 108
starting_page = 95
ending_page = 108

# Page Qualities
rows_per_page = 3
columns_per_page = 3
cards_per_page = rows_per_page * columns_per_page

# Card qualities (default resolution: 1700, 2200)
# Full Cards
# origin = 79, 29
# width = 503
# height = 703
# x_offset = 520
# y_offset = 720
# Mini Cards
origin = 168, 131
width = 325
height = 499
x_offset = 519
y_offset = 720

# Store Pdf with convert_from_path function
images = convert_from_path('PnP (Major and Minor).pdf', first_page=starting_page, last_page=ending_page)
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
    # Go through each of the 9 cards on the page
    # X is for rows of cards.
    for x in range(3):
        # Y is for columns of cards.
        for y in range(3):
            card = image.crop((selection[0], selection[1], selection[0] + width, selection[1] + height))
            if not is_blank(card.load()):
                # card_count += 1
                # card_name = "cards/"
                # if card_count < 100:
                #     card_name += "0"
                # if card_count < 10:
                #     card_name += "0"
                # card_name += str(card_count)
                if i % 2 == 0:
                    # card_name += "_front.jpg"
                    fronts.append(card)
                    # card.save(card_name)
                else:
                    # card_name += "_back.jpg"
                    backs.append(card)
                    # card.save(card_name)
            selection[0] = selection[0] + x_offset
        selection[0] = origin[0]
        selection[1] = selection[1] + y_offset

for i in range(len(fronts)):
    cards.append(fronts[i])
    cards.append(backs[i])

if cards.__sizeof__() > 1:
    cards[0].save('ReformattedPDF.pdf', save_all=True, append_images=cards[1:])
