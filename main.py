# import module
from pdf2image import convert_from_path
from PIL import Image
from PIL import ImageFilter

# Store Pdf with convert_from_path function
images = convert_from_path('PnP (Major and Minor).pdf')

for i in range(len(images)):
    # Save pages as images in the pdf
    image = images[i]
    origin = 79, 29
    width = 503
    height = 703
    x_offset = 17
    y_offset = 17
    selection = [origin[0], origin[1]]
    for x in range(3):
        for y in range(3):
            cropped_card = image.crop((selection[0], selection[1], selection[0] + width, selection[1] + height))
            cropped_card.save('cards/card_' + str((x * 3 + y + (int(i / 2) * 9))) + '_' + ('front' if i % 2 == 0 else 'back') + '.jpg', quality=100)
            selection[0] = selection[0] + width + x_offset
        selection[0] = origin[0]
        selection[1] = selection[1] + height + y_offset
