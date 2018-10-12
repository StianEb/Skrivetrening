##
# PROSEDYRER - Disse returnerer ingen verdier. De fleste tar root som argument,
# og tryller fram instansvariabler fra root omtrent som globalverdier.
#
# Jeg føler at det hadde vært mer ideelt om jeg hadde gjort mindre av dette,
# men tror ikke det hadde vært bedre å feks sende rundt en ordbok overalt eller ha 10+ argumenter,
# så jeg er ikke sikker på hvordan jeg kan forbedre det.
#
# Jeg har seksjonert prosedyrene i tre, ettersom hvilket rom de er assosiert med,
# og forsøkt å forklare underveis hva prosedyrene gjør + lage intuitive navn.
#

import tkinter as tk
from time import time
from colour import Color

import funksjoner
import konstanter
import assistent


                        ##############################
########################### "Main menu" procedures #########################
                        ##############################

def createMainMenu(root):
    '''Called once at the start of the program. Creates the main menu frame, instantiates widgets etc'''

    bg="#ccddff"
    menuFrame = tk.Frame(root, bg=bg)

    #Create the buttons on the main menu
    root.mtaButton = tk.Button(menuFrame,
                               text='Analysis chamber',
                               command=lambda: gotoAnalysisChamber(root))
    root.mtaButton.grid(row=0, column=0, padx=50, pady=30, sticky='n')
    root.exerciseButton = tk.Button(menuFrame,
                                    text='Start exercise!',
                                    command=lambda: engageTypingFrame(root))
    root.exerciseButton.grid(row=1, column=1, sticky='s')

    #Create the glamorous assistant!
    root.assistant = assistent.Assistant(menuFrame,
                                         width=720,
                                         height=600,
                                         highlightthickness=0,
                                         bg=bg)
    root.assistant.grid(row=0, column=2, rowspan=3)

    #Initialize the scrollbar to navigate the listbox of texts (see next paragraph)
    scrollFrame = tk.Frame(menuFrame)
    scrollFrame.grid(row=2, column=1, sticky='n', pady=10)
    root.textBar = tk.Scrollbar(scrollFrame)
    root.textBar.pack(side="right", fill="y")

    #Initialize the listbox of texts to choose from
    root.textListbox = tk.Listbox(scrollFrame, yscrollcommand=root.textBar.set)
    for text in konstanter.tekster:
        root.textListbox.insert("end", text)
    root.textListbox.pack(side="left", fill="both")

    #Configure the scrollbar to cooperate with the listbox
    root.textBar.config(command=root.textListbox.yview)

    #Place the frame
    root.menuFrame = menuFrame
    root.menuFrame.grid(row=0, column=0, sticky="nsew")

def gotoAnalysisChamber(root):

    root.analysisFrame.tkraise()
    root.atmButton.focus_set()
    
    hideCustomTraining(root)
    root.analysisFrame.canv.delete("all")
    root.analysisMessageLabel.config(text='')

def gotoMenu(root):
    
    root.menuFrame.tkraise()
    root.exerciseButton.focus_set()
    root.assistant.clearThroat()


                        ################################
########################### "Typing room" procedures #########################
                        ################################

