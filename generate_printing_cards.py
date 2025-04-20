from alive_progress import alive_bar
import glob
from math import ceil, floor
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

    return n, margin


if __name__ == "__main__":

    # inputs
    printing_format = "A4"
    card_dirpath = "/Users/julien/Documents/Projects/tradecards_atom/outputs"
    output_dir = "/Users/julien/Documents/Projects/tradecards_atom/outputs/sheets"
    show_sheet = False
    save = True
    save_as_one_file = True

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

    nx, margin_x = get_n_margin(paper_px_size[0], card_px_size[0])
    ny, margin_y = get_n_margin(paper_px_size[1], card_px_size[1])

    nb_cards_per_paper = int(nx * ny)
    print(f"Expecting {nb_cards_per_paper} cards per paper sheet")

    nb_paper_sheets = ceil(len(img_card_filepath)/float(nb_cards_per_paper))
    print(f"Expecting {nb_paper_sheets} paper sheets")


    sheet_imgs = []

    # IMAGE GENERATION
    print("Generating images")
    with alive_bar(nb_paper_sheets) as bar:

        for i in range(0, nb_paper_sheets):
    
            sheet_imgs.append(Image.new("RGBA", paper_px_size, (255,255,255)))
    
            for j in range(i*nb_cards_per_paper, min((i+1)*nb_cards_per_paper, len(img_card_filepath))):
                border_x = margin_x + j%nx * (card_px_size[0] + margin_x)
                border_y = margin_y + j%ny * (card_px_size[1] + margin_y)

                card_img = Image.open(img_card_filepath[j]).convert("RGBA")

                sheet_imgs[-1].paste(card_img, (border_x, border_y))

            if show_sheet:
                sheet_imgs[-1].show()

            bar()

    # SAVE OUTPUT
    if save:
        if save_as_one_file:
            sheet_output_path = Path(output_dir) / f"all.pdf"        
            print(f"Saving images as one PDF {sheet_output_path}")
            sheet_imgs[0].save(
                sheet_output_path, "PDF" ,resolution=100.0, save_all=True, append_images=sheet_imgs[1:]
            )

        else:
            print("Saving images as PDF")
            with alive_bar(nb_paper_sheets) as bar:
                for i in range(0, nb_paper_sheets):        
                    sheet_output_path = Path(output_dir) / f"sheet_{i}.pdf"
                    sheet_imgs[-1].save(sheet_output_path, 'PDF', quality=100)
                    bar()