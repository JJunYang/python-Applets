from removebg import RemoveBg
import os

rmbg = RemoveBg("qtKpc8PW4VvfGtYxoAxbcGYd", "error.log")

# remove certain img file:
# rmbg.remove_background_from_img_file("img.jpeg")

# remove all imgs in file:
# path = 'image'
# for pic in os.listdir(path):
#     img_path = os.path.join(path, pic)
#     rmbg.remove_background_from_img_file(img_path)
#     print(f'{img_path} is done')

# remove from url
# rmbg.remove_background_from_img_url(
#     "https://images.unsplash.com/photo-1537511446984-935f663eb1f4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60")


def remove_bg(path):
    rmbg.remove_background_from_img_file(path)