def createTypingRoom(parent):
    '''Called once at the start of the program. Initializes the typing frame
    and all constant content in it.'''

    #Create frame structure
    bg = "#ffe6b3"
    typingFrame = tk.Frame(parent, bg=bg)
    paddingGroup = tk.Frame(typingFrame, bg=bg)
    topGroup = tk.Frame(typingFrame, bg=bg)
    bottomGroup = tk.Frame(typingFrame, bg=bg)

    #Create canvas and contents
    canv = tk.Canvas(typingFrame, bg=bg, highlightthickness=0, width=20, height=20)
    canv.place(x=601,y=286)
    canv.create_polygon(8,0,0,16,16,16,fill='black')

    #Create variables to be used with the labels
    typingFrame.newTextGlobal = "This text should never display. RIP"
    typingFrame.doneTextGlobal = "This text should also never display. RIP indeed."
    typingFrame.doneTextVar = tk.StringVar()
    typingFrame.newTextVar = tk.StringVar()
    typingFrame.numberOfErrors = tk.IntVar()
    typingFrame.numberOfInputs = tk.IntVar()
    typingFrame.errorMessage = tk.StringVar()
    typingFrame.timeMessage = tk.StringVar()

    #Create labels
    typingFrame.doneText = tk.Label(topGroup, 
                     textvariable = typingFrame.doneTextVar,
                     fg = "green",
                     font = "fixedsys 16",
                                    bg=bg)
    typingFrame.newText = tk.Label(topGroup, 
                     textvariable=typingFrame.newTextVar,
                     fg = "red",
                     font = "fixedsys 16",
                                   bg=bg)
    typingFrame.errorCounter = tk.Label(bottomGroup,
                            textvariable=typingFrame.errorMessage,
                            fg = "black",
                            font = "Helvetica 16 bold italic",
                                        bg=bg)
    typingFrame.speedCounter = tk.Label(bottomGroup,
                                        textvariable=typingFrame.timeMessage,
                                        fg = "black",
                                        font = "Helvetica 16 bold italic",
                                        bg=bg)
    ghostLabel = tk.Label(paddingGroup,
                          bg=bg)

    #Place frames on screen
    paddingGroup.pack(side="top")
    paddingGroup.rowconfigure(0, minsize=200)
    topGroup.pack(side="top")
    topGroup.columnconfigure(0, minsize=400)
    topGroup.columnconfigure(1, minsize=400)
    topGroup.rowconfigure(0, minsize=150)
    bottomGroup.pack(side="top")

    #Place labels
    ghostLabel.grid(column=0, row=0)
    typingFrame.doneText.grid(column=0, row=0, sticky="e")
    typingFrame.newText.grid(column=1, row=0, sticky="w")
    typingFrame.errorCounter.grid(column=0, row=1, sticky="w")
    typingFrame.speedCounter.grid(column=0, row=2, sticky="w")

    #Arbitrarily bind the onKeyPress event to the doneText widget, make sure it's in focus
    typingFrame.doneText.bind("<Key>", lambda event: onKeyPress(event, typingFrame))

    parent.typingFrame = typingFrame
    parent.typingFrame.grid(row=0, column=0, sticky="nsew")

def engageTypingFrame(root, customText=False):
    '''Sets all variables needed to prepare a new typing session with the chosen text'''

    typingFrame = root.typingFrame

    #.curselection returns (n,) if item n on the list is selected, () otherwise.
    selectedIndex = root.textListbox.curselection()
    if len(selectedIndex) > 0 or customText:

        # Use the custom text if provided, otherwise check what's selected in the listbox.
        if customText:
            chosenText = customText
            chosenTitle = "Custom text"
        else:
            chosenTitle = root.textListbox.get(selectedIndex[0])
            chosenText = konstanter.tekster[chosenTitle]
        
        #(Re)set all variables to the starting point
        typingFrame.newTextGlobal = chosenText
        typingFrame.doneTextGlobal = ""
        typingFrame.doneTextVar.set("")
        typingFrame.newTextVar.set(typingFrame.newTextGlobal[:40])
        typingFrame.numberOfErrors.set(0)
        typingFrame.numberOfInputs.set(0)
        typingFrame.errorMessage.set("Errors: 0 (0%)")
        typingFrame.timeMessage.set("Words per minute: (start typing)")

        # Prepare a list to store this session's typing data
        root.keylog.append([])
        root.keylog[-1].append([chosenTitle, 0.0, False])

        # Display the typing session frame, and give it focus so that it can react to keyboard input.
        typingFrame.tkraise()
        typingFrame.doneText.focus_set()

