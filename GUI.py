from tkinter import *
from tkinter.scrolledtext import ScrolledText

from PIL import ImageTk, Image
import pandas as pd

# from automation import Automation

class GUI(Frame):
    def __init__(self, master):
        super().__init__(master)

        lf1 = LabelFrame(self, text = 'folder paths')
        lf2 = LabelFrame(self, text = 'time for each convert (s)')
        lf3 = LabelFrame(self, text = 'choose file type:', fg = 'green')
        self.countL1 = Label(self,font=("Times New Roman", 18, 'bold'), width = 50)
        self.countL2 = Label(self,font=("Times New Roman", 10, 'bold'), width = 105)
        self.countL3 = Label(self,font=("Times New Roman", 13, 'bold'))
        lf4 = LabelFrame(self, text = 'log')
        self.startB = Button(self, text = 'start', fg = 'blue')
        self.startB.grid(row = 0, column = 0, padx = (5,5))

        lf1.grid(row = 0, column = 1, padx = (5,5))
        lf2.grid(row = 0, column = 2, padx = (5,0), sticky = 'n')
        lf3.grid(row =1, column = 0, columnspan = 3, pady= (0,5), sticky = 'n')
        self.countL1.grid(row = 2, column = 0,  columnspan =3, pady = (5,5))
        self.countL2.grid(row = 3, column = 0,  columnspan =3, pady = (5,5))
        self.countL3.grid(row = 4, column = 0,  columnspan =3, pady = (5,5))
        lf4.grid(row = 5, column = 0, columnspan =3, pady = (20,5))

        self.raw_var = IntVar()
        self.Y_var = IntVar()
        self.XY_var = IntVar()
        self.XYE_var = IntVar()
        self.SAXS_var = IntVar()
        self.XY_var.set(1)
        Checkbutton(lf3, text = 'RAW files (*.raw)', variable = self.raw_var, onvalue = 1, offvalue =0, width =12).pack(side = 'left', padx = (2,2))
        Checkbutton(lf3, text = 'Y files (*.y)', variable = self.Y_var, onvalue = 1, offvalue =0, width =12).pack(side = 'left', padx = (2,2))
        Checkbutton(lf3, text = 'XY files (*.xy)', state = 'disabled', variable = self.XY_var, onvalue = 1, offvalue =0, width =12).pack(side = 'left', padx = (2,2))
        Checkbutton(lf3, text = 'XYE files (*.xye)', variable = self.XYE_var, onvalue = 1, offvalue =0, width =12).pack(side = 'left', padx = (2,2))
        Checkbutton(lf3, text = 'SAXS files (*.dat)', variable = self.SAXS_var, onvalue = 1, offvalue =0, width =12).pack(side = 'left', padx = (2,2))


        Label(self, text = 'put diffrac.eva software on the 1st position of Taskbar, then press "start"', fg = 'red').grid(row = 6, column = 0, columnspan =3)
        self.stopB = Button(self, text = 'STOP' +'\n'+ 'or press <Esc>', width = 80, height = 5, bg = 'lightgray')
        self.stopB.grid(row = 7, column = 0, columnspan = 3, pady = (5,5))

        self.folderPath = FolderPaths(lf1)
        # self.folderPath = Entry(lf1, width = 85)
        self.folderPath.pack()

        self.pauseTime = Entry(lf2, width = 6)
        self.pauseTime.insert(0, '3')
        self.pauseTime.pack()

        self.log = ScrolledText(lf4, height = 20, width = 120, font=("Times New Roman", 9))
        self.log.pack()

        master.bind("<F5>", self.on_start)


    def on_start(self, e):
        print('df')


    def get_selected_filetype(self):
        filetypes = ['raw', 'y', 'xy', 'xye', 'dat']
        return {f1:pos for pos, (f1, f2) in enumerate(zip(filetypes, [self.raw_var,self.Y_var,self.XY_var,self.XYE_var,self.SAXS_var])) if f2.get()}




class FolderPaths(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.n = 0 # path number
        #the whole frame :
        #{'l_path':l, 'entry':fP, 'b_remove':b_remove, 'l_status':l_status}
        self.e_paths = []


        b_add = Button(self, text = 'add path +', fg = 'red', command = self.add_path)
        b_add.pack(side = 'top', anchor = 'e', padx = (2,5), pady = (0,2))

        self.add_path()


    def add_path(self):
        self.n += 1
        f = Frame(self)
        f.pack()

        blank = ImageTk.PhotoImage(Image.open('blank.png'))

        l = Label(f,text = f'folder path {self.n}:', width =10)
        fP = Entry(f, width = 72)
        b_remove = Button(f, text = '-', fg = 'black',width =2, height = 1, command = lambda f = f, fP = fP: self.on_remove(f, fP))
        l_status = Label(f, image = blank)

        l.grid(row =0, column =0, sticky = 'w')
        fP.grid(row =0, column =1, sticky = 'w')
        b_remove.grid(row =0, column =2, padx = (2,2), pady =(2,2), sticky = 'w')
        l_status.grid(row =0, column =3, padx = (2,2), pady =(2,2), sticky = 'w')

        self.e_paths.append({'l_path':l, 'entry':fP, 'b_remove':b_remove, 'l_status':l_status})

    def on_remove(self,f, fP):
        f.destroy()
        for e_path in self.e_paths:
            if fP in e_path.values():
                self.e_paths.remove(e_path)

    def widgets_disabled(self):
        [e_path['b_remove'].config(state = 'disabled') for e_path in self.e_paths]
        [e_path['entry'].config(state = 'disabled') for e_path in self.e_paths]

    def widgets_normal(self):
        [e_path['b_remove'].config(state = 'normal') for e_path in self.e_paths]
        [e_path['entry'].config(state = 'normal') for e_path in self.e_paths]


    def get_e_paths(self):
        return [e_path['entry'] for e_path in self.e_paths]












def main():
    root = Tk()
    root.title('convert 2D XRD to 1D pattern')
    app = GUI(root)
    app.pack()

    root.mainloop()



if __name__ == '__main__':
    main()
