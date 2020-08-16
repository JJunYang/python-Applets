import os
from tkinter import Tk, Menu, Label, Button
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showinfo

from auto_delete_bg import remove_bg

path = ''


class GUI(object):

    def __init__(self, window):
        self.window = window
        self.window.geometry('500x200')

        # show
        self.l = Label(window, text='')
        self.l.pack(padx=5, pady=10)

        # select pic
        btn1 = Button(window, text='select pic', width=15,
                      height=2, command=self.get_img)
        btn1.pack()

        # delete background button
        send_btn = Button(
            window, text='delete background', width=15, height=2, command=self.delete_img)
        send_btn.pack()

    def get_img(self):
        global path
        filenames = askopenfilenames(filetypes=(
            ("jpeg img", "*.jpeg"), ("jpg img", "*.jpg"), ("png img", "*.png")))
        if len(filenames) > 0:
            filelist = [fn for fn in filenames]
            fnstr = '\n'.join(filelist)
            self.l.config(text=fnstr)
            path = filelist
        else:
            self.l.config(text='no file selected')

    def delete_img(self):
        global path
        respathList = []
        for imgpath in path:
            filepath, tempfilename = os.path.split(imgpath)
            filename, extension = os.path.splitext(tempfilename)
            remove_bg(imgpath)
            respathList.append(imgpath)
        respath = ' '.join(respathList)
        showinfo('complete', f'finished,path:{respath}')


if __name__ == '__main__':
    window = Tk()
    window.title("Remove picture background")
    GUI(window)
    window.mainloop()
