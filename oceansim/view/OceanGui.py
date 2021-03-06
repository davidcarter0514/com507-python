from tkinter import *
from tkinter import messagebox
import time
from simulation.Config import Config
from oceansim.model.Ocean import Ocean
from oceansim.model.Shark import Shark
from oceansim.model.Plankton import Plankton
from simulation.model.Location import Location

class OceanGui(Tk):

    # initialise window
    def __init__(self,ocean:Ocean):
        super().__init__()
        self.interaction_state = None 
        self.observers = []
        
        # load resources
        
        # set window attributes
        self.title("Simulator")
        self.configure(height=1000,width=1000)

        # add components
        # add a for loop based on Ocean Simulation
        self.__add_environment_frame()
        self.__add_grid_label(ocean)
        self.__add_button_frame()
        self.__add_start_button()
        self.__add_stop_button()
        self.__add_step_button()
        self.__add_reset_button()
        print("finished gui constructor")

    def __add_environment_frame(self):
        self.environment_frame = Frame()
        self.environment_frame.grid(row = 0, column=0)

    def __add_grid_label(self,ocean):
        self.label_grid = []
        oceanWidth = ocean.getWidth()
        oceanHeight = ocean.getHeight()
        for a in range(0,oceanHeight,1):
            self.label_grid.append([None]*oceanWidth)

        # populate label grid with labels and format if none empty
        for i in range (0,oceanWidth,1):
            for j in range(0,oceanHeight,1):

                self.label_grid[i][j] = Label(self.environment_frame)
                self.label_grid[i][j].grid(row=i,column=j,sticky=W+E)
                self.label_grid[i][j].config(
                        bg='#fff',
                        width=5,
                        height=2,
                        bd=1,
                        relief='ridge'
                        )
                #check if not empty
                if isinstance(ocean.getAgent(Location(i,j)),Shark) :
                    self.label_grid[i][j].config(bg='#faa',text='shark')
                elif isinstance(ocean.getAgent(Location(i,j)),Plankton) :
                    self.label_grid[i][j].config(bg='#afa',text='plant')
                
    def __add_button_frame(self):
        self.button_frame = Frame()
        self.button_frame.grid(
                row = 1,
                column = 0
                )
        self.button_frame.config(height = 200,padx=10, pady=10)
    
    def __add_start_button(self):
        #create
        self.start_button = Button(self.button_frame)
        self.start_button.grid(row=0,column=0)

        #style
        self.start_button.configure(
            width=10,
            bg="#fed",
            text="START"
            )

        #events
        self.start_button.bind("<ButtonRelease-1>", self.__start_button_clicked)  

    def __start_button_clicked(self,event):
        self.interaction_state = "START"
        self.notify_observer()

    def __add_stop_button(self):
        #create
        self.stop_button = Button(self.button_frame)
        self.stop_button.grid(row=0,column=2)

        #style
        self.stop_button.configure(
            width=10,
            bg="#fed",
            text="STOP"
            )

        #events
        self.stop_button.bind("<ButtonRelease-1>", self.__stop_button_clicked) 
        
    def __stop_button_clicked(self,event):
        self.interaction_state = "STOP"
        self.notify_observer()

    def __add_step_button(self):
        #create
        self.step_button = Button(self.button_frame)
        self.step_button.grid(row=0,column=1)

        #style
        self.step_button.configure(
            width=10,
            bg="#fed",
            text="STEP"
            )

        #events
        self.step_button.bind("<ButtonRelease-1>", self.__step_button_clicked) 
        
    def __step_button_clicked(self,event):
        self.interaction_state = "STEP"
        self.notify_observer()

    def __add_reset_button(self):
        #create
        self.reset_button = Button(self.button_frame)
        self.reset_button.grid(row=0,column=3)

        #style
        self.reset_button.configure(
            width=10,
            bg="#fed",
            text="RESET"
            )

    def refresh(self,ocean):
        # populate label grid with labels and format if none empty
        oceanWidth = ocean.getWidth()
        oceanHeight = ocean.getHeight()

        for i in range (0,oceanWidth,1):
            for j in range(0,oceanHeight,1):

                self.label_grid[i][j] = Label(self.environment_frame)
                self.label_grid[i][j].grid(row=i,column=j,sticky=W+E)
                self.label_grid[i][j].config(
                        bg='#fff',
                        width=5,
                        height=2,
                        bd=1,
                        relief='ridge'
                        )
                #check if not empty and format
                if isinstance(ocean.getAgent(Location(i,j)),Shark) :
                    self.label_grid[i][j].config(bg='#faa',text='shark')
                elif isinstance(ocean.getAgent(Location(i,j)),Plankton) :
                    self.label_grid[i][j].config(bg='#afa',text='plant')
                else:
                    self.label_grid[i][j].config(bg='#fff',text='')
    
    def add_observer(self,observer):
        self.observers.append(observer)

    def remove_observer(self,observer):
        pass

    def notify_observer(self):
        for observer in self.observers:
            observer.process(self.interaction_state)