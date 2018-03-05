import PIL.Image
from tkColorChooser import askcolor
import PIL.ImageTk
import self as self
from PIL import *
from Tkinter import *
import tkFileDialog
from tkinter import messagebox
from tkColorChooser import askcolor
from subprocess import Popen

from PIL import ImageTk

global labelValues
choosenColor = (0, 0, 0)
drawingImage = None
labelValues = None


def main():
    global root
    root = Tk()

    root.title("Paint Book")
    root.geometry("800x800")

    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Add Image", command=openFile)
    file_menu.add_command(label="Save Image", command=saveImage)
    file_menu.add_command(label="Clear", command=clear)
    file_menu.add_command(label="Quit", command=root.destroy)
    menu_bar.add_cascade(label="Options", menu=file_menu)
    root.config(menu=menu_bar)

    pickColor = Button(root, text='Color Selector', command=getColor)
    pickColor.grid(row=0, column=0)

    


    root.mainloop()



def getColor():
    color = askcolor()
    color = str(color)
    start = color.index("((")
    stop = color.index("),")
    color = color[(start):stop]
    color = color[2:len(color)]
    r, g, b = color.split(",")
    global choosenColor
    choosenColor = int(r), int(g), int(b)
    print ("choosenColor is :", choosenColor)

def openFile():
    file_path_string = tkFileDialog.askopenfilename()
    # drawingImage=Image.open(file_path_string)
    fp = open(file_path_string, "rb")
    global drawingImage
    drawingImage = PIL.Image.open(fp)

    global pix
    pix = drawingImage.load()
    xSize, ySize = drawingImage.size
    for i in range(xSize):
        for j in range(ySize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])
    addToScreen(drawingImage)


def addToScreen(Img):
    # option ekle
    dialog_title = 'Choose Your Labeling Tecnique '
    dialog_text = 'Please select yes if you want to label with 4 component teqnique'
    answer = messagebox.askquestion(dialog_title, dialog_text)
    if answer == 'yes':
        labeling(Img)
        render = ImageTk.PhotoImage(Img)
        img = Label(root, image=render)
        img.image = render
        img.place(x=150, y=50)
        img.bind("<Button-1>", printcoords)
    else:  # 'no'
        _component_labeling(Img)
        render = ImageTk.PhotoImage(Img)
        img = Label(root, image=render)
        img.image = render
        img.place(x=150, y=50)
        img.bind("<Button-1>", printcoords)


def printcoords(event):
    # outputting x and y coords to console
    print (event.x, event.y)
    paintReagion(event.x, event.y)


def paintReagion(x, y):
    global labelValues
    global drawingImage

    rowSize, columnSize = drawingImage.size

    for i in range(1, rowSize - 1):
        for j in range(1, columnSize - 1):
            if labelValues[i][j] == labelValues[x][y]:
                pix[i, j] = choosenColor
                global drawingImage
                global choosenColor
                drawingImage.putpixel((i, j), choosenColor)

    render = ImageTk.PhotoImage(drawingImage)
    img = Label(root, image=render)
    img.image = render
    img.place(x=150, y=50)
    img.bind("<Button-1>", printcoords)


def converToBinaryValue(rgbValues):
    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average == 255:
        return 1
    return 0


def labeling(Img):
    rowSize, columnSize = Img.size

    for i in range(rowSize):
        for j in range(columnSize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])

    pixelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]
    for i in range(rowSize):
        for j in range(columnSize):
            pixelValues[i][j] = converToBinaryValue(pix[i, j])
    for i in range(rowSize):
        for j in range(columnSize):
            if i == 0 or j == 0 or i == rowSize - 1 or j == columnSize - 1:
                pixelValues[i][j] = 0

    print "\n\n\n\nbefore labeling pixelValues matrix look like"
    for j in range(columnSize):
        for i in range(rowSize):
            print pixelValues[i][j],
        print ""

    global labelValues
    labelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]
    for i in range(rowSize):
        for j in range(columnSize):
            labelValues[i][j] = 0

    labelCounter = 2
    for i in range(1, rowSize - 1):
        for j in range(1, columnSize - 1):
            if pixelValues[i][j] == 1:  # current is White
                if pixelValues[i - 1][j] == 1 and pixelValues[i][j - 1] == 1:
                    if labelValues[i - 1][j] == labelValues[i][j - 1]:
                        labelValues[i][j] = labelValues[i][j - 1]
                    else:
                        labelValues[i][j] = labelValues[i - 1][j]
                        for t in range(0, i + 1):
                            for k in range(0, j + 1):
                                if labelValues[t][k] == labelValues[i][j - 1]:
                                    labelValues[t][k] = labelValues[i - 1][j]
                elif pixelValues[i - 1][j] == 1 or pixelValues[i][j - 1] == 1:
                    if pixelValues[i - 1][j] == 1:
                        labelValues[i][j] = labelValues[i - 1][j]
                    else:
                        labelValues[i][j] = labelValues[i][j - 1]
                else:
                    labelValues[i][j] = labelCounter
                    labelCounter += 1
            else:
                labelValues[i][j] = 1
    print"************"
    print"After labeling what labelValues matrix looks like"
    for j in range(columnSize):
        for i in range(rowSize):
            print labelValues[i][j],
        print ""


def vanishNoisesFromPixel(rgbValues):
    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average > 200:
        return 255, 255, 255
    return 0, 0, 0


