import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
from CreateTable import create_table
class MakeTable:
    def __init__(self, scale=1, 
                 time="result",
                 table = {
                    "database_name" : "",
                    'table_name' : "ㅁ 모든 작업",
                    'header' : {"Aa 이름":"s"},
                    'data' : [
                            [""],
                        ],
                    'analyzes' : ["개수"]
                 }) -> None:
        
        self.margin = 30 * scale
        self.padding = 10 * scale
        self.line = self.margin 
        self.image = self.create_bin_img(table['header'].keys(), table['data'], ImageFont.truetype("fonts/BMJUA.ttf", 14 * scale), self.padding, self.margin)
        self.max_x = self.image.shape[1] 
        self.max_y = self.image.shape[0]

        table_name = "  " + table['table_name'] + "  "
        self.create_back(table['database_name'], table_name, scale)

        self.image, max_x, max_y= create_table(self.lineUp(30 * scale), self.image, table['header'].keys(), table['data'], table['analyzes'], self.max_x, self.max_y, padding=self.padding, margin=self.margin, font=ImageFont.truetype("fonts/BMJUA.ttf", 14 * scale), scale=scale)
        self.image = self.image[:max_y + self.margin, :max_x + self.margin * 2]
        cv2.imwrite(f"{time}.png", self.image)
        print("makeTable")

    def create_bin_img(self, header, data, font, padding, margin):
        
        line = margin + 50 + 50

        max_widths = [0]*len(header)
        max_height = 0
        
        for row in [header] + data:
            for i, cell in enumerate(row):
                cell_width, cell_height = font.getsize(cell)
                max_widths[i] = max(max_widths[i], cell_width) + int(padding/3)
                max_height = max(max_height, cell_height)

        # Calculate table size
        width = sum(max_widths) + padding * (len(header) + 1) + margin * 4 # Modified
        height = line + (max_height + padding * 2) * (len(data) + 1) + padding * 3 + 10 + margin * 4
        img = np.ones((height, width, 3), dtype=np.uint8) * 255

        return img
    

    def create_back(self, title, visual, scale=1) :
        self.putText(title, self.margin , self.lineUp(0), 30, scale= scale)
        self.putText(visual, self.margin , self.lineUp(50*scale), 17, True, scale)
    
    def putText(self, text, x, y, size=20, line=False, scale=1):
        font = ImageFont.truetype('fonts/BMJUA.ttf', size * scale)
        img_pil = Image.fromarray(self.image)
        draw = ImageDraw.Draw(img_pil)
        draw.text((x, y), text, (0, 0, 0), font=font)
        self.image = np.array(img_pil)
        if line:
            text_bottom_x_len, text_bottom_y_len = font.getsize(text)
            line_y = self.line + 30 * scale - scale
            self.image = cv2.line(self.image, (x, line_y), (x + text_bottom_x_len, line_y), (0, 0, 0), thickness=2*scale)

    def lineUp(self, up = 50):
        self.line += up
        return self.line
    