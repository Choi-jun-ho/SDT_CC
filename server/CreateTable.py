from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_table(line, img, header, data, analyzes, max_x=1920, max_y=1080, padding=12, margin=0, font=ImageFont.truetype("fonts/BMJUA.ttf", 14), scale=1):

    # Calculate max width and height of the cells
    max_widths = [0]*len(header)
    max_height = 0
    
    for row in [header] + data:
        for i, cell in enumerate(row):
            cell_width, cell_height = font.getsize(cell)
            max_widths[i] = max(max_widths[i], cell_width) + int(padding/3)
            max_height = max(max_height, cell_height)

    # Calculate table size
    width = sum(max_widths) + padding * (len(header) + 1) + margin * 2 # Modified
    height = line + (max_height + padding * 2) * (len(data) + 1)
    line_width = 1 * scale

    # Empty image
    img = Image.fromarray(img)
    #img = Image.new('RGB', (width, height), (255, 255, 255))

    draw = ImageDraw.Draw(img)

    # Draw headers
    y_pos = line + padding
    for c, col_name in enumerate(header):
        x_pos = sum(max_widths[:c]) + padding * (c + 1) + margin # Modified
        draw.text((x_pos, y_pos), col_name, font=font, fill=(128, 128, 128))

    # Draw data
    for r, row_data in enumerate(data):
        y_pos = (max_height + padding * 2) * (r + 1) + padding + line
        for c, cell_data in enumerate(row_data):
            x_pos = sum(max_widths[:c]) + padding * (c + 1) + margin # Modified
            draw.text((x_pos, y_pos), cell_data, font=font, fill=(90, 90, 90))
    
    last_line_y = height + padding * 3
    font = ImageFont.truetype("fonts/BMJUA.ttf", 12*scale)
    
    for c, analyze_data in enumerate(analyzes):
        x_pos = sum(max_widths[:c + 1]) + padding * (c + 1) + margin # Modified
        draw.text((x_pos - font.getsize(analyze_data)[0], last_line_y + font.getsize(analyze_data)[1]), analyze_data, font=font, fill=(90, 90, 90))

    # Draw lines
    # 세로줄 | 
    for c, width in enumerate(max_widths[:-1]):
        x_pos = sum(max_widths[:c + 1]) + padding * (c + 1) + margin # Modified
        draw.line([(x_pos, line), (x_pos, height)], fill=(200, 200, 200), width=line_width)
    
    x_pos = sum(max_widths) + padding * (len(max_widths) + 1) + margin # Modified
    draw.line([(x_pos, line), (x_pos, height)], fill=(200, 200, 200), width=line_width)
    
    
    # 가로줄 __
    max_line_x = max_x - (padding * len(max_widths) + margin)
    for j in range(line, height + max_height + padding * 2, max_height + padding * 2):
        draw.line([(margin, j), (max_line_x + margin , j)], fill=(200, 200, 200), width=line_width)
    
    #last line __
    draw.line([(margin, last_line_y), (max_line_x  + margin , last_line_y)], fill=(200, 200, 200), width=line_width)

    return np.array(img), max_line_x, last_line_y + 12 * scale



if __name__ == "__main__":


    header = ["Aa 이름", "Long Header 2", "Headerasdsaddas 3"]
    data = [
        ["Sample dasadsadsasdta 1", "Sample data 2", "Sample data 3"],
        ["Example data 4", "Example data 5", "Example data 6"],
        ["Data 7", "Data 8", "Data 9"],
    ]

    # Create table
    #table = create_table(header, data)

    # # Save and show the table
    # table.save("example_table.png")
    # table.show()