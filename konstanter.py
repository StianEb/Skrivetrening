smallKeyValues = ['q','w','e','r','t','y','u','i','o','p',
                  'a','s','d','f','g','h','j','k','l',"'",
                  'z','x','c','v','b','n','m',',','.','-']

smallKeyPositions = [(120, 80), (200, 80), (280, 80), (360, 80), (440, 80), (520, 80), (600, 80), (680, 80), (760, 80), (840, 80),
                     (135, 170), (215, 170), (295, 170), (375, 170), (455, 170), (535, 170), (615, 170), (695, 170), (775, 170), (920, 170),
                     (170, 260), (250, 260), (330, 260), (410, 260), (490, 260), (570, 260), (650, 260), (730, 260), (810, 260), (890, 260)]

bigKeyValues = ['!','"', '?',
                'Q','W','E','R','T','Y','U','I','O','P',
                'A','S','D','F','G','H','J','K','L',
                'Z','X','C','V','B','N','M',';',':']

bigKeyPositions = [(80, 0), (160, 0), (880, 0),
                   (120, 80), (200, 80), (280, 80), (360, 80), (440, 80), (520, 80), (600, 80), (680, 80), (760, 80), (840, 80),
                   (135, 170), (215, 170), (295, 170), (375, 170), (455, 170), (535, 170), (615, 170), (695, 170), (775, 170),
                   (170, 260), (250, 260), (330, 260), (410, 260), (490, 260), (570, 260), (650, 260), (730, 260), (810, 260)]

tekster = {"Flying (short)": "If humans could fly, we'd consider it exercise and never do it.",
           "Potatoes (short)": "Your stomach thinks all potato is mashed.",
           "Scooby Doo (short)": "Where are you?",
           "Lottery (short)": "Trying to get rich by playing the lottery is like trying to commit suicide by flying on commercial airlines.",
           "Swiss army (short)": "The Swiss must've been pretty confident in their chances of victory if they included a corkscrew on their army knife.",
           "Doctor (short)": "Once you have a PhD, every meeting you go to becomes a doctor's appointment.",
           "All keys (debug)": '''qwertyuiopasdfghjkl'zxcvbnm,.-!"QWERTYUIOP?ASDFGHJKLZXCVBNM;:''',
           "Hamlet": '''To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take Arms against a Sea of troubles, And by opposing end them: to die, to sleep No more; and by a sleep, to say we end the heart-ache, and the thousand natural shocks that Flesh is heir to? 'Tis a consummation devoutly to be wished.''',
           "Guido van Rossum": '''Python is an experiment in how much freedom programmers need. Too much freedom and nobody can read another's code; too little and expressiveness is endangered.''',
           "Holy Handgrenade": '''First shalt thou take out the Holy Pin. Then shalt thou count to three, no more, no less. Three shall be the number thou shalt count, and the number of the counting shall be three. Four shalt thou not count, neither count thou two, excepting that thou then proceed to three. Five is right out. Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thy foe, who, being naughty in my sight, shall snuff it.''',
           "Frederick Donaldson": '''The Seven Social Sins are: Wealth without work. Pleasure without conscience. Knowledge without character. Commerce without morality. Science without humanity. Worship without sacrifice. Politics without principle.''',
           "Eleonora": '''Years dragged themselves along heavily, and still I dwelled within the Valley of the Many-Colored Grass; but a second change had come upon all things. The star-shaped flowers shrank into the stems of the trees, and appeared no more. The tints of the green carpet faded; and, one by one, the ruby-red asphodels withered away; and there sprang up, in place of them, ten by ten, dark, eye-like violets, that writhed uneasily and were ever encumbered with dew.''',
           "Fifty Shades": '''"Does this mean you're going to (strongly cuddle) me tonight, Christian?" Holy (smokes). Did I just say that? His mouth drops open slightly, but he recovers quickly. "No, Anastasia it doesn't. Firstly, I don't (strongly cuddle). I (exercise).. hard. Secondly, there's a lot more paperwork to do, and thirdly, you don't yet know what you're in for. You could still run for the hills. Come, I want to show you my playroom." My mouth drops open. (exercise) hard! Holy (smokes), that sounds so.. hot.'''}
    
charsByCategory = {"vowels": ['e', 'u', 'i', 'o', 'a'],
                   "consonants": ['q', 'w', 'r', 't', 'y', 'p', 's', 'd', 'f',
                                  'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v',
                                  'b', 'n', 'm'],
                   "punctuation": ['!', '"', '?', "'", ',', '.', '-', ';', ':'],
                   "leftside": ['q','w','e','r','t','a','s','d','f','g','z','x','c','v','b']}

ordinals = {1: "first",
            2: "second",
            3: "third",
            4: "fourth",
            5: "fifth",
            6: "sixth",
            7: "seventh",
            8: "eighth",
            9: "ninth"}
            
