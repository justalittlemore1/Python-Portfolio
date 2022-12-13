import tkinter as tk
from PIL import Image, ImageTk
from matplotlib import pyplot
from matplotlib import animation
from matplotlib import lines
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
pyplot.style.use('Solarize_Light2')

entrykey = {
    'Low (1.5 People)':0.15, 
    'Medium (2.5 People)':0.25, 
    'High (3.5 People)':0.35, 
    'Long (23 Days)':0.04, 
    'Mild (18 Days)':0.06, 
    'Short (14 Days)':0.08,
    'Available/Encouraged (Overall 40% Protection)':0.5, 
    'None (0% Protection)':1,
    'Mandated (70% Efficacy)':0.3, 
    'Recommended (30% Efficacy)':0.7, 
    'None (0% Efficacy)':1,
    'Required (40% Protection)':0.6, 
    'Encouraged (20% Protection)':0.8
}

class MainFunction():
    def __init__(self):
        self.S = None
        self.I = None
        self.R = 0
        self.r = None
        self.a = None
        self.v = 1
        self.h = 1
        self.m = 1
        self.dt = 1
        self.current = 0
        self.wanted = None
        self.ilist = []
        self.rlist = []
        self.currentlist = []
        self.fig = None
        self.ax = None
        self.anim = None
        self.canvas = None
        self.counter = 0
        self.always = True

    def setup(self):
        # Create window.
        global window 
        window = tk.Tk()
        window.title('Epidemic Simulation')

        # Create a frame.
        global mainframe
        mainframe = tk.Frame(master=window, width=1500, height=1000)
        mainframe.pack()

        # Initiate.
        self.welcomepage()

    def welcomepage(self):
        # Create main heading.
        global welcometitle
        welcometitle = tk.Label(master=mainframe, text='Simulation of an Epidemic (in Python).', font=('Times New Roman', 95))
        welcometitle.place(x=0, y=350)

        # Create button and binding.
        global letusbegin
        letusbegin = tk.Button(master=mainframe, text='Let\'s Begin!', font=('Times New Roman Italic', 75), width=10, height=1)
        letusbegin.place(x=525, y=550)
        def letusbegin_was_clicked(event):
            self.sirmodeldescription() 
        letusbegin.bind('<Button-1>', letusbegin_was_clicked)

        # Add virus images.
        global openedvirusimage
        openingvirusimage = Image.open('./virus.png')
        openedvirusimage = ImageTk.PhotoImage(openingvirusimage)
        global virusimage1
        virusimage1 = tk.Label(master=mainframe, image=openedvirusimage)
        virusimage1.image = openedvirusimage
        virusimage1.place(x=90, y=600)
        virusimage1.lower()
        global virusimage2
        virusimage2 = tk.Label(master=mainframe, image=openedvirusimage)
        virusimage2.image = openedvirusimage
        virusimage2.place(x=300, y=40)
        virusimage2.lower()
        global virusimage3
        virusimage3 = tk.Label(master=mainframe, image=openedvirusimage)
        virusimage3.image = openedvirusimage
        virusimage3.place(x=900, y=500)
        virusimage3.lower()

        window.attributes("-fullscreen", True)
        window.resizable(False, False)

    def sirmodeldescription(self):
        # Destroy previous.
        for widget in mainframe.winfo_children():
            widget.destroy()

        # Create main heading.
        global title1
        title1 = tk.Label(master=mainframe, text='This simulation uses the "SIR Model,"', font=('Times New Roman', 75))
        title1.place(x=150, y=25)
        global title2
        title2 = tk.Label(master=mainframe, text='which separates the population into...', font=('Times New Roman', 75))
        title2.place(x=150, y=115)

        # Information about the SIR model.
        global infosusceptible
        infosusceptible = tk.Label(master=mainframe, text='Susceptible:', font=('Times New Roman', 50), fg='green')
        infosusceptible.place(x=150, y=250)
        global textsusceptible
        textsusceptible = tk.Label(master=mainframe, text='The population that can be infected;', font=('Times New Roman Italic', 50))
        textsusceptible.place(x=150, y=340)

        global infoinfected
        infoinfected = tk.Label(master=mainframe, text='Infected:', font=('Times New Roman', 50), fg='red')
        infoinfected.place(x=150, y=450)
        global textinfected
        textinfected = tk.Label(master=mainframe, text='The currently infected population; and', font=('Times New Roman Italic', 50))
        textinfected.place(x=150, y=540) 

        global inforemoved
        inforemoved = tk.Label(master=mainframe, text='Removed:', font=('Times New Roman', 50), fg='blue')
        inforemoved.place(x=150, y=650)
        global textremoved
        textremoved = tk.Label(master=mainframe, text='The recovered or passed away population.', font=('Times New Roman Italic', 50))
        textremoved.place(x=150, y=740)

        # Create begin and setup binding.
        global proceedtosim
        proceedtosim = tk.Button(master=mainframe, text='Proceed to Simulation', font=('Times New Roman Italic', 75), width=18, height=1)
        proceedtosim.place(x=150, y=900)
        def proceed_was_clicked(event):
            self.customize() 
        proceedtosim.bind('<Button-1>', proceed_was_clicked)

        # Add images.
        global virusimage4
        virusimage4 = tk.Label(master=mainframe, image=openedvirusimage)
        virusimage4.image = openedvirusimage
        virusimage4.place(x=1000, y=500)
        virusimage4.lower()

    def customize(self):
        # Remove previous.
        for widget in mainframe.winfo_children():
            widget.destroy()

        # Create a heading for customization.
        customize1 = tk.Label(master=mainframe, text='Customize the simulation\'s parameters,', font=('Times New Roman', 75))
        customize1.place(x=150, y=25)
        customize2 = tk.Label(master=mainframe, text='and click "Run Simulation" when ready!', font=('Times New Roman', 75))
        customize2.place(x=150, y=115)

        # Initial infected population.
        initialinfectedchoices = [1, 10, 100]
        variable1 = tk.StringVar(window)
        variable1.set('Choose')
        initialinfectedentry = tk.OptionMenu(window, variable1, *initialinfectedchoices)
        initialinfectedentry.place(x=1075, y=307.5)
        initialinfectedtext = tk.Label(master=mainframe, text='Choose the number of people who start out infected out of a population of 10,000:', font=('Times New Roman', 25))
        initialinfectedtext.place(x=150, y=300)

        # Rate of infection.
        virusinfectionchoices = ['Low (1.5 People)', 'Medium (2.5 People)', 'High (3.5 People)']
        variable2 = tk.StringVar(window)
        variable2.set('Choose')
        virusinfectionentry = tk.OptionMenu(window, variable2, *virusinfectionchoices)
        virusinfectionentry.place(x=1055, y=357.5)
        virusinfectiontext = tk.Label(master=mainframe, text='Per every person with the virus, how many people will they infect (on average)?', font=('Times New Roman', 25))
        virusinfectiontext.place(x=150, y=350)

        # Rate of removed.
        removedchoices = ['Long (23 Days)', 'Mild (18 Days)', 'Short (14 Days)']
        variable3 = tk.StringVar(window)
        variable3.set('Choose')
        removedentry = tk.OptionMenu(window, variable3, *removedchoices)
        removedentry.place(x=900, y=407.5)
        removedtext = tk.Label(master=mainframe, text='On average, how long are people contagious towards others for?', font=('Times New Roman', 25))
        removedtext.place(x=150, y=400)

        # Public health measures.
        publichealthnotice = tk.Label(master=mainframe, text='Public Health Measures:', font=('Times New Roman Italic', 40))
        publichealthnotice.place(x=150, y=525)

        # How many days?
        setdayvariables = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        midmod = tk.StringVar(window)
        midmod.set('Choose')
        dayentry = tk.OptionMenu(window, midmod, *setdayvariables)
        dayentry.place(x=765, y=602.5)
        daytext = tk.Label(master=mainframe, text='The public health measures will be applied on day:', font=('Times New Roman', 25))
        daytext.place(x=150, y=595)

        # Vaccines?
        vaccinechoices = ['Available/Encouraged (Overall 40% Protection)', 'None (0% Protection)']
        mod1 = tk.StringVar(window)
        mod1.set('Choose')
        vaccineentry = tk.OptionMenu(window, mod1, *vaccinechoices)
        vaccineentry.place(x=635, y=652.5)
        vaccinetext = tk.Label(master=mainframe, text='Are vaccines available for protection?', font=('Times New Roman', 25))
        vaccinetext.place(x=150, y=645)
        
        # Masks?
        healthchoices = ['Mandated (70% Efficacy)', 'Recommended (30% Efficacy)', 'None (0% Efficacy)']
        mod2 = tk.StringVar(window)
        mod2.set('Choose')
        healthmeasuresentry = tk.OptionMenu(window, mod2, *healthchoices)
        healthmeasuresentry.place(x=805, y=702.5)
        healthmeasurestext = tk.Label(master=mainframe, text='Mask wearing is mandated by public health guidelines:', font=('Times New Roman', 25))
        healthmeasurestext.place(x=150, y=695)

        # Social distancing?
        distancing = ['Required (40% Protection)', 'Encouraged (20% Protection)', 'None (0% Protection)']
        mod3 = tk.StringVar(window)
        mod3.set('Choose')
        distancingentry = tk.OptionMenu(window, mod3, *distancing)
        distancingentry.place(x=610, y=752.5)
        distancingtext = tk.Label(master=mainframe, text='Indoor social distancing is required:', font=('Times New Roman', 25))
        distancingtext.place(x=150, y=745)

        # Images.
        global virusimage5
        virusimage5 = tk.Label(master=mainframe, image=openedvirusimage)
        virusimage5.image = openedvirusimage
        virusimage5.place(x=1000, y=600)
        virusimage5.lower()
        global virusimage6
        virusimage6 = tk.Label(master=mainframe, image=openedvirusimage)
        virusimage6.image = openedvirusimage
        virusimage6.place(x=1100, y=300)
        virusimage6.lower()

        def runsim_clicked(event):
            try:
                # Setup temporary variables.
                tempi = int(variable1.get())
                tempv = str(variable2.get())
                tempr = str(variable3.get())

                # Update variables.
                self.S = 1-(tempi/10000)
                self.I = tempi/10000
                self.r = entrykey[tempv]
                self.a = entrykey[tempr]

                # Set global temporary variables.
                self.wanted = int(midmod.get())
                global tempvaccine
                tempvaccine = str(mod1.get())
                tempvaccine = entrykey[tempvaccine]
                global tempmasks
                tempmasks = str(mod2.get())
                tempmasks = entrykey[tempmasks]
                global tempdistance
                tempdistance = str(mod3.get())
                tempdistance = entrykey[tempdistance]

                # Destroy previous text.
                for widget in mainframe.winfo_children():
                    widget.destroy()
                for widget in window.winfo_children():
                    widget.destroy()

                # Call simulationpage.
                self.simulationpage()
            except:
                failednotice = tk.Label(master=mainframe, text='Please set all the parameters for the simulation!', font=('Times New Roman', 25), fg='red')
                failednotice.place(x=150, y=850)

        # Button.
        runsim = tk.Button(master=mainframe, text='Run Simulation!', font=('Times New Roman Italic', 75), width=13, height=1)
        runsim.place(x=150, y=900)
        runsim.bind('<Button-1>', runsim_clicked)

    def simulationpage(self):
        # Plotting.
        self.fig = pyplot.Figure(dpi=200)
        self.fig.patch.set_facecolor('#f0ecec')
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.ax = self.fig.add_subplot(111)
        self.anim = animation.FuncAnimation(self.fig, self.plotvalgenerate, interval=100)

    def plotvalgenerate(self, i):
        # Update current values.        
        prevS = self.S
        prevI = self.I
        prevR = self.R

        # Public Health Measures update.
        if self.always == True:
            simulationrunning = tk.Label(master=window, text='The simulation is running...', font=('Times New Roman', 75))
            simulationrunning.pack(side=tk.TOP)
            self.always = False
        elif self.R > 0.5 and self.counter == 0:
            over50infected = tk.Label(master=window, text='The population that has been infected is now over 50%!', font=('Times New Roman Italic', 50))
            over50infected.pack(side=tk.TOP)
            self.counter += 1
        elif self.current == self.wanted:
            self.v = tempvaccine
            self.h = tempdistance
            self.m = tempmasks
            publicmeasurestext = tk.Label(master=window, text='Public Health Measures have been applied!', font=('Times New Roman Italic', 50), fg='red')
            publicmeasurestext.pack(side=tk.TOP)

        # Randomize coefficients.
        user = random.randint((self.r*100)-4, (self.r*100)+4)/100
        usea = random.randint((self.a*100)-4, (self.a*100)+4)/100
        usev = random.randint((self.v*100)-4, (self.v*100)+4)/100
        useh = random.randint((self.h*100)-4, (self.h*100)+4)/100
        usem = random.randint((self.m*100)-4, (self.m*100)+4)/100

        # Update SIR model.
        self.S = prevS - (user*usev*useh*usem*prevS*prevI)*self.dt
        self.I = prevI + (user*usev*useh*usem*prevS*prevI - usea*prevI)*self.dt
        self.R = prevR + (usea*prevI)*self.dt
        UseThisR = 1-self.R
        self.current += 1

        # Add results for plotting.
        self.ilist.append(self.I)
        self.rlist.append(UseThisR)
        self.currentlist.append(self.current)

        # Plotting.
        self.ax.cla()
        pyplot.tight_layout()
        self.ax.set_title('Epidemic Simulation', family='serif')
        infectedlabel, = self.ax.plot(self.currentlist, self.ilist, label='Infected', color='red')
        removedlabel, = self.ax.plot(self.currentlist, self.rlist, label='Removed', color='blue')
        susceptiblelabel = lines.Line2D([], [], color='green', label='Susceptible')
        self.ax.legend(handles=[infectedlabel, removedlabel, susceptiblelabel])
        self.ax.set_ylabel('% of Population')
        self.ax.set_xlabel('Time Passed (Days)')
        self.ax.fill_between(self.currentlist, self.ilist, color='red', alpha=1)
        self.ax.fill_between(self.currentlist, self.rlist, 1, color='blue', alpha=1)
        self.ax.fill_between(self.currentlist, self.ilist, self.rlist, color='green', alpha=0.5)
        time.sleep(0.1)

runprogram = MainFunction()
runprogram.setup()
window.mainloop()