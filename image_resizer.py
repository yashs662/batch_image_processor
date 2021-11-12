
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


# Iterate through every image
# and resize all the images.
    
class resize_popupWindow(object):
    def __init__(self,master,preview_resize_entry,preview_horizontal_offset,preview_vertical_offset):
        super().__init__()
        self.preview_resize_entry=preview_resize_entry
        self.preview_horizontal_offset=preview_horizontal_offset
        self.preview_vertical_offset=preview_vertical_offset
        top=self.top=tk.Toplevel(master)
        self.title_label=tk.Label(top,text="Choose Preferences")
        self.title_label.pack(pady=10,padx=10)
        self.resize_header=tk.Label(top,text="enter the size of the cropped image")
        self.resize_header.pack(pady=10,padx=10)
        self.resize_entry=tk.Entry(top)
        self.resize_entry.insert(0,'1024')
        self.resize_entry.pack(pady=10,padx=10)
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
        top.iconbitmap("E:\\All_programming\\python_programming\\image resize\\exe\\balkae.ico")
        top.resizable(False, False)
    def cleanup(self):
        self.value=','.join([self.resize_entry.get(),self.horizontal_offset.get(),self.vertical_offset.get()])
        self.top.destroy()
    def use_preview_settings(self):
        self.value=','.join([self.preview_resize_entry.get(),self.preview_horizontal_offset.get(),self.preview_vertical_offset.get()])
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
        top.iconbitmap("E:\\All_programming\\python_programming\\image resize\\exe\\balkae.ico")
        top.resizable(False, False)
    def cleanup(self):
        self.value=','.join([self.compression_entry.get()])
        self.top.destroy()

