from grid import detect_grid ,binarize
import cv2
from pathlib import Path

import pytesseract

days = ["Sat","Sun","Mon","Tue","Wed","Thu"]
times = ["8:00-9:30","9:40-11:10","11:20-12:50","13:00-14:30","14:40-16:10","16:20-17:50"]
input_image = cv2.imread(Path("input/image1.png"))

xs, ys = detect_grid(input_image)
cells = [[col for col in range(len(xs)-1)] for row in range(len(ys)-1)]

extracted_str = [[col for col in range(len(xs)-1)] for row in range(len(ys)-1)]
output_dir = Path("output")
output_dir.mkdir(parents=True,exist_ok=True)

def extract_cells(xs,ys):
    """
        fill cells matrix 
        each cell with its x,y coordinates
    """
    for j in range(len(ys)-1):

        for i in range(len(xs)-1):

            x1,x2,y1,y2 = xs[i],xs[i+1],ys[j],ys[j+1]
            crop = binarize(input_image[y1:y2,x1:x2])


            cells[j][i] = crop
            extracted_str[j][i] = pytesseract.image_to_string(crop)
            
    (output_dir / "extracted_cells.txt").write_text(str(extracted_str),encoding="utf-8")
extract_cells(xs,ys)