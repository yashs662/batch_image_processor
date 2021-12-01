# batch_image_processor
Batch process images 
  convert all images in a input folder and sub folders in one click
  simple toggle to convert images to jpg from png
  preview window to dial-in settings
  
parameter descriptions:
  size of cropped image = final count of pixels in the image(can be lower or higher than source)
  horizontal offset = number of pixels to offset the image on the x axis (+ve or -ve)
  vertical offset = number of pixels to offset the image on the y axis (+ve or -ve)
  compression quality = 90-100 high quality below 90 quality decreases exponentially (1 results in highly pixelated image)
  
preview settings to preview on a random image before starting the batch job

known limitations:
currently it does not support displaying preview images for images in subfolders(images in sub folders will be processed in the batch job)

This app was buit for the internal workings of Balkae.com but you can customize it and suggest/help with improvements to the app
This app was built using python and tkinter library

a working installer made with inno installer is also available
