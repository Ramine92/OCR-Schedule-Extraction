import cv2 
from pathlib import Path
import numpy as np

IMG_PATH = "input/image1.png"
OUTPUT_DIR = Path("preprocessed_image")
img = cv2.imread(IMG_PATH)

def binarize(img,save=False):
    if img is None:
        raise ValueError(f"Could not read image: {IMG_PATH}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / "bin_img.png"
        cv2.imwrite(str(output_path),bin_img)
    return bin_img

def keep_long_lines(bw,horizontal=True, scale=20):
    h,w = bw.shape

    size = w // scale if horizontal else h // scale 
    shape = (size,1) if horizontal else (1,size)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,shape)
    opened = cv2.erode(bw,kernel)
    return cv2.dilate(opened,kernel)

def merge_close(indices, gap=4):
    if len(indices) == 0:
        return []
    
    groups,current = [],[indices[0]]

    for i in indices[1:]:
        if i - current[-1] <= gap:
            current.append(i)
        else:
            groups.append(int(np.mean(current)))
            current = [i]
    groups.append(int(np.mean(current)))
    return groups 

def detect_grid(img,min_fill=0.3):
    bw = binarize(img,save=True)
    h,w = bw.shape

    horiz = keep_long_lines(bw,horizontal=True)
    vert = keep_long_lines(bw,horizontal=False)

    

    h_fill = horiz.sum(axis=1) / (255 * w)
    v_fill = vert.sum(axis=0) / (255 * h)

    print("v_fill max:", v_fill.max(), "mean:", v_fill.mean(), "min_fill:", min_fill)

    xs = merge_close(np.where(v_fill > min_fill)[0])
    ys = merge_close(np.where(h_fill > min_fill)[0])

    print(len(xs),len(ys))
    return xs,ys

def draw_grid(img,xs,ys,out_path="debug_grid.png"):
    dbg = img.copy()

    for x in xs:
        cv2.line(dbg,(x,0),(x,dbg.shape[0]),(0,0,255),1)

    for y in ys:
        cv2.line(dbg,(0,y), (dbg.shape[1],y),(255,0,0),1)

    cv2.imwrite(out_path,dbg)

def show_img(img):
    cv2.imshow("Binarized image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


xs,ys = detect_grid(img)

draw_grid(img,xs,ys)