def _component_labeling(Img):
    rowSize, columnSize = Img.size

    for i in range(rowSize):
        for j in range(columnSize):
            pix[i, j] = vanishNoisesFromPixel(pix[i, j])

    pixelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]
    for i in range(rowSize):
        for j in range(columnSize):
            pixelValues[i][j] = converToBinaryValue(pix[i, j])
    for i in range(rowSize):
        for j in range(columnSize):
            if i == 0 or j == 0 or i == rowSize - 1 or j == columnSize - 1:
                pixelValues[i][j] = 0

    print "\n\n\n\nbefore labeling pixelValues matrix look like"
    for j in range(columnSize):
        for i in range(rowSize):
            print pixelValues[i][j],
        print ""

    global labelValues
    labelValues = [[0 for x in range(columnSize)] for y in range(rowSize)]
    for i in range(rowSize):
        for j in range(columnSize):
            labelValues[i][j] = 0

    labelCounter = 2
    for i in range(rowSize - 2):
        for j in range(columnSize - 2):
            upperleft = pixelValues[i - 1][j - 1]
            up = pixelValues[i - 1][j]
            upperright = pixelValues[i - 1][j + 1]
            left = pixelValues[i][j - 1]

            Lupperleft = labelValues[i - 1][j - 1]
            Lup = labelValues[i - 1][j]
            Lupperright = labelValues[i - 1][j + 1]
            Lleft = labelValues[i][j - 1]
            current = labelValues[i][j]

            # *************************LABELING*******************************************
            if pixelValues[i][j] == 1:
                if upperleft == 1 and left == 1 and up == 1 and upperright == 1:  # 1
                    lst = []
                    lst.append(Lupperleft)
                    lst.append(Lupperright)
                    lst.append(Lup)
                    lst.append(Lleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current=minimum

                    del lst[:]

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperright:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lup:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 0 and left == 1 and up == 1 and upperright == 1:  # 2
                    lst = []

                    lst.append(Lupperright)
                    lst.append(Lup)
                    lst.append(Lleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperright:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lup:
                                labelValues[a][b] = minimum

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 0 and up == 1 and upperright == 1:  # 3
                    lst = []
                    lst.append(Lupperright)
                    lst.append(Lup)
                    lst.append(Lupperleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]


                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperright:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lup:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 1 and up == 0 and upperright == 1:  # 4
                    lst = []

                    lst.append(Lupperleft)

                    lst.append(Lupperright)

                    lst.append(Lleft)

                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperright:
                                labelValues[a][b] = minimum

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 1 and up == 1 and upperright == 0:  # 5
                    lst = []
                    lst.append(Lupperleft)
                    lst.append(Lup)
                    lst.append(Lleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]


                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lup:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 0 and up == 1 and upperright == 0:  # 7
                    lst = []
                    lst.append(Lupperleft)

                    lst.append(Lup)

                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]



                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lup:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 0 and up == 0 and upperright == 1:  # 8
                    lst = []
                    lst.append(Lupperleft)
                    lst.append(Lupperright)

                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperright:
                                labelValues[a][b] = minimum

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum

                if upperleft == 0 and left == 1 and up == 1 and upperright == 0:  # 9
                    lst = []

                    lst.append(Lup)
                    lst.append(Lleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]


                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lup:
                                labelValues[a][b] = minimum

                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 1 and up == 0 and upperright == 0:  # 10
                    lst = []
                    lst.append(Lupperleft)

                    lst.append(Lleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]


                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 1 and up == 0 and upperright == 0:  # 12
                    lst = []
                    lst.append(Lupperleft)

                    lst.append(Lleft)
                    lst.sort(reverse=True)
                    minimum = lst.pop()
                    current = minimum
                    del lst[:]


                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lupperleft:
                                labelValues[a][b] = minimum
                    for a in range(rowSize):
                        for b in range(columnSize):
                            if labelValues[a][b] == Lleft:
                                labelValues[a][b] = minimum

                if upperleft == 1 and left == 0 and up == 0 and upperright == 0:  # 13
                    current = Lupperleft

                if upperleft == 0 and left == 1 and up == 0 and upperright == 0:  # 14
                    current = Lleft

                if upperleft == 0 and left == 0 and up == 1 and upperright == 0:  # 15
                    current = Lup

                if upperleft == 0 and left == 0 and up == 0 and upperright == 1:  # 16
                    current = Lupperright
                if upperleft == 0 and left == 0 and up == 0 and upperright == 0:
                    labelCounter += labelCounter
                    current = labelCounter
            else:
                current = 1

    print"************"
    print"After labeling what labelValues matrix looks like"
    for j in range(columnSize):
        for i in range(rowSize):
            print labelValues[i][j],
        print ""


def saveImage():
    file = tkFileDialog.asksaveasfile(mode='w', defaultextension=".png")
    if file:
        global drawingImage
        drawingImage.save(file)

def clear():


    rowSize, columnSize = drawingImage.size

    for i in range(rowSize):
        for j in range(columnSize):
            if labelValues[i][j]!= 1:
                pix[i, j] = (255,255,255)
                drawingImage.putpixel((i,j),(255,255,255))


    render = ImageTk.PhotoImage(drawingImage)
    img = Label(root, image=render)
    img.image = render
    img.place(x=150, y=50)
    img.bind("<Button-1>", printcoords)




if __name__ == '__main__':
    main()
