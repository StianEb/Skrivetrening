##
# Oppgave 6: Egenoppgave
#
# Lag et skrivetreningsprogram med grafisk brukergrensesnitt. Programmet skal MINST inneholde:
#
# * Funksjonalitet for analyse av tastaturbruk, herunder:
#       - Et fargekart over tastaturet, som illustrerer gjennomsnittlig relativ skrivehastighet for hver tast
#       - En antropomorfisk figur som fungerer som personlig skrivetrener, ideelt en opphavsrettsbeskyttet figur
#       - Løpende tilbakemelding på skrivehastighet / nøyaktighet mens man skriver
#
# * Funksjonalitet for skrivetrening, herunder:
#       - En rekke utdrag fra klassiske tekster som brukeren kan velge mellom til skrivetrening
#       - Mulighet for å automatisk generere nye tekster, hvor taster brukeren er svak på dukker opp oftere
#
# * Ryddighet i kode og brukergrensesnitt, herunder:
#       - Separate, ulikefargede 'rom' for separate formål, f.eks. en hovedmeny, et rom for analyse osv.
#       - Prosedyrer, funksjoner og klasser i separate filer
#       - Engelsk språk i brukergrensesnittet, det fins ikke nok maskinvare på engelsk
#
# Programmet forventes dessuten å laste og lagre all informasjon om brukeren, slik at grunnlaget for tidligere nevnt
# analyse ikke nullstilles hver gang man lukker programmet, men samler seg opp og gir større nøyaktighet over tid.
#
# Det gis ikke anledning til utsettelse av leveringsfrist, og ubrukte, tomme lister som ligger og slenger i koden
# er synonymt med stryk og potensiell adgangsbegrensning til universitetets fasiliteter på ubestemt tid.
#

# 5: Clippy's eyes follow you, and other animations
# 3: More analytical comments from the assistant! (which text was the quickest, how much slower are Custom texts)
# 3: Filtering out obvious outliers before calculating averages

#Til Gaute: Jeg bruker en modul som heter 'colour' i prosedyrer.py. (Ikke 'color'!)

from tkinter import Tk, Frame
import prosedyrer

def initializeFrames(root):
    
    prosedyrer.createTypingRoom(root)
    prosedyrer.createAnalysisChamber(root)
    prosedyrer.createMainMenu(root)

def load(root):
    try:
        with open("saved_logs") as file:
            for line in file:
                exec("root.keylog.append(" + line + ")") #this allows for very easy saving
        print("Saved log found, resuming previous session.")
    except EnvironmentError:
        print("No saved data found, starting fresh.")

def main():

    #Initialize the window (master) and frame container (root)
    master = Tk()
    master.minsize(1200,600)
    master.root = Frame(master)
    master.root.pack(fill="both", expand=True)

    #Allow for child frames in (0, 0) (soon to be all of the rooms) to fill root completely
    master.root.grid_rowconfigure(0, weight=1)
    master.root.grid_columnconfigure(0, weight=1)

    #Initialize the keylog, which is the history of all key presses during exercises. Structured as follows:
    #keylog = [session, session, session..]
    #session = [[string=character, float=seconds since last recorded input, bool=correct input], ...]
    master.root.keylog = []

    #Create all rooms (frames)
    initializeFrames(master.root)

    #Load the game
    load(master.root)
    
    master.mainloop()


if __name__ == "__main__":
    main()
