from tkinter import *
import time
from simulation.Config import Config
from simulation.model.Location import Location
from marssim.model.Mars import Mars
from marssim.model.Rock import Rock
from marssim.model.Rover import Rover
from marssim.model.Spaceship import Spaceship

class MarsGui(Tk):

    # initialise window
    def __init__(self, mars:Mars,step):
        super().__init__()
        self.interaction_state = None
        self.observers = []

        # set window attributes
        self.title("Simulator")
        self.configure(height=1000,width=1000)

        # add components
        self.__add_legend_frame()
        self.__add_spaceship_legend_label()
        self.__add_rover_legend_label()
        self.__add_rock_legend_label()
        self.__add_spaceship_legend_text()
        self.__add_rover_legend_text()
        self.__add_rock_legend_text()
        self.__add_environment_frame()
        self.__add_grid_label(mars)
        self.__add_button_frame()
        self.__add_start_button()
        self.__add_stop_button()
        self.__add_step_button(step)
        self.__add_reset_button()
        print("finished gui constructor")

    def __add_environment_frame(self):
        self.environment_frame = Frame()
        self.environment_frame.grid(row = 1, column = 0)

    def __add_legend_frame(self):
        self.legend_frame = Frame()
        self.legend_frame.grid(row = 0,column = 0)
        self.legend_frame.config(padx=10, pady=10)

    def __add_spaceship_legend_label(self):
        self.spaceship_label = Label(self.legend_frame)
        self.spaceship_label.grid(row = 0, column = 0)
        self.spaceship_label.config(bg='#f00',
            width=5,
            height=2,
            bd=1,
            relief='ridge')

    def __add_rover_legend_label(self):
        self.rover_label = Label(self.legend_frame)
        self.rover_label.grid(row = 0, column = 2)
        self.rover_label.config(bg='#0a0',
                        width=5,
                        height=2,
                        bd=1,
                        relief='ridge')

    def __add_rock_legend_label(self):
        self.rock_label = Label(self.legend_frame)
        self.rock_label.grid(row = 0, column = 4)
        self.rock_label.config(bg='#000',
                        width=5,
                        height=2,
                        bd=1,
                        relief='ridge')

    def __add_spaceship_legend_text(self):
        self.spaceship_text = Label(self.legend_frame)
        self.spaceship_text.grid(row = 0, column = 1, sticky ='W')
        self.spaceship_text.config(
            text='Spaceship',                        
            bg='#fff',
            padx = 5
            )

    def __add_rover_legend_text(self):
        self.spaceship_text = Label(self.legend_frame)
        self.spaceship_text.grid(row = 0, column = 3, sticky ='W')
        self.spaceship_text.config(
            text='Rover',                        
            bg='#fff',
            padx = 5
            )

    def __add_rock_legend_text(self):
        self.spaceship_text = Label(self.legend_frame)
        self.spaceship_text.grid(row = 0, column = 5, sticky ='W')
        self.spaceship_text.config(
            text='Rock',                        
            bg='#fff',
            padx = 5
            )

    def __add_grid_label(self,mars:Mars):
        self.label_grid = []
        mars_width = mars.get_width()
        mars_height = mars.get_height()
        for a in range(0,mars_height,1):
            self.label_grid.append([None]*mars_width)

        # populate label grid with labels and format if none empty
        for i in range (0,mars_width,1):
            for j in range(0,mars_height,1):

                self.label_grid[i][j] = Label(self.environment_frame)
                self.label_grid[i][j].grid(row=i,column=j,sticky=W+E)
                self.label_grid[i][j].config(
                        bg='#fff',
                        width=5,
                        height=2,
                        bd=1,
                        relief='ridge'

                        # testing - show location coordinates
                        ,text = '('+str(i)+','+str(j)+')'
                        ,fg='#ccc'
                        
                        )

                agent = mars.get_agent(Location(i,j))
                # check if not empty
                if isinstance(agent,Rock):
                    self.label_grid[i][j].config(bg='#000')
                elif isinstance(agent,Rover):
                    self.label_grid[i][j].config(bg='#0a0', text = "R" + str(agent.get_id()))
                elif isinstance(agent,Spaceship):
                    self.label_grid[i][j].config(bg='#f00')
                else:
                    self.label_grid[i][j].config(bg='#ddd')
                
    def __add_button_frame(self):
        self.button_frame = Frame()
        self.button_frame.grid(
                row = 2,
                column = 0
                )
        self.button_frame.config(padx=10, pady=10)
    
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

    def __add_step_button(self,step):
        #create
        self.step_button = Button(self.button_frame)
        self.step_button.grid(row=0,column=1)

        #style
        self.step_button.configure(
            width=10,
            bg="#fed",
            text="STEP ("+str(step)+")"
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

    def refresh(self,mars:Mars,step):
        # populate label grid with labels and format if none empty
        mars_width = mars.get_width()
        mars_height = mars.get_height()

        for i in range (0,mars_width,1):
            for j in range(0,mars_height,1):
                agent = mars.get_agent(Location(i,j))
                # check if not empty
                if isinstance(agent,Rock):
                    self.label_grid[i][j].config(bg='#000', text = '('+str(i)+','+str(j)+')')
                elif isinstance(agent,Rover):
                    self.label_grid[i][j].config(bg='#0a0', text = "R" + str(agent.get_id()))
                elif isinstance(agent,Spaceship):
                    self.label_grid[i][j].config(bg='#f00', text = '('+str(i)+','+str(j)+')')
                else:
                    self.label_grid[i][j].config(bg='#ddd', text = '('+str(i)+','+str(j)+')')

        self.step_button.configure(text = "STEP ("+str(step)+")")

    def add_observer(self,observer):
        self.observers.append(observer)

    def remove_observer(self,observer):
        pass

    def notify_observer(self):
        for observer in self.observers:
            observer.process(self.interaction_state)

    # def __add_battery_pane(self):
    #     self.legend_frame = Frame()
    #     self.legend_frame.grid(row = 3,column = 0)
    #     self.legend_frame.config(padx=10, pady=10)


    # def __add_rover_battery(self,mars:Mars):
    #     self.battery_grid = []
    #     for a in range(0,mars_height,1):
    #         self.label_grid.append([None]*mars_width)

    #     # populate label grid with labels and format if none empty
    #     for i in range (0,mars_width,1):
    #         for j in range(0,mars_height,1):

    #             self.label_grid[i][j] = Label(self.environment_frame)
    #             self.label_grid[i][j].grid(row=i,column=j,sticky=W+E)
    #             self.label_grid[i][j].config(
    #                     bg='#fff',
    #                     width=5,
    #                     height=2,
    #                     bd=1,
    #                     relief='ridge'

    #                     # testing - show location coordinates
    #                     ,text = '('+str(i)+','+str(j)+')'
    #                     ,fg='#ccc'
                        
    #                     )

    #             agent = mars.get_agent(Location(i,j))
    #             # check if not empty
    #             if isinstance(agent,Rock):
    #                 self.label_grid[i][j].config(bg='#000')
    #             elif isinstance(agent,Rover):
    #                 self.label_grid[i][j].config(bg='#0a0', text = "R" + str(agent.get_id()))
    #             elif isinstance(agent,Spaceship):
    #                 self.label_grid[i][j].config(bg='#f00')
    #             else:
    #                 self.label_grid[i][j].config(bg='#ddd')