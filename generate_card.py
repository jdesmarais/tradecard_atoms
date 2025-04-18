from utils import write_text_in_box, draw_grid

from PIL import Image, ImageDraw, ImageFont

def generate_tradecard_image(
    background_img_path,
    atom_img_path,
    atom_title,
    atom_subgroup_title,
    picto_img_path,
    atom_kpis,
    atom_description):

    background_path = background_img_path

    atom_path = atom_img_path

    title_font_path = "/Library/Fonts/AdobeArabic-Regular.otf"
    title_font_size = 16*4
    title_text_position = (137.6,41.4-12)
    title_text = atom_title
    title_text_color = (0,0,0)

    subtitle_font_path = "/Library/Fonts/AdobeArabic-Italic.otf"
    subtitle_font_size = 10*4
    subtitle_text_position = (137.6,46.8+50)
    subtitle_text = atom_subgroup_title
    subtitle_text_color = (0,0,0)

    picto_path = picto_img_path
    picto_position = (int(117.6)-100, int(15))
    picto_color = (155,0,187) # purple
    # picto_color = (255,18,85) # pink
    # picto_color = (15,178,0)  # green

    atomic_font_path = "/Library/Fonts/AdobeArabic-Regular.otf"
    atomic_font_size = 10*4
    atomic_text_color = (255,255,255)

    atomic_number = atom_kpis[0]
    atomic_mass = atom_kpis[1]
    atomic_melting_temperature = atom_kpis[2]
    atomic_vaporisation_temperature = atom_kpis[3]
    atomic_discovery = atom_kpis[4]

    atomic_number_position = (330, 668)
    atomic_mass_position = (315, 720)
    atomic_melting_temperature_position = (380, 772)
    atomic_vaporisation_temperature_position = (455, 825)
    atomic_discovery_position = (465, 880)

    description_font_path = "/Library/Fonts/AdobeArabic-Regular.otf"
    description_font_size = 8*4
    description_color = (255,255,255)
    description = atom_description
    description_position = (65,970)
    description_box_size = (700-65, 250)


    # Load background image
    background_img = Image.open(background_path).convert("RGBA")
    img = Image.new("RGBA", background_img.size, (255,255,255))
    draw = ImageDraw.Draw(img)

    # Draw atom image
    atom_img = Image.open(atom_path).convert("RGBA")
    img.paste(atom_img, (31,31), atom_img)

    # Draw background
    img.paste(background_img, (0,0), background_img)
    

    # Draw title + subtitle
    title_font = ImageFont.truetype(title_font_path, title_font_size)
    draw.text(title_text_position, title_text, font=title_font, fill=title_text_color)

    subtitle_font = ImageFont.truetype(subtitle_font_path, subtitle_font_size)    
    draw.text(subtitle_text_position, subtitle_text, font=subtitle_font, fill=subtitle_text_color)


    # Draw picto
    picto_img = Image.open(picto_path).convert("RGBA")

    # Draw picto circle
    picto_x,picto_y = (picto_position[0] + picto_img.width/2, picto_position[1] + picto_img.height/2)
    picto_radius = picto_img.width / 2
    draw.ellipse((picto_x - picto_radius, picto_y - picto_radius, picto_x + picto_radius, picto_y + picto_radius),
                 fill=picto_color)

    # Draw picto logo
    img.paste(picto_img, picto_position, picto_img)


    if show_grid:
        draw_grid(draw, img.size)

    # Draw atomic numbers
    atomic_font = ImageFont.truetype(atomic_font_path, atomic_font_size)
    draw.text(atomic_number_position, atomic_number, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_mass_position, atomic_mass, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_melting_temperature_position, atomic_melting_temperature, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_vaporisation_temperature_position, atomic_vaporisation_temperature, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_discovery_position, atomic_discovery, font=atomic_font, fill=atomic_text_color)


    # Draw atomic description
    description_font = ImageFont.truetype(description_font_path, description_font_size)
    write_text_in_box(draw,
                      description,
                      description_box_size,
                      description_position,
                      description_font,
                      description_color)

    return img

if __name__ == "__main__":
    background_img_path = "/Users/julien/Documents/Projects/tradecards_atom/assets/background.png"
    atom_img_path = "/Users/julien/Documents/Projects/tradecards_atom/assets/img/hydrogene.png"
    atom_title = "Hydrogène (H)"
    atom_subgroup_title = "Non-métal"
    picto_img_path = "/Users/julien/Documents/Projects/tradecards_atom/assets/picto.png"
    atom_kpis = ["1", "1.01 g/mol", "-259°C", "-252°C", "1766"]
    atom_description = "L'hydrogène est le principal constituant du Soleil et de la plupart des étoiles (dont l'énergie provient de la fusion thermonucléaire de cet hydrogène), et de la matière interstellaire ou intergalactique. Sur Terre, il est surtout présent à l'état d'eau liquide, solide (glace) ou gazeuse (vapeur d'eau), mais on le trouve aussi dans les émanations de certains volcans sous la forme de H2 et de CH4 (méthane)."

    output_path="/Users/julien/Documents/Projects/tradecards_atom/outputs/hydrogene.png"

    show_grid = False
    show_result = False

    img = generate_tradecard_image(
        background_img_path,
        atom_img_path,
        atom_title,
        atom_subgroup_title,
        picto_img_path,
        atom_kpis,
        atom_description)
    
    # Show the image if requested
    if show_result:
        img.show()

    # Save the final image
    if output_path:
        img.save(output_path)
        print(f"Image saved to {output_path}")

