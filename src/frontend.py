from src.backend import BackEnd

class FrontEnd:
    """This part completely handles the console/graph interface"""
    def __init__(self):
        self.backend = BackEnd()
        self.quit = False
        self.errorMessage = ""

    def initializeConsole(self):
        print("Initializing...")
        self.backend.initialize()
        while not self.quit:
            print("\n"*50)
            print(self.errorMessage)
            self.errorMessage = ""
            print("\nIn case you want to quit, type Q")
            print("You can search through the carbon/temperature history by giving an example input of\n\"1960-1987\"\nThe following input will grant you with a graph of the following timeline")
            print("You can also input specific years which will grant you the summary of the Carbon Footprint of that year. Example \"1967\", will give you the graph of that year.")
            print("\nRemember \"-\" in between of multiple years\n")
            yearInput = input(">")
            yearInput = yearInput.split("-")
            try:
                if yearInput[0].lower() == "q":
                    self.quit = True
                if(len(yearInput) == 1):
                    firstYear = int(yearInput[0])
                    interact = self.backend.interact([firstYear])
                else:
                    firstYear, secondYear = int(yearInput[0]), int(yearInput[1])
                    interact = self.backend.interact([firstYear, secondYear])
                if interact != None:
                    self.errorMessage = interact
            except (ValueError, IndexError):
                self.errorMessage = "Error. Input not valid. Examples 1960-1980, or a specific year 2005"
            