def onKeyPress(event, typingFrame):
    '''Takes care of everything that should happen when the user presses a key in a typing session.'''

    root = typingFrame.master
    
    #Check the current time once, so we don't have to reuse the time() function
    current_time = time()
    
    #If the user hasn't correctly entered the first character yet, start the timer
    if typingFrame.doneTextGlobal == "":
        typingFrame.t0 = current_time
        typingFrame.t_previouskey = False #There's no time stamp for 'previous key' yet.

    #Increment valid input counter
    if event.keysym not in ('Shift_L','Shift_R'):
        numInp = typingFrame.numberOfInputs.get() + 1
        typingFrame.numberOfInputs.set(numInp)
    
    #If user hit the correct key, update the left and right text.
    #Only 40 characters are displayed on either side.
    if typingFrame.newTextGlobal[0] == event.char:

        #Update the keylog
        if typingFrame.t_previouskey:
            root.keylog[-1].append([event.char,
                                    current_time - typingFrame.t_previouskey,
                                    True])
        typingFrame.t_previouskey = current_time

        #Update the text variables
        typingFrame.doneTextGlobal += typingFrame.newTextGlobal[0]
        typingFrame.newTextGlobal = typingFrame.newTextGlobal[1:]
        if len(typingFrame.doneTextGlobal) < 41:
            typingFrame.doneTextVar.set(typingFrame.doneTextGlobal)
        else:
            typingFrame.doneTextVar.set(typingFrame.doneTextGlobal[-40:])
        if len(typingFrame.newTextGlobal) < 41:
            typingFrame.newTextVar.set(typingFrame.newTextGlobal)
        else:
            typingFrame.newTextVar.set(typingFrame.newTextGlobal[:40])
            
        #If that was the last letter, record the results and return to main menu
        if len(typingFrame.newTextGlobal) == 0:

            #Record the session WPM in the title entry
            minutesSpent = (current_time-typingFrame.t0) / 60
            wordsTyped = len(typingFrame.doneTextGlobal)/5
            root.keylog[-1][0][1] = wordsTyped/minutesSpent

            #Give some feedback in the terminal
            print("Practice session complete! Here are your stats..")
            print(typingFrame.timeMessage.get())
            print(typingFrame.errorMessage.get())

            #Bring the user back to the main menu
            gotoMenu(root)

            #Save the log
            save(root.keylog)
            
    #If user hit the wrong key, increment the error counter, unless it was Shift
    elif event.keysym not in ('Shift_L','Shift_R'):
        print("Wrong input: {}".format(event.char))
        typingFrame.numberOfErrors.set(typingFrame.numberOfErrors.get() + 1)

        #..and also update the keylog
        if typingFrame.t_previouskey:
            typingFrame.master.keylog[-1].append([event.keysym,
                                    round(current_time - typingFrame.t_previouskey, 3),
                                    False])
            typingFrame.t_previouskey = current_time

    #Calculate the error message
    if typingFrame.numberOfInputs.get() > 0:
        errorPercentage = (typingFrame.numberOfErrors.get()/typingFrame.numberOfInputs.get())*100
        typingFrame.errorMessage.set("Errors: {} ({:.2f}%)".format(typingFrame.numberOfErrors.get(), errorPercentage))
        
    #Calculate the speed message. 5 characters is considered an average word.
    if len(typingFrame.doneTextGlobal) > 6:
        minutesSpent = (current_time-typingFrame.t0) / 60
        wordsTyped = len(typingFrame.doneTextGlobal)/5
        typingFrame.timeMessage.set("Words per minute: {:.2f}".format(wordsTyped/minutesSpent))

def save(log):
    '''What do you think?'''
    
    #Write each session to a separate line in the save file
    with open("saved_logs", "w") as file:
        for index, session in enumerate(log):
            file.write(str(session))
            if index+1 < len(log):
                file.write("\n")

                        #####################################
########################### "Analysis chamber" procedures #########################
                        #####################################

