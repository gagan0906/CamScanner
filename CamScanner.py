import time
import cv2
from fpdf import FPDF
from glob2 import glob
from tkinter import *
from tkinter import filedialog
import os

root = Tk()
root.title('Camscanner')
images=[]
root.directory=os.getcwd()



def process():
    global images
    if optimize.get()==1:
        for img in images:
            org_image = cv2.imread(img, 1)
            gray_img = cv2.cvtColor(org_image, cv2.COLOR_BGR2GRAY)
            gaus_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 105, 25)
            cv2.imwrite('_temp' + img, gaus_img)
    images_temp=[]
    pdf = FPDF()
    for img in glob('_temp*'):
        images_temp.append(img)
    for image in images_temp:
        pdf.add_page()
        pdf.image(image, w =150)
    name='camscan'
    digit=int(time.time())%10000
    name=name+'_'+str(digit)

    pdf.output(name + ".pdf", "F")
    for i in images_temp:
        os.remove(i)
    Lastmessgage.set('Your PDF is Ready')
    done=Label(root, textvariable=Lastmessgage)
    done.grid(row=6,column=1)


def selectDir():
    global images
    root.directory = filedialog.askdirectory()
    os.chdir(root.directory)
    var.set(root.directory)
    images = glob('*.jpg') + glob('*.png')
    grey = Checkbutton(root, text="Optimize for better quality", variable=optimize)
    grey.grid(row=4, column=0)
    generate=Button(root,text='Generate', command=process)
    generate.grid(row=5,column=1)

root.geometry('400x300')
root.resizable(0, 0)
var = StringVar()
Lastmessgage=StringVar()
var.set('Empty')
optimize = IntVar()
optimize.set(0)
inst = Label(root, text="Select the directory where images are kept")
inst.grid()

direc = Label(root, textvariable=var)
direc.grid(row=2)

change_dir = Button(root, text="Select Folder", command=selectDir)
change_dir.grid(row=2, column=1)

root.mainloop()
