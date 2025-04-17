import argparse
from PIL import Image, ImageDraw, ImageFont

def wrap_text_to_box(draw, text, font, box_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        if width <= box_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def generate_image():
#     background_path,
#     overlay_path,
#     output_path,
#     text,
#     font_path,
#     font_size,
#     text_position,
#     text_color,
#     circle_color_variable,
#     circle_position,
#     circle_radius,
#     overlay_position,
#     overlay_size,
#     show_result
# ):
    show_grid = False
    show_result = True

    background_path = "/Users/julien/Documents/Projects/tradecards_atom/assets/background.png"

    atom_path = "/Users/julien/Documents/Projects/tradecards_atom/assets/img/hydrogene.png"

    title_font_path = "/Library/Fonts/AdobeArabic-Regular.otf"
    title_font_size = 16*4
    title_text_position = (137.6,41.4-12)
    title_text = "Hydrogène (H)"
    title_text_color = (0,0,0)

    subtitle_font_path = "/Library/Fonts/AdobeArabic-Italic.otf"
    subtitle_font_size = 10*4
    subtitle_text_position = (137.6,46.8+50)
    subtitle_text = "Non-métal"
    subtitle_text_color = (0,0,0)

    picto_path = "/Users/julien/Documents/Projects/tradecards_atom/assets/picto.png"
    picto_position = (int(117.6)-100, int(15))
    picto_color = (155,0,187) # purple
    # picto_color = (255,18,85) # pink
    # picto_color = (15,178,0)  # green

    atomic_font_path = "/Library/Fonts/AdobeArabic-Regular.otf"
    atomic_font_size = 10*4
    atomic_text_color = (255,255,255)

    atomic_number = "1"
    atomic_mass = "1.01 g/mol"
    atomic_melting_temperature = "-259°C"
    atomic_vaporisation_temperature = "-252°C"
    atomic_discovery = "1766"

    atomic_number_position = (330, 668)
    atomic_mass_position = (315, 720)
    atomic_melting_temperature_position = (380, 772)
    atomic_vaporisation_temperature_position = (455, 825)
    atomic_discovery_position = (465, 880)

    description_font_path = "/Library/Fonts/AdobeArabic-Regular.otf"
    description_font_size = 8*4
    description_color = (255,255,255)
    description = "L'hydrogène est le principal constituant du Soleil et de la plupart des étoiles (dont l'énergie provient de la fusion thermonucléaire de cet hydrogène), et de la matière interstellaire ou intergalactique. Sur Terre, il est surtout présent à l'état d'eau liquide, solide (glace) ou gazeuse (vapeur d'eau), mais on le trouve aussi dans les émanations de certains volcans sous la forme de H2 et de CH4 (méthane)."
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
    # draw = ImageDraw.Draw(background_img)
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
        for i in range(0,10):
            x_line = i*100
            draw.line([(x_line,0), (x_line,1000)], fill=(255,0,0), width=2)

            for j in range(1,10):
                x_line = i*100 + j*10
                draw.line([(x_line,0), (x_line,1000)], fill=(0,255,0), width=2)

            j=5
            x_line = i*100 + j*10
            draw.line([(x_line,0), (x_line,1000)], fill=(255,255,255), width=2)
            

        for i in range(0,10):
            y_line = i*100
            draw.line([(0,y_line), (1000,y_line)], fill=(255,0,0), width=2)

            for j in range(1,10):
                y_line = i*100 + j*10
                draw.line([(0,y_line), (1000, y_line)], fill=(0,255,0), width=2)
        
            j=5
            y_line = i*100 + j*10
            draw.line([(0,y_line), (1000, y_line)], fill=(255,255,255), width=2)



    # Draw atomic numbers
    atomic_font = ImageFont.truetype(atomic_font_path, atomic_font_size)
    draw.text(atomic_number_position, atomic_number, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_mass_position, atomic_mass, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_melting_temperature_position, atomic_melting_temperature, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_vaporisation_temperature_position, atomic_vaporisation_temperature, font=atomic_font, fill=atomic_text_color)
    draw.text(atomic_discovery_position, atomic_discovery, font=atomic_font, fill=atomic_text_color)


    # Draw atomic description
    description_font = ImageFont.truetype(description_font_path, description_font_size)

    # Your box configuration
    box_top_left = description_position
    box_width, box_height = description_box_size

    # Wrap the text into lines
    lines = wrap_text_to_box(draw, description, description_font, box_width)

    # Draw lines within the box (check height if needed)
    bbox = draw.textbbox((0, 0), "Ag", font=description_font)
    line_height = (bbox[3] - bbox[1]) + 5  # height + line spacing
    y_offset = box_top_left[1]

    for line in lines:
        if y_offset + line_height > box_top_left[1] + box_height:
            break  # Stop if we exceed the box height
        draw.text((box_top_left[0], y_offset), line, font=description_font, fill=description_color)
        y_offset += line_height

    # Show the image if requested
    if show_result:
        img.show()

    # Save the final image
    # background.save(output_path)
    # print(f"Image saved to {output_path}")

if __name__ == "__main__":
    generate_image()
