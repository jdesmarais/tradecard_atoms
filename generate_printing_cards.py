from alive_progress import alive_bar
import glob
from math import ceil, floor
import os
from pathlib import Path
from PIL import Image

PAPER_FORMAT_TO_PX_300DPI_MAP = {
    "A6" : (1240, 1748),
    "A5" : (1748, 2480),
    "A4" : (2480, 3508),
    "A3" : (3508, 4960),
    "A2" : (4960, 7016),
    "A1" : (7016, 9933),
    "A0" : (9933, 14043)
}

def get_n_margin(paper_px, card_px):
    n = int(floor(float(paper_px) / float(card_px)))

    margin = floor( (float(paper_px) - n * float(card_px)) / float(n+1) )
    margin_left = margin
    margin_right = paper_px - n * (margin + card_px)

    return n, margin, margin_left, margin_right


if __name__ == "__main__":

    # inputs
    printing_format = "A4"
    card_dirpath = "outputs"
    output_dirpath = "outputs/sheets"
    front_card_filepath = "assets/front.png"
    generate_front_card = True
    show = False
    save = True
    save_as_one_file = True

    if save:
        if os.path.exists(output_dirpath):
            if not os.path.isdir(output_dirpath):
                raise Exception(f"The output path {output_dirpath} exists but is not a directory, please fix it")
        else :
            os.mkdir(output_dirpath)


    img_card_filepath = glob.glob(card_dirpath+'/*.png')
    print(f"Expecting a total of {len(img_card_filepath)} cards to be printed")

    #                         margin_x
    #                            |                  
    #                            v                  
    # +---------------------------+                 
    # | +-----+  +-----+  +-----+ |<------- margin_y
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | +-----+  +-----+  +-----+ |                 
    # | +-----+  +-----+  +-----+ |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | |     |  |     |  |     | |                 
    # | +-----+  +-----+  +-----+ |                 
    # +---------------------------+                 

    paper_px_size = PAPER_FORMAT_TO_PX_300DPI_MAP[printing_format]
    card_px_size = (768, 1276)

    nx, margin_x, margin_x_left, margin_x_right = get_n_margin(paper_px_size[0], card_px_size[0])
    ny, margin_y, margin_y_top, margin_y_bottom = get_n_margin(paper_px_size[1], card_px_size[1])

    nb_cards_per_paper = int(nx * ny)
    print(f"Expecting {nb_cards_per_paper} cards per paper sheet")

    nb_paper_sheets = ceil(len(img_card_filepath)/float(nb_cards_per_paper))
    print(f"Expecting {nb_paper_sheets} paper sheets")


    # FRONT CARD IMAGE GENERATION
    if generate_front_card:
        print("Generating front-card image")
        front_card_img = Image.open(front_card_filepath).convert("RGBA")
        front_card_sheet_img = Image.new("RGBA", paper_px_size, (255,255,255))

        for i in range(0, nx*ny):
            k = i
            x = k%nx
            y = floor(k/nx)

            border_x = margin_x_right + x * (card_px_size[0] + margin_x)
            border_y = margin_y_top + y * (card_px_size[1] + margin_y)
            front_card_sheet_img.paste(front_card_img, (border_x, border_y), front_card_img)

        if show:
            front_card_sheet_img.show()


    # CARD IMAGE GENERATION
    print("Generating atom card images")
    sheet_imgs = []

    with alive_bar(nb_paper_sheets) as bar:

        for i in range(0, nb_paper_sheets):

            if generate_front_card and save_as_one_file:
                sheet_imgs.append(front_card_sheet_img)
    
            sheet_imgs.append(Image.new("RGBA", paper_px_size, (255,255,255)))
    
            for j in range(i*nb_cards_per_paper, min((i+1)*nb_cards_per_paper, len(img_card_filepath))):
                k = j%(nx*ny)
                x = k%nx
                y = floor(k/nx)

                border_x = margin_x_left + x * (card_px_size[0] + margin_x)
                border_y = margin_y_top + y * (card_px_size[1] + margin_y)

                card_img = Image.open(img_card_filepath[j]).convert("RGBA")

                sheet_imgs[-1].paste(card_img, (border_x, border_y))

            if show:
                sheet_imgs[-1].show()

            bar()

    # SAVE OUTPUT
    if save:
        if save_as_one_file:

            sheet_output_path = Path(output_dirpath) / f"all.pdf"        
            print(f"Saving images as one PDF {sheet_output_path}")
            sheet_imgs[0].save(
                sheet_output_path, "PDF" ,resolution=100.0, save_all=True, append_images=sheet_imgs[1:]
            )

        else:
            print("Saving images as PDF")
            if generate_front_card:
                sheet_imgs.insert(0, front_card_sheet_img)

            with alive_bar(len(sheet_imgs)) as bar:
                for i in range(0, len(sheet_imgs)):        
                    sheet_output_path = Path(output_dirpath) / f"sheet_{i}.pdf"
                    sheet_imgs[-1].save(sheet_output_path, 'PDF', quality=100)
                    bar()