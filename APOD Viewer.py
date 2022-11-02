import tkinter as tk
import requests, webbrowser
from urllib import request, response
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from io import BytesIO
from tkinter import filedialog

# Define window
root = tk.Tk()
root.title("APOD Viewer")
root.iconbitmap("rocket.ico")

# Define colors and fonts
text_font = ("Times New Roman", 14)
nasa_blue = "#043c93"
nasa_light_blue = "#7aa5d3"
nasa_red = "#ff1923"
nasa_white = "#ffffff"
root.config(bg = nasa_blue)

# Define functions

def get_request():
    global response
    url  = "https://api.nasa.gov/planetary/apod"
    api_key = "yMnakIUFJhKBXEVO3Me64b3je4rGViBX8JRg2mLl"
    date = calendar.get_date()
    print(date)

    quarystring = {"api_key":api_key, "date":date}

    response = requests.request("GET", url, params = quarystring)
    response = response.json()

    set_info()
    set_picture()

def set_info():

    """{'copyright': 'Dario Giannobile', 'date': '2022-09-15', 'explanation': "For northern hemisphere dwellers,
    September's Full Moon was the Harvest Moon. Reflecting warm hues at sunset it rises over the historic town of
    Castiglione di Sicilia in this telephoto view from September 9. Famed in festival, story, and song Harvest
    Moon is just the traditional name of the full moon nearest the autumnal equinox. According to lore the
    name is a fitting one. Despite the diminishing daylight hours as the growing season drew to a close,
    farmers could harvest crops by the light of a full moon shining on from dusk to dawn.   Harvest Full
    Moon 2022: Notable Submissions to APOD", 
    'hdurl': 'https://apod.nasa.gov/apod/image/2209/HarvestMoonCastiglioneSicilyLD.jpg',
    'media_type': 'image', 'service_version': 'v1', 'title': 'Harvest Moon over Sicily',
    'url': 'https://apod.nasa.gov/apod/image/2209/HarvestMoonCastiglioneSicily1024.jpg'}"""

    picture_date.config(text = response["date"], font= text_font, bg=nasa_white)
    picture_explanation.config(text=response["explanation"], font= text_font, bg=nasa_white, wraplength= 800)

def set_picture():
    global img
    
    global thumb
    global full_img
    url = response["url"]
 
    if response["media_type"] == "image":
        


        img_response = requests.get(url, stream=True)
        img_data = img_response.content
        img = Image.open(BytesIO(img_data))
        
        full_img = ImageTk.PhotoImage(img)

        thumb_data = img_response.content
        thumb = Image.open(BytesIO(thumb_data))
        thumb.thumbnail((200,200))
        thumb = ImageTk.PhotoImage(thumb)

        #Set the thumbnail image
        picture_label.config(image=thumb)
    elif response["media_type"] == "video":
        picture_label.config(text = url, image = "")
        webbrowser.open(url)

def full_photo():
    top = tk.Toplevel()
    top.title("Full APOD Photo")
    top.iconbitmap("rocket.ico")

    img_label = tk.Label(top,image = full_img)
    img_label.pack()

def save_photo():
    global hdimg
    save_name = filedialog.asksaveasfilename(initialdir="./", title = "Save Image", filetypes=(("JPEG", "*.jpg"), ("All Files", "*.*")))
    hdurl = response["hdurl"]
    img_response = requests.get(hdurl, stream=True)
    img_data = img_response.content
    hdimg = Image.open(BytesIO(img_data))
  
    hdimg.save(save_name + ".jpg")



# Define layout
input_frame = tk.Frame(root,bg = nasa_blue)
output_frame = tk.Frame(root, bg = nasa_white)
input_frame.pack()
output_frame.pack(padx = 50, pady = (0,25))

# Layout for input frame
calendar =  DateEntry(input_frame, width=10, font = text_font, background = nasa_blue, foreground = nasa_white)
submit_button = tk.Button(input_frame, text = "Submit", font = text_font, bg=nasa_light_blue, command= get_request)
full_button = tk.Button(input_frame, text = "Full Photo", font = text_font, bg=nasa_light_blue, command= full_photo)
save_button = tk.Button(input_frame, text = "Save Photo", font = text_font, bg=nasa_light_blue, command= save_photo)
quit_button = tk.Button(input_frame, text = "Exit", font = text_font, bg=nasa_red, command=root.destroy)

calendar.grid(row=0,column=0,padx = 5, pady = 10)
submit_button.grid(row=0,column=1,padx=5,pady=10, ipadx=35)
full_button.grid(row=0,column=2,padx=5,pady=10, ipadx=25)
save_button.grid(row=0,column=3,padx=5,pady=10, ipadx=25)
quit_button.grid(row=0,column=4,padx=5,pady=10, ipadx=50)

#Layout for the output frame
picture_date = tk.Label(output_frame)
picture_explanation = tk.Label(output_frame)
picture_label = tk.Label(output_frame) 

picture_date.grid(row=1,column=1,padx = 10)
picture_explanation.grid(row=0,column=0, padx = 10, pady = 10,rowspan=2)
picture_label.grid(row=0,column=1,padx=10,pady=10)

get_request()

#Define root window main loop
root.mainloop()