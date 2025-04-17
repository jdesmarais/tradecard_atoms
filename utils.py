from PIL import ImageDraw, ImageFont

def wrap_text_to_box(draw: ImageDraw, text: str, font: ImageFont, box_width: tuple):
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

def write_text_in_box(draw: ImageDraw, text: str, box_size: tuple, box_top_left: tuple, font: ImageFont, color: tuple):
    box_width, box_height = box_size

    lines = wrap_text_to_box(draw, text, font, box_width)

    # Draw lines within the box (check height if needed)
    bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_height = (bbox[3] - bbox[1]) + 5  # height + line spacing
    y_offset = box_top_left[1]

    for line in lines:
        if y_offset + line_height > box_top_left[1] + box_height:
            break  # Stop if we exceed the box height
        draw.text((box_top_left[0], y_offset), line, font=font, fill=color)
        y_offset += line_height

def draw_grid(draw: ImageDraw, img_size: tuple):
    i_max = int(img_size[0] / 100.) + 1
    j_max = int(img_size[1] / 100.) + 1

    # draw vertical lines
    for i in range(0,i_max):
        x_line = i*100
        draw.line([(x_line,0), (x_line,img_size[1])], fill=(255,0,0), width=2)

        for j in range(1,10):
            x_line = i*100 + j*10
            draw.line([(x_line,0), (x_line,img_size[1])], fill=(0,255,0), width=2)

        j=5
        x_line = i*100 + j*10
        draw.line([(x_line,0), (x_line,img_size[1])], fill=(255,255,255), width=2)
        
    # draw horizontal lines
    for i in range(0,j_max):
        y_line = i*100
        draw.line([(0,y_line), (img_size[0],y_line)], fill=(255,0,0), width=2)

        for j in range(1,10):
            y_line = i*100 + j*10
            draw.line([(0,y_line), (img_size[0], y_line)], fill=(0,255,0), width=2)
    
        j=5
        y_line = i*100 + j*10
        draw.line([(0,y_line), (img_size[0], y_line)], fill=(255,255,255), width=2)

