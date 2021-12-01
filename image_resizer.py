# how to build python -m nuitka --mingw64 --windows-disable-console --windows-icon-from-ico=balkae.ico .\image_resizer.py

# Required Libraries
import os
import subprocess
from PIL import Image, ImageTk
import errno
import time
import tkinter as tk
from tkinter import filedialog, PhotoImage
import random
from ctypes import windll,c_int,byref

# Query DPI Awareness (Windows 10 and 8)
awareness = c_int()
errorCode = windll.shcore.GetProcessDpiAwareness(0, byref(awareness))

# Set DPI Awareness  (Windows 10 and 8)
errorCode = windll.shcore.SetProcessDpiAwareness(2)
# the argument is the awareness level, which can be 0, 1 or 2:
# for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)

cwd = os.getcwd()

# Iterate through every image
# and resize all the images.
    
class crop_popupWindow(object):
    def __init__(self,master,preview_crop_width_entry,preview_crop_height_entry,preview_horizontal_offset,preview_vertical_offset):
        super().__init__()

        top=self.top=tk.Toplevel(master)

        self.preview_crop_width_entry=preview_crop_width_entry
        self.preview_crop_height_entry=preview_crop_height_entry
        self.preview_horizontal_offset=preview_horizontal_offset
        self.preview_vertical_offset=preview_vertical_offset
        
        self.title_label=tk.Label(top,text="Choose Preferences")
        self.title_label.pack(pady=10,padx=10)
        self.crop_header=tk.Label(top,text="enter the size of the cropped image")
        self.crop_header.pack(pady=10,padx=10)
        self.crop_width_entry=tk.Entry(top)
        self.crop_width_entry.insert(0,'1024')
        self.crop_width_entry.pack(pady=10,padx=10)
        self.crop_height_entry=tk.Entry(top)
        self.crop_height_entry.insert(0,'1024')
        self.crop_height_entry.pack(pady=10,padx=10)
        self.horizontal_offset=tk.Label(top,text="Enter horizontal offset")
        self.horizontal_offset.pack(pady=10,padx=10)
        self.horizontal_offset=tk.Entry(top)
        self.horizontal_offset.insert(0,'0')
        self.horizontal_offset.pack(pady=10,padx=10)
        self.vertical_offset=tk.Label(top,text="Enter vertical offset")
        self.vertical_offset.pack(pady=10,padx=10)
        self.vertical_offset=tk.Entry(top)
        self.vertical_offset.insert(0,'0')
        self.vertical_offset.pack(pady=10,padx=10)
        self.submit_button=tk.Button(top,text='use preview settings',command=self.use_preview_settings)
        self.submit_button.pack()
        self.submit_button=tk.Button(top,text='Ok',command=self.cleanup)
        self.submit_button.pack()
        top.iconbitmap(cwd + os.sep +"assets\\balkae.ico")
        top.resizable(False, False)
    def cleanup(self):
        self.value=','.join([self.crop_width_entry.get(),self.crop_height_entry.get(),self.horizontal_offset.get(),self.vertical_offset.get()])
        self.top.destroy()
    def use_preview_settings(self):
        self.value=','.join([self.preview_crop_width_entry.get(),self.preview_crop_height_entry.get(),self.preview_horizontal_offset.get(),self.preview_vertical_offset.get()])
        self.top.destroy()
    def close_window(self,e):
        self.top.destroy()

class compress_popupWindow(object):
    def __init__(self,master):
        top=self.top=tk.Toplevel(master)
        self.title_label=tk.Label(top,text="Choose Preferences")
        self.title_label.pack(pady=10,padx=10)
        self.compression_header=tk.Label(top,text="enter the quality of compression (0-100)\nnote compression quality decreases exponentially from 100 to 0")
        self.compression_header.pack(pady=10,padx=10)
        self.compression_entry=tk.Entry(top)
        self.compression_entry.insert(0,'95')
        self.compression_entry.pack(pady=10,padx=10)
        self.submit_button=tk.Button(top,text='Ok',command=self.cleanup)
        self.submit_button.pack()
        top.iconbitmap(cwd + os.sep +"assets\\balkae.ico")
        top.resizable(False, False)
    def cleanup(self):
        self.value=','.join([self.compression_entry.get()])
        self.top.destroy()