def createAnalysisChamber(root):
    '''Called once at the start of the program. Creates the analysis chamber frame and instantiates widgets.'''

    #Create the frame
    bg = "#c4c4ed"
    analysisFrame = tk.Frame(root, bg=bg)
    analysisFrame.rowconfigure(1, minsize=100)
    root.analysisMessage = tk.StringVar()

    #Create all the widgets
    analysisFrame.canv = tk.Canvas(analysisFrame, width=941, height=391, bg=bg, highlightthickness=0)
    analysisFrame.canv.grid(row=1, column=1, rowspan=5, padx=30, pady=20, sticky='e')
    root.atmButton = tk.Button(analysisFrame,
                               text="Back to menu",
                               command=lambda: gotoMenu(root))
    root.atmButton.grid(row=0, column=0, pady=20)
    root.keyboardAnalysisButton = tk.Button(analysisFrame,
                                            text="Analyze your performance",
                                            command=lambda: runKeyboardAnalysis(root))
    root.keyboardAnalysisButton.grid(row=1, column=0, sticky='s', padx=30)
    root.listInfoLabel = tk.Label(analysisFrame,
                                  text="Filter analysis by texts:",
                                  font=("Purisa",12),
                                  bg=bg)
    root.listInfoLabel.grid(row=3, column=0, sticky="s")
    root.customTrainingButton = tk.Button(analysisFrame,
                                          text="Generate custom training session",
                                          command=lambda: initializeCustomTraining(root))
    root.customTrainingSlider = tk.Scale(analysisFrame,
                                         label="Number of words",
                                         orient="horizontal",
                                         from_=3,
                                         to=100,
                                         highlightthickness=0,
                                         bg=bg)

    root.analysisMessageLabel = tk.Label(analysisFrame,
                                         textvariable = root.analysisMessage,
                                         bg='white',
                                         relief='solid',
                                         borderwidth=1,
                                         font=('Purisa', 14))
    root.analysisMessageLabel.place(x=300, y=50)

    temp = tk.IntVar()
    root.shiftCheckbutton = tk.Checkbutton(analysisFrame,
                                           text="Shift keyboard",
                                           variable=temp,
                                           bg=bg,
                                           command=lambda: hideCustomTraining(root))
    root.shiftCheckbutton.checked = temp
    root.shiftCheckbutton.grid(row=2, column=0)

    #Create the listbox of texts to enable user filtering (see createMainMenu for breakdown)
    root.selectionFrame = tk.Frame(analysisFrame)
    root.selectionFrame.grid(row=4, column=0, sticky="n")
    selectionBar = tk.Scrollbar(root.selectionFrame)
    selectionBar.pack(side="right", fill="y")
    
    root.selectionBox = tk.Listbox(root.selectionFrame, yscrollcommand=selectionBar.set, selectmode="multiple")
    for text in konstanter.tekster:
        root.selectionBox.insert("end", text)
    root.selectionBox.insert("end", "Custom text")
    root.selectionBox.select_set(0,'end')
    root.selectionBox.bind('<<ListboxSelect>>', lambda event: hideCustomTraining(root))
    
    root.selectionBox.pack(side="left", fill="both")
    selectionBar.config(command=root.selectionBox.yview)

    #Create buttons to select 'all' and 'none' in the listbox
    boxButtonFrame = tk.Frame(analysisFrame)
    boxButtonFrame.grid(row=5, column=0, sticky="n")
    noneButton = tk.Button(boxButtonFrame,
                           text="All",
                           command=lambda: noneButtonEvent(root))
    allButton = tk.Button(boxButtonFrame,
                          text="None",
                          command=lambda: allButtonEvent(root))
    noneButton.pack(side='left')
    allButton.pack(side='left')

    #Tie the frame to the container frame
    root.analysisFrame = analysisFrame
    root.analysisFrame.grid(row=0, column=0, sticky="nsew")

def allButtonEvent(root):
    root.selectionBox.selection_clear(0,'end')
    hideCustomTraining(root)

def noneButtonEvent(root):
    root.selectionBox.select_set(0, 'end')
    hideCustomTraining(root)
    
