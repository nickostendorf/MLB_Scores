from tkinter import *
import tkinter as tk
import MLB_Scores as fh
import MLB_Starters as st


root = Tk()
root.title("MLB - Scoring")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 50, padx = 50)

# Create a Tkinter variable
variable1 = StringVar(root)
variable2 = StringVar(root)
avgT = ""
avgHA = ""


# Dictionary with options
choices = { 'Colorado','Philadelphia','Atlanta','San Diego','Houston','NY Yankees','Chi Cubs','Detroit','LA Dodgers','Baltimore','LA Angels','Minnesota','Tampa Bay','Oakland','SF Giants','Kansas City','Chi Sox','Cincinnati','Boston','Miami','Arizona','Seattle','Milwaukee','Pittsburgh','NY Mets','Washington','St. Louis','Texas','Cleveland','Toronto'}
choicesAlpha = sorted(choices)
variable1.set('Team 1') # default value
variable2.set('Team 2') # default value 

AwayMenu = OptionMenu(mainframe, variable1, *choicesAlpha)
Label(mainframe, text="Choose Away team").grid(row = 1, column = 1)
AwayMenu.grid(row = 2, column =1)

HomeMenu = OptionMenu(mainframe, variable2, *choicesAlpha)
Label(mainframe, text="Choose Home team").grid(row = 3, column = 1)
HomeMenu.grid(row = 4, column =1)

Label(mainframe, text="2020 Avg:").grid(row = 3, column = 3)
total = Label(mainframe, text="")
total.grid(row = 4, column = 3)

Label(mainframe, text="H/A Avg:").grid(row = 3, column = 4)
HAtotal = Label(mainframe, text="")
HAtotal.grid(row = 4, column = 4)

Label(mainframe, text="Home Pitcher:").grid(row = 3, column = 5)
pitcher = Label(mainframe, text="")
pitcher.grid(row = 4, column = 5)

Label(mainframe, text="Away Pitcher:").grid(row = 3, column = 6)
pitcher2 = Label(mainframe, text="")
pitcher2.grid(row = 4, column = 6)

# on change dropdown value
def change_dropdown1(*args):
    print( variable1.get() )
def change_dropdown2(*args):
    print( variable2.get() )

# link function to change dropdown
variable1.trace('w', change_dropdown1)
variable2.trace('w', change_dropdown2)

#runs when button is pressed, returns scores
def ok(): 
	AwayTeam = variable1.get()
	HomeTeam = variable2.get()
	avgT = fh.get2019(AwayTeam, HomeTeam)
	avgHA = fh.getHA(AwayTeam, HomeTeam)
	pitcherFind = st.changeTeams(AwayTeam)
	pitcherFind2 = st.changeTeams(HomeTeam)
	total.config(text=avgT)
	HAtotal.config(text=avgHA)
	pitcher.config(text=pitcherFind)
	pitcher2.config(text=pitcherFind2)


button = Button(mainframe, text="Let's See", command=ok)
button.grid(row = 3, column = 2)	

root.mainloop()