class resize_and_compress_popupWindow(object):
    def __init__(self,master,preview_resize_entry,preview_horizontal_offset,preview_vertical_offset):
        super().__init__()
        self.preview_resize_entry=preview_resize_entry
        self.preview_horizontal_offset=preview_horizontal_offset
        self.preview_vertical_offset=preview_vertical_offset
        top=self.top=tk.Toplevel(master)
        self.title_label=tk.Label(top,text="Choose Preferences")
        self.title_label.pack(pady=10,padx=10)
        self.resize_header=tk.Label(top,text="enter the size of the cropped image")
        self.resize_header.pack(pady=10,padx=10)
        self.resize_entry=tk.Entry(top)
        self.resize_entry.insert(0,'1024')
        self.resize_entry.pack(pady=10,padx=10)
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
        self.compression_header=tk.Label(top,text="enter the quality of compression (0-100)\nnote compression quality decreases exponentially from 100 to 0")
        self.compression_header.pack(pady=10,padx=10)
        self.compression_entry=tk.Entry(top)
        self.compression_entry.insert(0,'95')
        self.compression_entry.pack(pady=10,padx=10)
        self.submit_button=tk.Button(top,text='use preview settings',command=self.use_preview_settings)
        self.submit_button.pack()
        self.submit_button=tk.Button(top,text='Ok',command=self.cleanup)
        self.submit_button.pack()
        top.iconbitmap("E:\\All_programming\\python_programming\\image resize\\exe\\balkae.ico")
        top.resizable(False, False)
    def cleanup(self):
        self.value=','.join([self.resize_entry.get(),self.horizontal_offset.get(),self.vertical_offset.get(),self.compression_entry.get()])
        self.top.destroy()
    def use_preview_settings(self):
        self.value=','.join([self.preview_resize_entry.get(),self.preview_horizontal_offset.get(),self.preview_vertical_offset.get(),self.compression_entry.get()])
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

        self.title("Balkae Batch Image Processor")
        self.input_folder = ""
        self.output_folder = ""
        self.input_folder_path = tk.StringVar()
        self.input_folder_path.set("No folder selected")
        self.output_folder_path = tk.StringVar()
        self.output_folder_path.set("No folder selected")
        self.log_label = tk.StringVar()
        self.log_label.set("Logs")
        self.log_label = tk.StringVar()
        self.log_label.set("No file selected for preview")
        tk.Button(self, text='Select input folder', command=self.openinputfolder,font=("Arial", 15)).grid(row=0, column=0, sticky=tk.W, pady=4)
        self.folder_label = tk.Label(self, textvariable=self.input_folder_path,font=("Arial", 15)).place(x=200, y=15)
        tk.Button(self, text='Select output folder', command=self.openoutputfolder,font=("Arial", 15)).grid(row=1, column=0, sticky=tk.W, pady=4)
        self.folder_label = tk.Label(self, textvariable=self.output_folder_path,font=("Arial", 15)).place(x=200, y=55)
        tk.Button(self, text='Resize and compress', command=lambda:[self.resize_and_compress_popup(),self.resize_and_compress()],font=("Arial", 15)).grid(row=2, column=0, sticky=tk.W, pady=4)
        tk.Button(self, text='Compress images', command=lambda:[self.compress_popup(),self.compress()],font=("Arial", 15)).grid(row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(self, text='Resize images' , command=lambda:[self.resize_popup(),self.resize()],font=("Arial", 15)).grid(row=4, column=0, sticky=tk.W, pady=4)
        tk.Checkbutton(self, text="Convert PNG to JPG", variable=self.check_png_jpg, onvalue=1, offvalue=0,font=("Arial", 15)).grid(row=6, column=0, sticky=tk.W, pady=4)
        tk.Label(self, textvariable=self.log_label,font=("Arial", 15)).grid(row=7, column=0, sticky=tk.W, pady=4)
        self.log_box = tk.Text(self, height=10, width=100)
        self.log_box.grid(row=8, column=0, sticky=tk.W, pady=4)
        scrollb = tk.Scrollbar(self, command=self.log_box.yview)
        scrollb.grid(row=8, column=1, sticky='nsew')
        self.log_box['yscrollcommand'] = scrollb.set
        self.clear_log_bttn=tk.Button(self,text="Clear logs",command=self.clear_logs,font=("Arial", 15))
        self.clear_log_bttn.grid(row=9,column=0,sticky=tk.W,pady=4)
        self.img_canvas = tk.Canvas(self, width=400, height= 400,borderwidth=0,highlightthickness=5,highlightbackground="#ffe15b",relief='ridge')
        self.img_canvas.place(x=840, y=100)
        self.preview_text = tk.Text(self, height=3, width=48)
        self.preview_text.place(x=851, y=520)
        self.preview_text.insert(tk.END, "No file selected for preview")
        self.preview_text.configure(state='disabled')
        self.image_container = self.img_canvas.create_image(0,0,anchor='nw',image=None)

        tk.Label(text="Preview settings\nwarning!!!!!\npreview currently only works with images in input folder and not subfolders\nif you dont see anything it means image from subfolder was selected as random").grid(row=10,column=0)
        self.preview_resize_header=tk.Label(text="enter the size of the cropped image")
        self.preview_resize_header.grid(row=11, column=0)
        self.preview_resize_entry=tk.Entry()
        self.preview_resize_entry.insert(0,'1024')
        self.preview_resize_entry.grid(row=12, column=0)
        self.preview_horizontal_offset=tk.Label(text="Enter horizontal offset")
        self.preview_horizontal_offset.grid(row=13, column=0)
        self.preview_horizontal_offset_entry=tk.Entry()
        self.preview_horizontal_offset_entry.insert(0,'0')
        self.preview_horizontal_offset_entry.grid(row=14, column=0)
        self.preview_vertical_offset=tk.Label(text="Enter vertical offset")
        self.preview_vertical_offset.grid(row=15, column=0)
        self.preview_vertical_offset_entry=tk.Entry()
        self.preview_vertical_offset_entry.insert(0,'0')
        self.preview_vertical_offset_entry.grid(row=16, column=0)
        self.preview_bttn=tk.Button(text="Generate random preview",command=lambda:[self.preview_img(self.input_folder)])
        self.preview_bttn.grid(row=17, column=0)

        self.iconbitmap("E:\\All_programming\\python_programming\\image resize\\exe\\balkae.ico")
        self.geometry("1280x750")
        self.resizable(False, False)
        self.mainloop()
        
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
                crop_size = int(int(self.preview_resize_entry.get())/2)

                left=(height//2)-crop_size + int(self.preview_horizontal_offset_entry.get())
                top=(width//2)-crop_size + int(self.preview_vertical_offset_entry.get())
                right=(height//2)+crop_size + int(self.preview_horizontal_offset_entry.get())
                bottom=(width//2)+crop_size + int(self.preview_vertical_offset_entry.get())
                temp_float= os.stat(input_path).st_size / 1024
                self.img_preview = opt.crop((left,top,right,bottom)).resize((410,410), Image.ANTIALIAS)
                self.img_preview = ImageTk.PhotoImage(self.img_preview)
                self.img_canvas.itemconfig(self.image_container,image=self.img_preview)
                self.preview_text.configure(state='normal')
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(1.0, str(os.path.basename(input_path)) + " --size " + str(round(temp_float,2)) + " KB")
                self.preview_text.configure(state='disabled')
                self.update()
                
            except:
                pass
        
    def resize_and_compress(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return
        if self.output_folder == "":
            self.custom_print("Please select an output folder")
            return
        self.reset_variables()
        square_size = self.resize_and_compress_preference_popup.value.split(',')[0]
        horizontal_offset = self.resize_and_compress_preference_popup.value.split(',')[1]
        vertical_offset = self.resize_and_compress_preference_popup.value.split(',')[2]
        compression_quality = self.resize_and_compress_preference_popup.value.split(',')[3]
        self.QUALITY = int(compression_quality)
        self.resize_image(self.input_folder,square_size,horizontal_offset,vertical_offset)
        self.custom_print("--------------------------------------------------------------------------------")
        self.custom_print('-------------------------------------SUMMARY------------------------------------')
        self.custom_print("Images resized Successfully")
        self.custom_print(f"size of resized image is {square_size}x{square_size} pixels")
        self.custom_print('Files: '  + f'{self.TOTAL_FILES}')
        self.compress_images(self.output_folder)
        self.custom_print(
            "Original: " + f'{self.TOTAL_ORIGINAL:,.2f}' + " megabytes || " + "New Size: " + f'{self.TOTAL_COMPRESSED:,.2f}' +
            " megabytes" + " || Storage Saved: " + f'{self.TOTAL_GAIN:,.2f}' + " megabytes ~" + f'{(self.TOTAL_GAIN / self.TOTAL_ORIGINAL) * 100:,.2f}'
            + "% reduction")
        self.custom_print("Images compressed Successfully")

    def resize(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return
        if self.output_folder == "":
            self.custom_print("Please select an output folder")
            return
        self.reset_variables()
        square_size = self.resize_preference_popup.value.split(',')[0]
        horizontal_offset = self.resize_preference_popup.value.split(',')[1]
        vertical_offset = self.resize_preference_popup.value.split(',')[2]
        self.resize_image(self.input_folder,square_size,horizontal_offset,vertical_offset)
        self.custom_print("----------------------------------------------------------------------------------------------------")
        self.custom_print('-----------------------------------------------SUMMARY----------------------------------------------')
        self.custom_print("Images resized Successfully")
        self.custom_print(f"size of resized image is {square_size}x{square_size} pixels")
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
        self.custom_print("----------------------------------------------------------------------------------------------------")
        self.custom_print('-----------------------------------------------SUMMARY----------------------------------------------')
        self.custom_print('Files: '  + f'{self.TOTAL_FILES}')
        self.custom_print(
            "Original: " + f'{self.TOTAL_ORIGINAL:,.2f}' + " megabytes || " + "New Size: " + f'{self.TOTAL_COMPRESSED:,.2f}' +
            " megabytes" + " || Storage Saved: " + f'{self.TOTAL_GAIN:,.2f}' + " megabytes ~" + f'{(self.TOTAL_GAIN / self.TOTAL_ORIGINAL) * 100:,.2f}'
            + "% reduction")
        self.custom_print("Images compressed Successfully")

    def openinputfolder(self):
        self.input_folder = filedialog.askdirectory(title="Open folder with input images").replace('/', '\\')
        text = self.input_folder
        if self.input_folder == "":
            text = "None"
            self.custom_print("Please select an input folder")
        self.input_folder_path.set(f"input folder {text}")
    
    def openoutputfolder(self):
        self.output_folder = filedialog.askdirectory(title="Open folder to output images").replace('/', '\\')
        text = self.output_folder
        if self.output_folder == "":
            text = "None"
            self.custom_print("Please select an output folder")
        self.output_folder_path.set(f"output folder {text}")

    def resize_image(self,location,box_size,horizontal_offset,vertical_offset):
        for r, d, f in os.walk(location):
            for item in d:
                self.resize_image(location + os.sep + item,box_size,horizontal_offset,vertical_offset)

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
                        crop_size = int(int(box_size)/2)

                        left=(height//2)-crop_size + int(horizontal_offset)
                        top=(width//2)-crop_size + int(vertical_offset)
                        right=(height//2)+crop_size + int(horizontal_offset)
                        bottom=(width//2)+crop_size + int(vertical_offset)

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

    '''def preview_popup(self):
        self.preview_preference_popup=preview(self)
        self.wait_window(self.preview_preference_popup.top)'''

    def resize_popup(self):
        self.resize_preference_popup=resize_popupWindow(self,self.preview_resize_entry,self.preview_horizontal_offset_entry,self.preview_vertical_offset_entry)
        self.wait_window(self.resize_preference_popup.top)

    def compress_popup(self):
        self.compress_preference_popup=compress_popupWindow(self)
        self.wait_window(self.compress_preference_popup.top)
        
    def resize_and_compress_popup(self):
        self.resize_and_compress_preference_popup=resize_and_compress_popupWindow(self,self.preview_resize_entry,self.preview_horizontal_offset_entry,self.preview_vertical_offset_entry)
        self.wait_window(self.resize_and_compress_preference_popup.top)

    def clear_logs(self):
        self.log_box.delete(1.0, tk.END)

    def check_folder(self):
        if self.input_folder == "":
            self.custom_print("Please select an input folder")
            return

    def update_image(self,path):
        img = Image.open(path).resize((410,410), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.img_canvas.itemconfig(self.image_container,image=img)
        self.update()

    def reset_variables(self):
        self.TOTAL_ORIGINAL = 1
        self.TOTAL_COMPRESSED = 0
        self.TOTAL_GAIN = 0
        self.TOTAL_FILES = 0

if __name__ == '__main__':
    App()
    global innput_folder