def runKeyboardAnalysis(root):
    '''This is what happens when you press the keyboard analysis button in the Analysis Chamber'''

    #This is going to be the message displayed to the user
    message = ""

    selectedIndexes = root.selectionBox.curselection()
    selectedTitles = []
    for index in selectedIndexes:
        selectedTitles.append(root.selectionBox.get(index))

    sessionFilteredLog = funksjoner.numberOfSessions(root.keylog, titles=selectedTitles, returnFilteredLog=True)
    filteredLog = funksjoner.filterPostShift(sessionFilteredLog)

    #If there's no data to analyze, just inform the user
    if len(root.keylog) == 0:
        message = "There's nothing to analyze yet. Go back and do some typing exercises!"

    elif len(filteredLog) == 0:
        message = "There's no training data on the selected texts."

    #If the user has checked the Shift - checkbox, signalling they want to analyze their Shift-character usage:
    elif root.shiftCheckbutton.checked.get():

        #Filter the Shift characters out of the keylog, calculate their averages
        trimmedKeylog = funksjoner.trimKeylog(konstanter.bigKeyValues, filteredLog)
        avgDelays = funksjoner.calculateAverageDelays(trimmedKeylog)

        #If there's enough training data for Shift characters:
        if len(avgDelays) > 5:
            drawKeyboard(root, "big", avgDelays)
            message = "Displaying your average delays for big (Shift) keyboard layout for the selected texts."
            root.customTrainingButton.grid(row=6, column=1)
            root.customTrainingSlider.grid(row=7, column=1, pady=6, sticky="n")
        else:
            message = "Not enough training data on Shift-enabled (capitalized) characters for the selected texts."

    #If the user has not checked the Shift - checkbox.. (see above)
    else:
        trimmedKeylog = funksjoner.trimKeylog(konstanter.smallKeyValues, filteredLog)
        avgDelays = funksjoner.calculateAverageDelays(trimmedKeylog)
        
        if len(avgDelays) > 5:
            drawKeyboard(root, "small", avgDelays)
            message = "Displaying your average delays for small (non-Shift) keyboard layout for the selected texts."
            root.customTrainingButton.grid(row=6, column=1)
            root.customTrainingSlider.grid(row=7, column=1, pady=6, sticky="n")
        else:
            message = "Not enough training data on non-Shift (small) characters for the selected texts."

    #Display the message
    root.analysisMessage.set(message)

def drawKeyboard(root, mode, avgDelays):
    '''Draws the colored keyboard in the Analysis Chamber'''

    #Clear the canvas, draw the background for the keyboard
    canv = root.analysisFrame.canv
    canv.delete("all")
    canv.create_rectangle(0,0,940,390, fill="gray", outline='black')

    #Set certain values depending on whether we're drawing the Shift version or not
    if mode == "big":
        keyPositions = konstanter.bigKeyPositions    
        keyValues = konstanter.bigKeyValues
        xOffset = 14
        yOffset = 0
    else:
        keyPositions = konstanter.smallKeyPositions
        keyValues = konstanter.smallKeyValues
        xOffset = -30
        yOffset = -20

    #Distribute the calculated delays between 0.0 and 1.0.
    #avgDelays already contains only the characters we want in this mode.
    root.distributedAverageDelays = funksjoner.calculateDistributedAverages(avgDelays)
    dAD = root.distributedAverageDelays

    #Use the colour module to create a list of colors in a smooth transition from green to red
    canv = root.analysisFrame.canv
    green = Color("green")
    greenToRed = list(green.range_to(Color("red"),101))

    #For each key to be displayed:
    for i, (x, y) in enumerate(keyPositions):
        
        #if we have the average speed data for that key, determine the color for that key
        #and display the speed data underneath
        if keyValues[i] in avgDelays:
            delay = str( int( avgDelays[keyValues[i]][0] * 1000 ) ) + " ms"
            canv.create_text(x-45+xOffset, y+110+yOffset, text=delay, fill='white', font=("Purisa", 10))
            keyFill = greenToRed[ int( dAD[ keyValues[i] ]*100 ) ]
        else:
            keyFill = "lightgrey"
            
        #draw a rectangle with the appropriate character on it, representing the key
        canv.create_rectangle(x-70+xOffset, y+50+yOffset, x-20+xOffset, y+100+yOffset, fill=keyFill)
        canv.create_text(x-48+xOffset, y+72+yOffset, text=keyValues[i], font=("Purisa", 28), fill="black")

def initializeCustomTraining(root):

    #Generate the custom text
    numberOfWords = root.customTrainingSlider.get()
    mode = "big" if root.shiftCheckbutton.checked.get() else "small"
    generatedText = funksjoner.generateTrainingText(root.distributedAverageDelays, numberOfWords, mode=mode)

    #Goto the typing room
    engageTypingFrame(root, customText=generatedText)

def hideCustomTraining(root):
    
    root.customTrainingButton.grid_remove()
    root.customTrainingSlider.grid_remove()
    root.analysisFrame.canv.delete('all')
    root.analysisMessage.set("Customize your analysis on the left.")


