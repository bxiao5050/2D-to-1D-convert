from tkinter import *
from tkinter.filedialog import askdirectory
import pyperclip
import pyautogui
import time
import os
import threading
import random
from PIL import ImageTk, Image
from random import randrange
import numpy as np

from formattedScanlist import FormattedScanlist
from GUI import GUI





class Automation(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.gui = GUI(master)
        self.gui.pack()
        # master.bind("<F5>", self.on_start)
        self.gui.startB.config(command = self.on_start)
        self.gui.stopB.config(command = self.on_terminate)



        self.ongoing = [ImageTk.PhotoImage(Image.open('ongoing1.png')), ImageTk.PhotoImage(Image.open('ongoing2.png')), ImageTk.PhotoImage(Image.open('ongoing3.png'))]
        self.blank = ImageTk.PhotoImage(Image.open('blank.png'))

        self.finish = ImageTk.PhotoImage(Image.open('finish.png'))
        self.fail = ImageTk.PhotoImage(Image.open('fail.png'))





    def on_terminate(self):
        self.terminate_flag = True

    def mysleep(self, t):
        if self.terminate_flag is True:
            return
        else:
            time.sleep(t)
    def mytypewrite(self, key):
        if self.terminate_flag is True:
            return
        else:
            pyautogui.typewrite(key)




    def on_start(self):
        self.l_status = self.gui.folderPath.e_paths[0]['l_status']
        [e_path['l_status'].config(image = self.blank) for e_path in self.gui.folderPath.e_paths] # label statu
        self.gui.folderPath.widgets_disabled()
        self.gui.startB.config(state = 'disabled')
        [e.config(fg = 'black', bg = 'white') for e in self.gui.folderPath.get_e_paths()]
        self.gui.pauseTime.config(state = 'disabled')

        self.gui.log.delete('1.0', 'end')
        self.terminate_flag = False
        self.finished_frames = 0
        self.getFocused = False # win + 1 to get focus
        self.isFirstRound = True

        self.xy_filename = ''
        self.runInf = ''



        try:
            threading.Thread(target=self.run).start()
            threading.Thread(target=self.executionTime).start()
            threading.Thread(target=self.display).start()
        except:
            self.terminate_flag = True
            self.gui.startB.config(state = 'normal')
            self.gui.folderPath.config(state = 'normal')
            self.gui.pauseTime.config(state = 'normal')
            self.gui.countL1.config(text = f'(stopped)    {self.finished_frames} data are finished', fg = 'red')

    def executionTime(self):
        start = time.time()
        while True:
            if self.terminate_flag == False:
                self.gui.countL3.config(text = f'execution time: {self.convert(time.time() - start)}' , fg = 'gray')
                self.l_status.config(image = self.ongoing[randrange(3)])
                self.mysleep(0.2)
            else:
                return
    def display(self):
           while True:
            if self.terminate_flag == False:
                suffix = ''
                for i, image in enumerate(self.ongoing):
                    suffix += '.'
                    for j in range(40):
                        self.gui.countL2.config(text =  f'{self.runInf}' + suffix, fg = 'gray')
                        self.mysleep(0.05)

            else:
                return

    def run(self):
        pauseTime = float(self.gui.pauseTime.get())
        for e_path in self.gui.folderPath.e_paths:
            self.workPath = e_path['entry'].get()
            #highlight the folder path
            self.l_status = e_path['l_status']
            # self.l_status.config(image = self.finish)
            # self.gui.log.see('end')r
            # self.gui.log.insert('end',  + '\n', 'red')
            text = e_path["l_path"].cget("text")
            self.add_to_log(f'================= {text} ===================')
            frames = FormattedScanlist(workPath = self.workPath).frames()
            total_frames = len(frames['diffName'])
            self.finished_frames = 0

            stableRunTime = 0

            for frameblock in frames['diffName']:
                if self.terminate_flag == True:
                    self.gui.countL1.config(text = f'(stopped)    {self.finished_frames} data are finished', fg = 'red')
                    self.initialization()
                    return
                self.xy_filename_base = frameblock.split('.gfrm')[0].replace('"','')
                self.xy_filename = self.xy_filename_base + '_exported.xy'
                self.runInf  =  f'convert "{self.xy_filename_base}"'
                #check if the 1D pattern already exists
                if os.path.exists(os.path.join(self.workPath, self.xy_filename)):
                    self.finished_frames +=1
                    # self.gui.log.see('end')
                    # self.gui.log.insert('end', +'\n')
                    self.add_to_log(f'{self.finished_frames} -- exists   "{self.xy_filename}"')
                    self.gui.countL1.config(text = f'total data: {total_frames}         finished: {self.finished_frames}' ,fg = 'black')
                    continue

                self.gui.countL1.config(text = f'total data: {total_frames}         finished: {self.finished_frames}',fg = 'black')
                self.oneround(frameblock, pauseTime)
                iteration_N = 0 # record the iteration times
                stableRunTime += 1
                if stableRunTime >=2 and pauseTime >1:
                    pauseTime -= (0.07 + random.random()/20)
                    self.gui.pauseTime.config(state = 'normal')
                    self.gui.pauseTime.delete(0, 'end')
                    self.gui.pauseTime.insert(0, np.round(pauseTime,2))
                    self.gui.pauseTime.config(state = 'disabled')
                    stableRunTime = 0
                # trialTimes = 0 # how many times did I try
                while True:
                    if self.terminate_flag == True:
                        self.gui.countL1.config(text = f'(stopped)    {self.finished_frames} data are finished', fg = 'red')
                        self.initialization()
                        return
                    iteration_N +=1
                    self.mysleep(0.04)
                    # if pauseTime > 10:
                    #     pauseTime = 5
                    #     self.gui.pauseTime.delete(0, 'end')
                    #     self.gui.pauseTime.insert(0, np.round(pauseTime,2))
                    if os.path.exists(os.path.join(self.workPath, self.xy_filename)):
                        self.finished_frames +=1
                        self.runInf  =  f'obtained "{self.xy_filename_base}"'
                        # self.gui.log.see('end')
                        # self.gui.log.insert('end', +'\n')
                        self.add_to_log(f'{self.finished_frames} ---> obtained   "{self.xy_filename}"')
                        self.gui.countL1.config(text = f'total data: {total_frames}         finished: {self.finished_frames}' ,fg = 'black')
                        break
                    if iteration_N > 100 and iteration_N < 106: #re-do it after waiting for 5s
                        self.runInf  =  f'failed to obtain "{self.xy_filename_base}", try again'
                        self.mytypewrite(['enter','esc','esc'])
                        self.mysleep(pauseTime/50)
                        self.mytypewrite(['enter','esc','esc'])
                        self.mysleep(pauseTime/50)
                        self.mytypewrite(['enter','esc','esc'])
                        pauseTime += 0.3 + random.random()/7
                        stableRunTime = 0
                        self.gui.pauseTime.config(state = 'normal')
                        self.gui.pauseTime.delete(0, 'end')
                        self.gui.pauseTime.insert(0, np.round(pauseTime,2))
                        self.gui.pauseTime.config(state = 'disabled')
                        self.oneround(frameblock, pauseTime)
                    elif iteration_N >= 106 and iteration_N <108:
                        self.runInf  =  f'failed to obtain "{self.xy_filename_base}", increase time and try again'
                        self.mytypewrite(['enter','esc','esc'])
                        self.mysleep(pauseTime/50)
                        self.mytypewrite(['enter','esc','esc'])
                        self.mysleep(pauseTime/50)
                        self.mytypewrite(['enter','esc','esc'])
                        pauseTime = 5
                        stableRunTime = 0
                        self.gui.pauseTime.config(state = 'normal')
                        self.gui.pauseTime.delete(0, 'end')
                        self.gui.pauseTime.insert(0, np.round(pauseTime,2))
                        self.gui.pauseTime.config(state = 'disabled')
                    elif iteration_N >= 108 :
                        # self.gui.log.see('end')
                        # self.gui.log.insert('end', )
                        self.add_to_log(f'"{self.xy_filename}" failed'+'\n')
                        self.l_status.config(image = self.fail)
                        break

            if total_frames == self.finished_frames:
                self.gui.countL1.config(text = f'all data are finished', fg = 'blue')
                # self.gui.countL1.config(text = f'all {total_frames} data are finished', fg = 'blue')
                self.l_status.config(image = self.finish)

            #prepare for the next folder
            self.add_to_log('\n') # add new line after a folder is complete
            self.terminate_flag = False
            self.isFirstRound = True
        self.initialization()


    def add_to_log(self, text):
            self.gui.log.see('end')
            self.gui.log.insert('end', text + '\n')


    def initialization(self):
        self.terminate_flag = True
        self.gui.startB.config(state = 'normal')
        # [e.config(fg = 'black') for e in self.gui.folderPath.get_e_paths()]
        self.gui.pauseTime.config(state = 'normal')
        self.gui.folderPath.widgets_normal()


    def convert(self, seconds):
        return time.strftime("%H:%M:%S", time.gmtime(seconds))


    def oneround(self, frameblock, pauseTime= 5):
        if self.getFocused == False:
            pyautogui.hotkey('winleft', '1')
            self.getFocused = True
        self.mytypewrite(['esc', 'esc'])
        self.mysleep(pauseTime/50)
        pyautogui.hotkey('ctrlleft', 'n')
        self.mysleep(pauseTime/50)
        self.mytypewrite(['n'])
        self.mysleep(pauseTime/5)
        pyautogui.hotkey('ctrlleft', 'i')
        self.mysleep(pauseTime/2)

        # print(path)

        if self.isFirstRound == True:
            self.runInf  =  f'locate file path'
            path = os.path.join(self.workPath)
            pyperclip.copy(path)
            self.mysleep(pauseTime/50)
            self.isFirstRound = False
            pyautogui.hotkey('ctrlleft', 'v')
            self.mysleep(pauseTime/5)
            self.mytypewrite(['enter'])
            self.mysleep(pauseTime/10)

        self.runInf  =  f'import 2D image files of "{self.xy_filename_base}"'

        pyperclip.copy(frameblock)
        self.mysleep(pauseTime/5)
        pyautogui.hotkey('ctrl', 'v')
        self.mysleep(pauseTime/20)
        self.mytypewrite(['enter'])
        self.mysleep(pauseTime*1.2)

        self.runInf  =  f'convert to "{self.xy_filename_base}"'
        self.mytypewrite(['pagedown', 'pagedown'])
        self.mysleep(pauseTime/20)


        for  ft,pos in self.gui.get_selected_filetype().items():
            pyautogui.hotkey('shiftleft', 'f10')
            self.mysleep(pauseTime/10)

            self.mytypewrite(['up', 'up', 'up', 'right', 'down', 'down', 'enter'])
            self.mysleep(pauseTime/1.5)



            self.runInf  =  f'save 1D diffraction pattern ({ft})'
            self.mytypewrite(['tab'])
            self.mysleep(pauseTime/7)
            self.mytypewrite(['down'])
            self.mysleep(pauseTime/4)
            self.mytypewrite(['r']) #make sure '.raw' is selected
            self.mysleep(pauseTime/4)


            self.press_down(totalnum = pos, pauseTime = pauseTime) #press 'down' key

            self.mytypewrite(['enter'])
            self.mysleep(pauseTime/10)
            self.mytypewrite([ 'enter'])
            self.mysleep(pauseTime/5
                )


            self.mytypewrite(['left', 'enter'])# in case need to overrite
            self.mysleep(pauseTime/5
                )


    def press_down(self, totalnum, pauseTime):
        for i in range(totalnum):
            self.mytypewrite([ 'down'])
            self.mysleep(pauseTime/30)








def main():


    root = Tk()
    root.title('convert 2D XRD to 1D pattern')
    app = Automation(root)
    app.pack()

    root.mainloop()





if __name__ == '__main__':

    main()






