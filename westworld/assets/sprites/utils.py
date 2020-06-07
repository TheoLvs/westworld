
from PIL import Image
import numpy as np
import pandas as pd
import pyperclip


def make_lighter_color(color,lighter = 0.5):
    lighter_fn = lambda x,t : min([255,int((1+t)*x)]) 
    return tuple([lighter_fn(x,lighter) for x in color])

def get_unique_colors_sprite(filepath):
    img = Image.open(filepath)
    array = np.array(img).reshape(-1,3).tolist()
    array = ["(" + ",".join(map(str,x)) + ")" for x in array]
    return pd.Series(array).value_counts()


def make_sprite_generator_fn(filepath,replace = None,return_array = False):
    
    img = Image.open(filepath)
    shape = img.size
    array = np.array(img).reshape(-1,3).tolist()
    array = ["(" + ",".join(map(str,x)) + ")" for x in array]
    
    if replace is not None:
        array = [replace.get(x,x) for x in array]
        
    array = np.array(array).reshape(shape)
    
    if return_array:
        return array
    
        
    array = f"{array.tolist()}".replace(",",",\n\t\t").replace('"','').replace("'","")
    
    fn_str = f"import numpy as np\n\ndef make_sprite(args):\n\treturn np.array(\n\t\t{array}\n)"
    fn_str = fn_str.replace("\t","    ")
    pyperclip.copy(fn_str)
    print("Copied to clipboard")