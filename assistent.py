import tkinter as tk
from random import choice, randint

import konstanter
import funksjoner

class Assistant(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Dodge the 'seventh father in the house' effect
        self._keylog = self.master.master.keylog

        #Have a visual appearance
        x = 600
        y = 360
        self.create_line(x+30, y+60, x+30, y+79, width=3, fill='gray')
        self.create_line(x+30, y+79, x+32, y+89, width=3, fill='gray')
        self.create_arc(x+32, y+78, x+50, y+98, start=185, extent=180, style='arc', width=3, outline='gray')
        self.create_line(x+49, y+63, x+50, y+88, width=3, fill='gray')
        self.create_line(x+54, y+22, x+49, y+63, width=3, fill='gray')
        self.create_arc(x+26, y+7, x+54, y+36, start=-5, extent=175, style='arc', width=3, outline='gray')
        self.create_line(x+24, y+32, x+27, y+18, width=3, fill='gray')
        self.create_line(x+24, y+32, x+23, y+78, width=3, fill='gray')
        self.create_line(x+23, y+78, x+26, y+98, width=3, fill='gray')
        self.create_line(x+26, y+98, x+31, y+112, width=3, fill='gray')
        self.create_arc(x+30, y+94, x+59, y+121, start=190, extent=165, style='arc', width=3, outline='gray')
        self.create_line(x+59, y+109, x+60, y+95, width=3, fill='gray')
        self.create_line(x+60, y+95, x+59, y+72, width=3, fill='gray')
        self.create_line(x+59, y+72, x+62, y+63, width=3, fill='gray')

        self.create_oval(x+8, y+29, x+34, y+50, fill='#f2f2f2', outline='#cccccc')
        self.create_oval(x+40, y+36, x+66, y+56, fill='#f2f2f2', outline='#cccccc')
        self.create_oval(x+14, y+34, x+27, y+44, fill='black')
        self.create_oval(x+49, y+42, x+62, y+52, fill='black')

        self.create_line(x+11, y+26, x+31, y+20, width=3, fill='black')
        self.create_line(x+52, y+26, x+68, y+35, width=3, fill='black')

        #Have the ability to speak
        self._speechBubble = False
        self._messageWidget = tk.Message(self.master, text='', bg=self.cget('bg'), width=320, font=('Purisa', 16))
        self._messageWidget.place(x=640, y=350)
        self._previousComment = "boop"

        #Respond to clicks
        self.bind("<Button-1>", lambda event: self.makeComment())

        #Have a repertoir of generic, non-analytical comments
        self._randomComments = ["Hmm.. Your progress so far.. I don't really have a comment..",
                "The Analysis Chamber is pretty cool, you should check it out.",
                "Did you know the timer doesn't start until you start typing?",
                "There's no point in generating an all-caps text! That's why the custom text generator for "+\
                "Shift mode only capitalizes the first letter in each word.",
                "When you generate a custom text, your slower letters will appear more often,"+\
                "so that you'll get more practice with those.",
                "I'm here to help you! Come talk to me whenever.",
                "I hang out in the main menu because I like this color.",
                "What's up?",
                "I've been out of work for a while, you know.",
                "My favorite text? Eleonora. *sigh* You really should read the whole thing."]

    def makeComment(self):
        '''Occurs whenever the assistant is clicked. The assistant says something.'''

        # Determine which comment to make! The reason this part is so massive is threefold:
        # 1 - Some comments should only be considered if the user has had X amount of training sessions
        # 2 - There are just a lot of potential comments to consider
        # 3 - To save Clippy's poor nuggin, I've taken an extra step to make sure 'ponder' methods aren't evaluated unless needed
        
        number_of_sessions = len(self._keylog)
        potentialCategories = []

        #Figure out which categories of comments to consider, based on session count
        potentialCategories.append("dumbComment")
        if number_of_sessions > 4:
            #Give the more advanced comments greater odds of appearing
            potentialCategories.append("fourPlus")
            potentialCategories.append("fourPlus")
        if number_of_sessions > 0:
            potentialCategories.append("overZero")
            if number_of_sessions < 3:
                potentialCategories.append("oneOrTwo")
                potentialCategories.append("oneOrTwo")
        else:
            potentialCategories.append("zero")

        #Make sure we don't get the same comment twice in a row
        insightfulComment = self._previousComment
        while insightfulComment == self._previousComment:
            
            #Choose a category of comments
            theChoice = choice(potentialCategories)

            #Pick a specific comment (or method to calculate comment) within the chosen category
            if theChoice == "dumbComment":
                insightfulComment = choice(self._randomComments)

            elif theChoice == "zero":
                zero = choice(["Go on, try an exercise! I'll wait for you.",
                               "You haven't tried any typing exercises yet..",
                               "Choose a text from the list, then click the button."])
                insightfulComment = zero
                
            elif theChoice == "overZero":
                overZero = choice(["self.ponderSignificanceOfShift()",
                                   "Whenever you generate a custom text, the generated text is"+\
                                   " based on the keyboard analysis map currently on-screen.",
                                   "Arguably the best way to improve your typing speed: Leave only custom "+\
                                   "texts selected in the Analysis room, do lots of long custom exercises.",
                                   "You know, if I were a little bit smarter, I bet I could identify you.. "+\
                                   "Just by your keystroke latency."])
                insightfulComment = eval(overZero) if overZero.startswith("self.") else overZero

            elif theChoice == "oneOrTwo":
                oneOrTwo = choice(["So, you picked {} ".format(self._keylog[0][0][0])+\
                                   "as your first exercise.. Very telling. Very telling indeed."])
                insightfulComment = eval(oneOrTwo) if oneOrTwo.startswith("self.") else oneOrTwo
                
            elif theChoice == "fourPlus":
                fourPlus = choice(["self.ponderFiftyShades()",
                                   "self.ponderErrorCount()",
                                   "self.ponderHandedness()",
                                   "self.ponderSpeedImprovement()"])
                insightfulComment = eval(fourPlus) if fourPlus.startswith("self.") else fourPlus
            
        
        #Configure the message widget, draw the speech bubble.
        #Note that we have to update the window to get the size of the message widget,
        #and we need the size of the message widget to draw the speech bubble correctly.
        self._messageWidget.config(text=insightfulComment, bg='white')
        self._messageWidget.place(x=544, y=195) #temporary placement just to calculate the height
        self.master.master.master.update()
        messageHeight = self._messageWidget.winfo_height()

        self._messageWidget.place(x=544, y=195-messageHeight//2)
        self.drawSpeechBubble([200, 200-messageHeight//2, 520, 200+messageHeight//2])

        self._previousComment = insightfulComment

    def ponderSignificanceOfShift(self):

        #Figure out how much time user spends on the next letter after capitalized letters versus not after capitalized letters
        afterBig = [0.0, 0] #[running average delay, running count of occurrences]
        notafterBig = [0.0, 0]
        
        for session in self._keylog:
            previousCharacter = False
            for entry in session:

                #Go through all of the entries in the log, and keep a running average for each category
                if entry[2]:
                    if previousCharacter in konstanter.bigKeyValues and previousCharacter not in konstanter.charsByCategory["punctuation"]:
                        newBigCount = afterBig[1] + 1
                        afterBig[0] = (afterBig[0]*afterBig[1] + entry[1]) / newBigCount
                        afterBig[1] = newBigCount
                    else:
                        newNotBigCount = notafterBig[1] + 1
                        notafterBig[0] = (notafterBig[0]*notafterBig[1] + entry[1]) / newNotBigCount
                        notafterBig[1] = newNotBigCount
                    previousCharacter = entry[0]

        if afterBig[1] > 5:
            statement = "On average, you've spent {}ms typing small letters after capitalized letters.. \
and {}ms otherwise. This is why, to improve consistency, entries directly following Shift entries are ignored in the Analysis Chamber.".format(int(afterBig[0]*1000),
                                                                                                                                               int(notafterBig[0]*1000))
        else:
            statement = "Hmm.. Seems like you haven't been using Shift very much."
        return statement
    
    def ponderFiftyShades(self):

        if funksjoner.numberOfSessions(self._keylog, titles=["Fifty Shades"]) > 0:
            return "I see you've given Fifty Shades a go. You know.. If you're curious, I know a thing or two about bindings."
        else:
            return "You haven't tried Fifty Shades yet? Go on, try it! I'll.. I'll close my eyes."

    def ponderErrorCount(self):

        #Figure out the user's overall error count, compare it to overall keys entered and make a comment
        errorCounter = 0
        entryCounter = 0
        titles = konstanter.tekster.keys()
        for session in self._keylog:
            for entry in session:
                if entry[0] != "Custom text" and entry[0] not in titles:
                    entryCounter += 1
                    if not entry[2]:
                        errorCounter += 1

        errorPercentage = 100 * errorCounter / entryCounter
        if errorPercentage > 10:
            errorComment = "How's that even possible?"
        elif errorPercentage > 7:
            errorComment = '''You're a "type first, think later" kind of person, huh?'''
        elif errorPercentage > 4:
            errorComment = "Pretty sloppy."
        elif errorPercentage > 2:
            errorComment = "Try focusing a little more on accuracy over speed, and it'll help your speed in the long run."
        elif errorPercentage > 0:
            errorComment = "That's pretty much where I'm at, too. Score!"
        else:
            errorComment = "Perfect! Of course, there's no way you'll keep that record for very long."
        return "You've made {0} errors total so far. That's a {1:.1f}% error rate. {2}".format(errorCounter,
                                                                                               errorPercentage,
                                                                                               errorComment)

    def ponderHandedness(self):

        #Consider the average speeds of left-side characters vs right-side characters
        avgLeft = [0.0, 0]
        avgRight = [0.0, 0]

        for session in self._keylog:
            for entry in session:
                if entry[2]:
                    cha = entry[0].lower()
                    if cha in konstanter.charsByCategory["consonants"] or cha in konstanter.charsByCategory["vowels"]:
                        if cha in konstanter.charsByCategory["leftside"]:
                            newcount = avgLeft[1] + 1
                            avgLeft[0] = (avgLeft[0]*avgLeft[1] + entry[1]) / newcount
                            avgLeft[1] = newcount
                        else:
                            newcount = avgRight[1] + 1
                            avgRight[0] = (avgRight[0]*avgRight[1] + entry[1]) / newcount
                            avgRight[1] = newcount
                            
        msLeft = int(avgLeft[0] * 1000)
        msRight = int(avgRight[0] * 1000)

        #Make a comment on the proportion
        if max(msLeft, msRight) / (abs(msLeft-msRight)+0.01) > 8:
            comment = "That's not a huge difference. You're just as {} with both hands, huh?".format("slow" if max(msLeft, msRight) > 200 else "fast")
        elif msLeft < msRight:
            comment = "Seems like.. you're significantly better with your left hand? That's.. interesting.."
        else:
            comment = "I think you should treat your left hand to a workout more often."
        return "You've spent an average of {}ms typing letters on the left hand side of the keyboard, versus {}ms for the right! {}".format(
            msLeft, msRight, comment)

    def ponderSpeedImprovement(self):

        #List all sessions for convenience
        sessionList = []
        for session in self._keylog:
            sessionList.append([session[0][0], session[0][1]])

        #Count how many times each text has been completed
        sessionCount = {}
        for entry in sessionList:
            if entry[0] in sessionCount.keys():
                sessionCount[entry[0]] += 1
            else:
                sessionCount[entry[0]] = 1

        #Identify the most frequently picked text, and check how many times it's been done.
        mostFrequentTitle = max(sessionCount, key=sessionCount.get)
        attempts = sessionCount[mostFrequentTitle]

        #Extract the WPM values for all of the times the user has done that particular exercise
        sessionSpeeds = []
        for item in sessionList:
            if item[0] == mostFrequentTitle:
                sessionSpeeds.append(item[1])

        #Identify the WPM of the most recent session of that title, rank it among the others
        latestSpeed = sessionSpeeds[-1]
        placement = attempts - sorted(sessionSpeeds).index(latestSpeed)

        #Figure out how to put that in human language
        xBest = konstanter.ordinals[placement]+" " if placement in konstanter.ordinals else str(placement)+". "
        if xBest == "first ":
            xBest = ""

        return "Your most frequent exercise is {}. You've completed it {}, and your latest effort was your {}fastest so far.".format(
                mostFrequentTitle,
                str(attempts)+" time" if attempts == 1 else str(attempts)+" times",
                xBest)
            
    def drawSpeechBubble(self, boundaries):

        x1, y1, x2, y2 = boundaries

        if self._speechBubble:
            self.delete(self._speechBubble)
        self._speechBubble = self.create_polygon(x1-30, y1, x1-30, y2, x1-24, y2+14, x1-14, y2+24,
                                                 x1, y2+30, x2-40, y2+30, x2-10, y2+60, x2-22, y2+30,
                                                 x2, y2+30, x2+14, y2+24, x2+24, y2+14,
                                                 x2+30, y2, x2+30, y1, x2+24, y1-14, x2+14, y1-24,
                                                 x2, y1-30, x1, y1-30, x1-14, y1-24, x1-24, y1-14,
                                                 fill='white', outline='black', width=3)
        
    def clearThroat(self):
        '''Removes the speech bubble and its contents'''
        
        if self._speechBubble:
            self.delete(self._speechBubble)
        self._messageWidget.place_forget()
