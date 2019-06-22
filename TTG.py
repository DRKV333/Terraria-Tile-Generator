import random
import PIL.Image
import os
from tkinter import *
from tkinter.colorchooser import *
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()

shadesNum = StringVar()
texn = StringVar()
textype = StringVar(value="TTG.png")
global colors
root.resizable(FALSE,FALSE)
root.title("Terraria Tile Generator")
    
if not os.path.exists("Blocks"):
    os.makedirs("Blocks")
    print("Created dir 'Blocks'.")

def MakeTile(shadesNum, colors):
    print("\nStarted!")
    tamplateImg = PIL.Image.open(resource_path(textype.get())).convert("RGBA")
    template = tamplateImg.load()

    for x in range(shadesNum):
        darkShade = tuple(x - 10 if x >= 10 else x for x in colors[-1])
        lightShade = tuple(x + 10 if x <= 245 else x for x in colors[0])
        colors = [lightShade] + colors + [darkShade]

    for row in range(0, tamplateImg.width, 2):
        for pixel in range(0, tamplateImg.height, 2):
            if template[row, pixel][1] == 255:
                randomColor = colors[random.randint(0, len(colors) - 1)]
                template[row, pixel] = randomColor
                template[row + 1, pixel] = randomColor
                template[row, pixel + 1] = randomColor
                template[row + 1, pixel + 1] = randomColor
    print("Created image!")

    tamplateImg.save('Blocks\\' + texn.get() + '.png')
    print("Saved image!")
    print("Done!")

def getColor():
    color = askcolor()
    colorButton.configure(bg=color[1])
    hexcolor = color[1][1:]
    global colors
    colors = [(int(hexcolor[0] + hexcolor[1], 16), int(hexcolor[2] + hexcolor[3], 16), int(hexcolor[4] + hexcolor[5], 16), 255)]

Label(root, text="Terraria Tile Generator", font='Helvetica 18 bold').grid(row=0, column=0, padx=10, pady=10, columnspan=2)
Label(root, text="Number of lighter and darker shades:").grid(column=0, row=1, padx=10, pady=10)
Entry(root, textvariable=shadesNum).grid(column=0, row = 2)
Label(root, text="Enter Texture name:").grid(column=0, row=3, padx=10, pady=10)
Label(root, text="Select Texture Type:").grid(column=1, row=3, padx=10, pady=10)
Radiobutton(root, text="Jaggy-like Type", variable=textype, value="TTG.png").grid(column=1, row=4, padx=10)
Radiobutton(root, text="Smooth Type", variable=textype, value="TTGS.png").grid(column=1, row=5, padx=10)
Entry(root, textvariable=texn).grid(column=0, row=4)
Label(root, text="Pick a base color:").grid(column=1, row=1, padx=10, pady=10)
colorButton = Button(root, command=getColor, text="                          ")
colorButton.grid(column=1,row=2, padx=10, pady=10)
Button(root, text="Generate!", command=lambda: MakeTile(int(shadesNum.get()), colors)).grid(row=5, column=0, padx=10, pady=10)

root.mainloop()
