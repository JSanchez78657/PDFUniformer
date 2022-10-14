# import module
import sys

from pdf2image import convert_from_path
from PIL import Image
from PIL import ImageFilter

# PDF Qualities
starting_page = 1
ending_page = 6

# Page Qualities
rows_per_page = 3
columns_per_page = 3
cards_per_page = rows_per_page * columns_per_page

# Card qualities
origin = 79, 29
width = 503
height = 703
x_offset = 17
y_offset = 17

# Store Pdf with convert_from_path function
images = convert_from_path('BattleCON V4 Errata.pdf')
cards = []


def is_blank(img):
    offset = 50
    white = (255, 255, 255)
    return img[offset, offset] == img[width - offset, offset] == img[offset, height - offset] == img[width - offset, height - offset] == white


# Go through each page in the pdf.
if ending_page > images.__sizeof__():
    print("PDF is not long enough for the requested range.")
    sys.exit()

for i in range(starting_page - 1, ending_page):
    # Save pages as images in the pdf
    image = images[i]
    selection = [origin[0], origin[1]]
    # Go through each of the 9 cards on the page
    # X is for rows of cards.
    for x in range(3):
        # Y is for columns of cards.
        for y in range(3):
            # Mathematical bullshit to get correct indexes.
            # Each page has a 3x3 grid of cards with 9 cards total.
            # x and y are used to find the position of the card on a given page, each index incrementing by 2.
            # i is used to determine if the card is a front or back (even page or odd page) and to offset the index appropriately.
            # If it is a front (even), simply offset the index to reflect the card count.
            # If it is a back (odd), set the offset to be one more than the matching card on the previous page.
            index = (x * columns_per_page * 2) + (y * 2) + (i * cards_per_page if i % 2 == 0 else (i - 1) * cards_per_page + 1)
            card = image.crop((selection[0], selection[1], selection[0] + width, selection[1] + height))
            cards.insert(index, card)
            selection[0] = selection[0] + width + x_offset
        selection[0] = origin[0]
        selection[1] = selection[1] + height + y_offset

blanks = []
for card in cards:
    if is_blank(card.load()):
        blanks.append(card)

for card in blanks.__reversed__():
    cards.remove(card)

if cards.__sizeof__() > 1:
    cards[0].save('ReformattedPDF.pdf', save_all=True, append_images=cards[1:])
