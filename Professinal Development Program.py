#========================================================#
from GPSPhoto import gpsphoto
import folium
from folium import plugins
import webbrowser
from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import exifread
from tkinter import scrolledtext
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file, exif_log, __version__
import PIL.Image
#===========================================================#



win = tk.Tk()
win.title("EXIF GPS")
win.configure(background='black')

win.minsize(width=660, height=590)
win.maxsize(width=660, height=590)

win.resizable(0,0)
menubar = Menu(win)

tooltip = '<b>Click for more info</b>'

def FileOpener():
    filename = askopenfilename(filetypes=[("JPEG image","*.jpg *.jpeg"),("All files","*.*")])
    return filename
def displayData(filename):
    f = open(filename,'rb')

    tags = exifread.process_file(f, stop_tag='TAG')
    for tag in tags.keys():
        if tag in ('Image Make','Image Model','Image DateTime','GPS GPSTimeStamp','EXIF DateTimeOriginal'):
            print (tag, tags[tag])
            tug = tag, tags[tag]
            scr.insert(tk.INSERT,tug)

def ExifGPS(filename):
    map_exif = folium.Map(location=[51.509865,-0.118092],zoom_start=11, tiles='Stamen Terrain')
    data = gpsphoto.getGPSData(filename)
    latt = data['Latitude']
    longg = data['Longitude']
    scrolly ="GPS: " + str(latt) + str(longg)
    scr.insert(tk.INSERT,scrolly)
    print(scr.get("1.0",END))

    with open(filename,'rb') as d:
        tags = exifread.process_file(d,stop_tag ='EXIF DateTimeOriginal')
        dateTaken = tags['Image DateTime']
        init = '<b>'+str(dateTaken)+'</b>'
    
    
    folium.Marker([latt,longg], popup=init,tooltip=tooltip,icon=folium.Icon(color='red', icon='info-sign')).add_to(map_exif)
    map_exif.save('ExifGPS.html')

def ShowPlot():
    webbrowser.open_new_tab('ExifGPS.html')
    

def Help():
    top = Toplevel()
    top.title=("Help")
    top.geometry("1065x861")
    render = PhotoImage(file='Help.png')
    top.img = Label(top,image=render)
    top.img.image = render
    top.img.place(x=0,y=0)



def export():
    sct = scr.get("1.0",END)
    fl = open("Output.txt", "w")
    fl.write(sct)
#FileMenu 
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label="Quit",command=win.quit)
menubar.add_cascade(label="File", menu=filemenu)
#OpenMenu
openmenu = Menu(menubar,tearoff=0)
openmenu.add_command(label="Select Image GPS",command=lambda: ExifGPS(FileOpener()))
openmenu.add_command(label="Select Image Display Data",command=lambda:displayData(FileOpener()))
menubar.add_cascade(label="Open",menu=openmenu)
#ShowMenu
showmenu = Menu(menubar,tearoff=0)
showmenu.add_command(label="Show GPS Location",command=ShowPlot)
menubar.add_cascade(label="Show",menu=showmenu)
#SaveMenu
savemenu = Menu(menubar,tearoff=0)
savemenu.add_command(label="Save Data",command=export)
menubar.add_cascade(label="Save",menu=savemenu)
#HelpMenu
helpmenu = Menu(menubar,tearoff=0)
helpmenu.add_command(label="How to use",command=Help)
menubar.add_cascade(label="Help",menu=helpmenu)

# Adding a button to clear
action = ttk.Button(win, text="Clear",command=lambda: scr.delete(1.0,tk.END)).place(x=460,y=160,height=425,width=198)
# Add a label for user
bLabel = ttk.Label(win, text="                               Use menubar and select the image file                                                    ")
bLabel.grid(column=0,row=0,sticky='W')
#ScrollBox
scr = scrolledtext.ScrolledText(win, width=54,height=35, wrap=tk.WORD)
scr.place(x=1,y=20)
#Logo Placement
render = PhotoImage(file='rsz_1exif1.png')
img = Label(win,image=render)
img.image = render
img.place(x=460,y=0)

win.config(menu=menubar)
win.mainloop()