class resize_popupWindow(object):
    def __init__(self,master):
        super().__init__()
        top=self.top=tk.Toplevel(master)
        self.title_label=tk.Label(top,text="Choose Preferences")
        self.title_label.pack(pady=10,padx=10)
        self.resize_header=tk.Label(top,text="enter the base width for resizing\n height will be calculated automatically to\nmaintain the image aspect ratio")
        self.resize_header.pack(pady=10,padx=10)
        self.resize_entry=tk.Entry(top)
        self.resize_entry.insert(0,'80')
        self.resize_entry.pack(pady=10,padx=10)
        self.submit_button=tk.Button(top,text='Ok',command=self.cleanup)
        self.submit_button.pack()
        top.iconbitmap(cwd + os.sep +"assets\\balkae.ico")
        top.resizable(False, False)
    def cleanup(self):
        self.value=self.resize_entry.get()
        self.top.destroy()

class App(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self) # create window

        #init variables
        self.check_png_jpg = tk.BooleanVar()
        self.CONVERT_PNG_TO_JPG = tk.BooleanVar()
        self.CONVERT_PNG_TO_JPG = False
        self.TOTAL_ORIGINAL = 1
        self.TOTAL_COMPRESSED = 0
        self.TOTAL_GAIN = 0
        self.TOTAL_FILES = 0
        self.QUALITY = 90

        self.input_folder = ""
        self.output_folder = ""
        self.input_folder_path = tk.StringVar()
        self.input_folder_path.set("No folder selected")
        self.output_folder_path = tk.StringVar()
        self.output_folder_path.set("No folder selected")
        self.log_label = tk.StringVar()
        self.log_label.set("Logs")

        bg = PhotoImage(file=cwd + os.sep +"assets\\background.png")
        input_folder_img = PhotoImage(file=cwd + os.sep +"assets\\img1.png")
        output_folder_img = PhotoImage(file=cwd + os.sep +"assets\\img3.png")
        exit_button_img = PhotoImage(file=cwd + os.sep +"assets\\img0.png")
        crop_button_img = PhotoImage(file=cwd + os.sep +"assets\\img4.png")
        compress_button_img = PhotoImage(file=cwd + os.sep +"assets\\img6.png")
        preview_button_img = PhotoImage(file=cwd + os.sep +"assets\\img5.png")
        minimize_button_img = PhotoImage(file=cwd + os.sep +"assets\\img8.png")
        resize_button_img = PhotoImage(file=cwd + os.sep +"assets\\img7.png")
        clear_log_button_img = PhotoImage(file=cwd + os.sep +"assets\\img9.png")
        canvas_border_img = Image.open(cwd + os.sep +'assets\\img10.png').resize((600,600), Image.ANTIALIAS)
        log_border_img = canvas_border_img.resize((500,600), Image.ANTIALIAS)
        canvas_border_img = ImageTk.PhotoImage(canvas_border_img)
        log_border_img = ImageTk.PhotoImage(log_border_img)
        preview_canvas_img = Image.open(cwd + os.sep +"assets\\img11.png").resize((220,40), Image.ANTIALIAS)
        preview_canvas_img = ImageTk.PhotoImage(preview_canvas_img)

        self.points = [50, 0, 50, 0, 549, 0, 549, 0, 599, 0, 599, 50, 599, 50, 599, 549, 599, 549, 599, 599, 549, 599, 549, 599, 50, 599, 50, 599, 0, 599, 0, 549, 0, 549, 0, 50, 0, 50, 0, 0]

        bg_label = tk.Label(self, image=bg, bg='#FFE15B')
        bg_label.place(x=0, y=0, relwidth=1, relheight=1, anchor='nw')

        #fake Titlebar
        self.title_bar = tk.Frame(self, height=100, width=1150, bg="#FFE15B",bd=20)
        self.title_bar.place(x=129,y=0)
        self.title_bar.bind("<Button-1>", self.startMove)
        self.title_bar.bind("<ButtonRelease-1>", self.stopMove)
        self.title_bar.bind("<B1-Motion>", self.moving)
        self.title_bar.bind("<Map>",self.frame_mapped)
        title_label = tk.Label(self.title_bar, text="Balkae Batch Image Processor", font=("Karla", 25), bg="#FFE15B", fg="black")
        title_label.place(x=0, y=0)
        
        exit_button = tk.Button(self, image=exit_button_img, bg='#FFE15B',highlightthickness = 0, bd = 0,activebackground='#FFE15B')
        exit_button.place(x=1363, y=36)
        exit_button.bind("<Button-1>", self.exitProgram)

        minimize_button = tk.Button(self, image=minimize_button_img, bg='#FFE15B',highlightthickness = 0, bd = 0,activebackground='#FFE15B')
        minimize_button.place(x=1280, y=36)
        minimize_button.bind("<Button-1>", self.minimize)

        input_folder_button = tk.Button(self, image=input_folder_img, command=self.openinputfolder,highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        input_folder_button.place(x=29, y=141)

        output_folder_button = tk.Button(self, image=output_folder_img, command=self.openoutputfolder,highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        output_folder_button.place(x=29, y=245)

        crop_button = tk.Button(self, image=crop_button_img, command=lambda:[self.crop_popup(),self.crop()],highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        crop_button.place(x=29, y=349)

        compress_button = tk.Button(self, image=compress_button_img, command=lambda:[self.compress_popup(),self.compress()],highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        compress_button.place(x=29, y=453)

        resize_button = tk.Button(self, image=resize_button_img, command=lambda:[self.resize_popup(),self.resize()],highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        resize_button.place(x=29, y=557)

        preview_button = tk.Button(self, image=preview_button_img, command=lambda:[self.preview_img(self.input_folder)],highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        preview_button.place(x=29, y=661)

        tk.Checkbutton(self, text="Convert PNG to JPG", variable=self.check_png_jpg, onvalue=1, offvalue=0,font=("Karla", 14), background="#FFE15B",activebackground='#FFE15B').place(x=29, y=890)

        log_label = tk.Label(self, textvariable=self.log_label, font=("Karla", 18), bg="#FFE15B", fg="black")
        log_label.place(x=170, y=150)
        self.log_canvas = tk.Canvas(self, width=500, height= 700, bg='#FFE15B',highlightthickness = 0, bd = 0)
        self.log_canvas_border = self.log_canvas.create_image(0,0,anchor='nw',image=log_border_img)
        self.log_canvas.place(x=170, y=200)
        self.log_box = tk.Text(self, height=20, width=35,background="#FFE15B",highlightthickness = 0, bd = 0,font=("Karla", 10))
        self.log_box.place(x=190, y=235)

        clear_log_button = tk.Button(self, image=clear_log_button_img, command=self.clear_logs,highlightthickness = 0, bd = 0, background='#FFE15B',activebackground='#FFE15B')
        clear_log_button.place(x=29, y=765)

        self.img_canvas = tk.Canvas(self, width=600, height= 600, bg='#FFE15B',highlightthickness = 0, bd = 0)
        self.img_canvas.place(x=800, y=200)
        
        self.preview_text = tk.Text(self, height=1, width=48, background="#FFE15B",highlightthickness = 0, bd = 0,font=("Karla", 18))
        self.preview_text.place(x=840, y=150)
        self.preview_text.insert(tk.END, "No file selected for preview")
        self.preview_text.configure(state='disabled')
        self.image_container = self.img_canvas.create_image(0,0,anchor='nw',image=None)
        self.canvas_border = self.img_canvas.create_image(0,0,anchor='nw',image=canvas_border_img)

        tk.Label(self, text="Input Folder :", font=("Karla", 10), bg="#FFE15B").place(x=10, y=945)
        tk.Label(self, text="Output Folder :", font=("Karla", 10), bg="#FFE15B").place(x=10, y=970)
        self.folder_label = tk.Label(self, textvariable=self.input_folder_path,font=("Karla", 10), background="#FFE15B").place(x=150, y=945)
        self.folder_label = tk.Label(self, textvariable=self.output_folder_path,font=("Karla", 10), background="#FFE15B").place(x=150, y=970)

        '''tk.Label(text="Preview settings\nwarning!!!!!\npreview currently only works with images in input folder and not subfolders\nif you "
                        +"dont see anything it means image from subfolder was selected as random").place(x=800, y=700)'''
        
        self.preview_canvas = tk.Canvas(self, width=270, height= 200, bg='#FFE15B',highlightthickness = 0, bd = 0)
        self.preview_canvas.place(x=1150, y=817)
        self.preview_canvas_border = self.preview_canvas.create_image(0,0,anchor='nw',image=preview_canvas_img)
        self.preview_canvas_border = self.preview_canvas.create_image(0,50,anchor='nw',image=preview_canvas_img)
        self.preview_canvas_border = self.preview_canvas.create_image(0,100,anchor='nw',image=preview_canvas_img)
        self.preview_crop_header=tk.Label(text="Enter size in pixels",font=("Karla", 14), background="#FFE15B")
        self.preview_crop_header.place(x=840, y=820)
        self.preview_crop_width_entry=tk.Entry(background="#FFE15B",highlightthickness = 0, bd = 0,font=("Karla", 14))
        self.preview_crop_width_entry.insert(0,'1000')
        self.preview_crop_width_entry.place(x=1160, y=822, width=70, height=28)
        self.preview_crop_header=tk.Label(text="x",font=("Karla", 11), background="#FFE15B")
        self.preview_crop_header.place(x=1229, y=820)
        self.preview_crop_height_entry=tk.Entry(background="#FFE15B",highlightthickness = 0, bd = 0,font=("Karla", 14))
        self.preview_crop_height_entry.insert(0,'1000')
        self.preview_crop_height_entry.place(x=1250, y=822, width=70, height=28)
        self.preview_horizontal_offset=tk.Label(text="Enter horizontal offset",font=("Karla", 14), background="#FFE15B")
        self.preview_horizontal_offset.place(x=840, y=870)
        self.preview_horizontal_offset_entry=tk.Entry(background="#FFE15B",highlightthickness = 0, bd = 0,font=("Karla", 14))
        self.preview_horizontal_offset_entry.insert(0,'0')
        self.preview_horizontal_offset_entry.place(x=1160, y=872, width=70, height=28)
        self.preview_vertical_offset=tk.Label(text="Enter vertical offset",font=("Karla", 14), background="#FFE15B")
        self.preview_vertical_offset.place(x=840, y=920)
        self.preview_vertical_offset_entry=tk.Entry(background="#FFE15B",highlightthickness = 0, bd = 0,font=("Karla", 14))
        self.preview_vertical_offset_entry.insert(0,'0')
        self.preview_vertical_offset_entry.place(x=1160, y=922, width=70, height=28)
        

        self.wm_iconbitmap("assets\\balkae.ico")
        self.geometry("1440x1024")
        self.resizable(False, False)
        self.overrideredirector(True)
        self.title("BBIP")
        self.mainloop()
    
    def overrideredirector(self, boolean=None):
            tk.Tk.overrideredirect(self, boolean)
            GWL_EXSTYLE=-20
            WS_EX_APPWINDOW=0x00040000
            WS_EX_TOOLWINDOW=0x00000080
            if boolean:
                print("Setting")
                hwnd = windll.user32.GetParent(self.winfo_id())
                style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                style = style & ~WS_EX_TOOLWINDOW
                style = style | WS_EX_APPWINDOW
                res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            self.wm_withdraw()
            self.wm_deiconify()

    def startMove(self, event):
        self.x = event.x +129
        self.y = event.y 

    def stopMove(self, event):
        self.x = None
        self.y = None

    def moving(self,event):
        x = (event.x_root - self.x - self.title_bar.winfo_rootx() + self.title_bar.winfo_rootx())
        y = (event.y_root - self.y - self.title_bar.winfo_rooty() + self.title_bar.winfo_rooty())
        self.geometry("+%s+%s" % (x, y))

    def frame_mapped(self,e):
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')

    def minimize(self, event):
        self.update_idletasks()
        self.overrideredirect(False)
        #self.state('withdrawn')
        self.state('iconic')

    def exitProgram(self, event):
        os._exit(0)


    def preview_img(self,location):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return
        self.image_list= []
        for r, d, f in os.walk(location):
            for item in d:
                self.preview_img(location + os.sep + item)

            for image in f:
                self.image_list.append(image)
        path = location
        image = self.image_list[random.randint(0,len(self.image_list)-1)]
        input_path = path + os.sep + image
        if image.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', 'webp')):
            try:
                opt = Image.open(input_path)
                height,width = opt.size
                crop_size_width = int(int(self.preview_crop_width_entry.get())/2)
                crop_size_height = int(int(self.preview_crop_height_entry.get())/2)
                left=(height//2)-crop_size_width + int(self.preview_horizontal_offset_entry.get())
                top=(width//2)-crop_size_height + int(self.preview_vertical_offset_entry.get())
                right=(height//2)+crop_size_width + int(self.preview_horizontal_offset_entry.get())
                bottom=(width//2)+crop_size_height + int(self.preview_vertical_offset_entry.get())
                temp_float= os.stat(input_path).st_size / 1024
                self.img_preview = opt.crop((left,top,right,bottom)).resize((610,610), Image.ANTIALIAS)
                self.img_preview = ImageTk.PhotoImage(self.img_preview)
                self.img_canvas.itemconfig(self.image_container,image=self.img_preview)
                self.preview_text.configure(state='normal')
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(1.0, str(os.path.basename(input_path)) + " --size " + str(round(temp_float,2)) + " KB")
                self.preview_text.configure(state='disabled')
                self.update()
                
            except:
                pass
        
    def resize(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return
        if self.output_folder == "":
            self.custom_print("Please select an output folder")
            return
        self.reset_variables()
        self.custom_print("Resizing images...")
        resize_width = self.resize_preference_popup.value
        square_size = self.resize_image(self.input_folder,resize_width)
        self.custom_print("-----------------------------------------------------------------")
        self.custom_print('--------------------------SUMMARY-------------------------')
        self.custom_print("Images resized Successfully")
        self.custom_print(f"size of resized image is {square_size}x{square_size} pixels")
        self.custom_print('Files: '  + f'{self.TOTAL_FILES}')

    def crop(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return
        if self.output_folder == "":
            self.custom_print("Please select an output folder")
            return
        self.reset_variables()
        crop_size_width = self.crop_preference_popup.value.split(',')[0]
        crop_size_height = self.crop_preference_popup.value.split(',')[1]
        horizontal_offset = self.crop_preference_popup.value.split(',')[2]
        vertical_offset = self.crop_preference_popup.value.split(',')[3]
        self.crop_image(self.input_folder,crop_size_width,crop_size_height,horizontal_offset,vertical_offset)
        self.custom_print("-----------------------------------------------------------------")
        self.custom_print('--------------------------SUMMARY-------------------------')
        self.custom_print("Images croped Successfully")
        self.custom_print(f"size of croped image is {crop_size_width}x{crop_size_height} pixels")
        self.custom_print('Files: '  + f'{self.TOTAL_FILES}')

    def compress(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return
        if self.output_folder == "":
            self.custom_print("Please select an output folder")
            return
        self.reset_variables()
        compression_quality = self.compress_preference_popup.value
        self.QUALITY = int(compression_quality)
        self.compress_images(self.input_folder)
        self.custom_print("-----------------------------------------------------------------")
        self.custom_print('--------------------------SUMMARY-------------------------')
        self.custom_print('Files: '  + f'{self.TOTAL_FILES}')
        self.custom_print(
            "Original: " + f'{self.TOTAL_ORIGINAL:,.2f}' + " megabytes || " + "New Size: " + f'{self.TOTAL_COMPRESSED:,.2f}' +
            " megabytes" + " || Storage Saved: " + f'{self.TOTAL_GAIN:,.2f}' + " megabytes ~" + f'{(self.TOTAL_GAIN / self.TOTAL_ORIGINAL) * 100:,.2f}'
            + "% reduction")
        self.custom_print("Images compressed Successfully")

    def resize_image(self,location,resize_width):
        for r, d, f in os.walk(location):
            for item in d:
                self.resize_image(location + os.sep + item,resize_width)

            for image in f:
                path = location
                input_path = path + os.sep + image
                out_path = self.output_folder
                if image.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', 'webp')):
                    if os.path.isfile(input_path):
                        opt = None
                        
                        try:
                            opt = Image.open(input_path)
                        except Exception as e:
                            #do nothing just self.custom_print the file skipping
                            self.custom_print(f'skipping file cannot open: {input_path}' + str(e))
                            continue
                        
                        if not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path, exist_ok=True)
                            except OSError as e:
                                #wait for race condition to settle
                                time.sleep(1)
                                # try to create the folder again
                                os.makedirs(out_path, exist_ok=True)
                                if e.errno != errno.EEXIST:
                                    raise
                        
                        out_file = out_path + os.sep + image
                        # Convert .png to .jpg
                        if self.check_png_jpg.get() and image.lower().endswith('.png'):
                            im = opt
                            rgb_im = im.convert('RGB')
                            out_file = out_file.replace(".png", ".jpg")
                            rgb_im.save(out_file)
                            opt = Image.open(out_file)

                        basewidth = int(resize_width)
                        wpercent = (basewidth / float(opt.size[0]))
                        hsize = int((float(opt.size[1]) * float(wpercent)))
                        opt = opt.resize((basewidth, hsize), Image.ANTIALIAS)

                        """height,width = opt.size
                        print((int((width * int(resize_width))/100), int((height * int(resize_width))/100)))
                        opt.resize((int((width * int(resize_width))/100), int((height * int(resize_width))/100)), Image.ANTIALIAS)"""
                        opt.save(out_file, optimize=True)
                        opt.close()

                        self.custom_print(image + ' saved')
                        self.update_image(out_file)
                        self.TOTAL_FILES +=1
                else:
                    if os.path.isdir(out_path) and not os.path.exists(out_path):
                        try:
                            os.makedirs(out_path, exist_ok=True)
                        except OSError as e:
                            #wait for race condition to settle
                            time.sleep(1)
                            # try to create the folder again
                            os.makedirs(out_path, exist_ok=True)
                            if e.errno != errno.EEXIST:
                                raise
                    if os.path.isfile(input_path):
                        
                        if  not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path, exist_ok=True)
                            except OSError as e:
                                #wait for race condition to settle
                                time.sleep(1)
                                # try to create the folder again
                                os.makedirs(out_path, exist_ok=True)
                                if e.errno != errno.EEXIST:
                                    raise        
                        input_file = input_path
                        output_file= input_file.replace('input','outout')        
                        self.custom_print('File not image, copying instead: ' + input_path)
                        subprocess.call('cp ' + input_file + ' ' + output_file, shell=True)

    def openinputfolder(self):
        self.input_folder = filedialog.askdirectory(title="Open folder with input images").replace('/', '\\')
        text = self.input_folder
        if self.input_folder == "":
            text = "None"
            self.custom_print("Please select an input folder")
        self.input_folder_path.set(f"{text}")
    
    def openoutputfolder(self):
        self.output_folder = filedialog.askdirectory(title="Open folder to output images").replace('/', '\\')
        text = self.output_folder
        if self.output_folder == "":
            text = "None"
            self.custom_print("Please select an output folder")
        self.output_folder_path.set(f"{text}")

    def crop_image(self,location,crop_size_width,crop_size_height,horizontal_offset,vertical_offset):
        for r, d, f in os.walk(location):
            for item in d:
                self.crop_image(location + os.sep + item,crop_size_width,crop_size_height,horizontal_offset,vertical_offset)

            for image in f:
                path = location
                input_path = path + os.sep + image
                out_path = self.output_folder
                if image.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', 'webp')):
                    if os.path.isfile(input_path):
                        global TOTAL_GAIN
                        global TOTAL_ORIGINAL
                        global TOTAL_COMPRESSED
                        global TOTAL_FILES
                        global QUALITY
                        opt = None
                        
                        try:
                            opt = Image.open(input_path)
                        except Exception as e:
                            #do nothing just self.custom_print the file skipping
                            self.custom_print(f'skipping file cannot open: {input_path}' + str(e))
                            continue
                        
                        if not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path, exist_ok=True)
                            except OSError as e:
                                #wait for race condition to settle
                                time.sleep(1)
                                # try to create the folder again
                                os.makedirs(out_path, exist_ok=True)
                                if e.errno != errno.EEXIST:
                                    raise
                        
                        out_file = out_path + os.sep + image
                        # Convert .png to .jpg
                        if self.check_png_jpg.get() and image.lower().endswith('.png'):
                            im = opt
                            rgb_im = im.convert('RGB')
                            out_file = out_file.replace(".png", ".jpg")
                            rgb_im.save(out_file)
                            opt = Image.open(out_file)

                        height,width = opt.size
                        left=(height//2)-int(crop_size_width)//2 + int(horizontal_offset)
                        top=(width//2)-int(crop_size_height)//2 + int(vertical_offset)
                        right=(height//2)+int(crop_size_width)//2 + int(horizontal_offset)
                        bottom=(width//2)+int(crop_size_height)//2 + int(vertical_offset)

                        img = opt.crop((left,top,right,bottom))
                        img.save(out_file, optimize=True, quality=self.QUALITY)
                        opt.close()

                        self.custom_print(image + ' saved')
                        self.update_image(out_file)
                        self.TOTAL_FILES +=1
                else:
                    if os.path.isdir(out_path) and not os.path.exists(out_path):
                        try:
                            os.makedirs(out_path, exist_ok=True)
                        except OSError as e:
                            #wait for race condition to settle
                            time.sleep(1)
                            # try to create the folder again
                            os.makedirs(out_path, exist_ok=True)
                            if e.errno != errno.EEXIST:
                                raise
                    if os.path.isfile(input_path):
                        
                        if  not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path, exist_ok=True)
                            except OSError as e:
                                #wait for race condition to settle
                                time.sleep(1)
                                # try to create the folder again
                                os.makedirs(out_path, exist_ok=True)
                                if e.errno != errno.EEXIST:
                                    raise        
                        input_file = input_path
                        output_file= input_file.replace('input','outout')        
                        self.custom_print('File not image, copying instead: ' + input_path)
                        subprocess.call('cp ' + input_file + ' ' + output_file, shell=True)

    def compress_images(self,location):
        for r, d, f in os.walk(location):
            for item in d:
                self.compress_images(location + os.sep + item)

            for image in f:
                path = location
                input_path = path + os.sep + image
                out_path = self.output_folder
                if image.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', 'webp')):
                    if os.path.isfile(input_path):
                        
                        opt = None
                        
                        try:
                            opt = Image.open(input_path)
                        except:
                            #do nothing just self.custom_print the file skipping
                            self.custom_print(f'skipping file cannot open: {input_path}')
                            continue
                            
                        original_size = os.stat(input_path).st_size / 1024 / 1024
                        self.TOTAL_ORIGINAL += original_size
                        self.custom_print("Original size: " + f'{original_size:,.2f}' + " megabytes")
                        if not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path, exist_ok=True)
                            except OSError as e:
                                #wait for race condition to settle
                                time.sleep(1)
                                # try to create the folder again
                                os.makedirs(out_path, exist_ok=True)
                                if e.errno != errno.EEXIST:
                                    raise
                        
                        out_file= out_path + os.sep + image
                        # Convert .pgn to .jpg
                        if self.check_png_jpg.get() and image.lower().endswith('.png'):
                            im = opt
                            rgb_im = im.convert('RGB')
                            out_file = out_file.replace(".png", ".jpg")
                            rgb_im.save(out_file)
                            opt = Image.open(out_file)

                        opt.save(out_file, optimize=True, quality=self.QUALITY)
                        opt = Image.open(out_file)
                        compressed_size = os.stat(out_file).st_size / 1024 / 1024
                        self.TOTAL_COMPRESSED += compressed_size
                        gain = original_size - compressed_size
                        self.TOTAL_GAIN += gain
                        self.TOTAL_FILES +=1
                        self.update_image(out_file)
                        self.custom_print("Compressed size: " + f'{compressed_size:,.2f}' + " megabytes")
                        self.custom_print("Gain : " + f'{gain:,.2f}' + " megabytes")
                        opt.close()
                else:
                    if os.path.isdir(out_path) and not os.path.exists(out_path):
                        try:
                            os.makedirs(out_path, exist_ok=True)
                        except OSError as e:
                            #wait for race condition to settle
                            time.sleep(1)
                            # try to create the folder again
                            os.makedirs(out_path, exist_ok=True)
                            if e.errno != errno.EEXIST:
                                raise
                    if os.path.isfile(input_path):
                        
                        if  not os.path.exists(out_path):
                            try:
                                os.makedirs(out_path, exist_ok=True)
                            except OSError as e:
                                #wait for race condition to settle
                                time.sleep(1)
                                # try to create the folder again
                                os.makedirs(out_path, exist_ok=True)
                                if e.errno != errno.EEXIST:
                                    raise        
                        input_file = input_path
                        output_file= input_file.replace('input','outout')        
                        self.custom_print('File not image, copying instead: ' + input_path)
                        subprocess.call('cp ' + input_file + ' ' + output_file, shell=True)
        
    def custom_print(self,msg):
        self.log_box.insert(tk.END, msg + '\n')
        self.log_box.see(tk.END)
        self.update()

    def crop_popup(self):
        self.crop_preference_popup=crop_popupWindow(self,self.preview_crop_width_entry,self.preview_crop_height_entry,self.preview_horizontal_offset_entry,self.preview_vertical_offset_entry)
        self.wait_window(self.crop_preference_popup.top)

    def compress_popup(self):
        self.compress_preference_popup=compress_popupWindow(self)
        self.wait_window(self.compress_preference_popup.top)
        
    def resize_popup(self):
        self.resize_preference_popup=resize_popupWindow(self)
        self.wait_window(self.resize_preference_popup.top)

    def clear_logs(self):
        self.log_box.delete(1.0, tk.END)

    def check_folder(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return

    def update_image(self,path):
        img = Image.open(path).resize((610,610), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.img_canvas.itemconfig(self.image_container,image=img)
        self.update()

    def reset_variables(self):
        self.TOTAL_ORIGINAL = 1
        self.TOTAL_COMPRESSED = 0
        self.TOTAL_GAIN = 0
        self.TOTAL_FILES = 0

    def sidebar(self):
        return
if __name__ == '__main__':
    App()