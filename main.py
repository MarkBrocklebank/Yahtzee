import random

########################################################################
#Classes
#rolls a random value from 1-6
#accessed by dice.value
class Dice:
    def __init__(self):
        self.value = random.randint(1,6)

    def __str__(self):
        return "Dice value: " + str(self.value)

#populates a hand with 5 dice
#contains methods for rerolling a hand
#contains methods for scoring a hand
#turn - a counter of how many rerolls have been
class Hand:
    def __init__(self):
        self.dices = []
        self.turn = 1
        for i in range(5):
            tempDice = Dice()
            self.dices.append(tempDice)

        self.dieValues = []
        for item in self.dices:
            self.dieValues.append(item.value)

    def __str__(self):
        return "\nPlayer hand contains: {}, {}, {}, {}, {}".format(self.dices[0].value, self.dices[1].value, self.dices[2].value, self.dices[3].value, self.dices[4].value)

    #takes a list of the dice the user wishes to change
    #changes the values in the dices list
    #only allows for two rerolls
    def rerollHand(self,dieList):
        if self.turn >= 3:
            outputStr = "Only two rerolls are allowed"
        else:
            outputStr = "Rerolling die: "
            for item in dieList:
                outputStr += str(item + 1) + ", "
            outputStr = outputStr[:-2]
        print (outputStr)
        for i in range(5):
            if i in dieList:
                self.dices[i] = Dice()
        #updates the dieValues variable after the reroll
        self.dieValues = []
        for item in self.dices:
            self.dieValues.append(item.value)
        self.turn += 1
        return self.dices


#Contains the variables relating to the player
#Holds their score
#Can generate a new hand
#Scorecard holds the values they have assigned to each score
class Player:
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.oneHand = ""
        self.scoreCard = {"Aces":"-","Twos":"-","Threes":"-","Fours":"-","Fives":"-","Sixes":"-",\
                          "ThreeOfKind":"-","FourOfKind":"-","FullHouse":"-","LowStraight":"-","HighStraight":"-","Yahtzee":"-","Chance":"-"}
        self.handNumber = 0

    def __str__(self):
        return "Player name - {}\nPlayer score - {}\nPlayer hand - {}".format(self.name,self.score,self.oneHand)

    def NewHand(self):
        self.handNumber += 1
        print("\n\nPlayer - {}. Turn number - {}".format(self.name,self.handNumber))
        self.oneHand = Hand()
        print(self.oneHand)
        return self.oneHand

    def DisplayScorecard(self):
        print("Player: {}. Hand Number: {}. Current Player Scores:\n----------\nAces:{}\nTwos:{}\nThrees:{}\nFours:{}\nFives:{}\nSixes:{}\n----------\nThree of a kind:{}\nFour of a kind:{}\nFull House:{}\nLow Straight:{}\
            \nHigh Straight:{}\nYahtzee:{}\nChance:{}\n----------\nTotal:{}"\
            .format(self.name,self.handNumber,self.scoreCard["Aces"],self.scoreCard["Twos"],self.scoreCard["Threes"],self.scoreCard["Fours"],self.scoreCard["Fives"],self.scoreCard["Sixes"],\
            self.scoreCard["ThreeOfKind"],self.scoreCard["FourOfKind"],self.scoreCard["FullHouse"],self.scoreCard["LowStraight"],self.scoreCard["HighStraight"],self.scoreCard["Yahtzee"],\
            self.scoreCard["Chance"],self.TotalScore()))


    ######SCORING#####

    def TotalScore(self):
        score = 0
        for i in self.scoreCard.values():
            if i != "-":
                score += i
        return score

    #return a score for a single value of the dice
    #Use a dictionary to convert from number to word
    def ScoreSingle(self,dieValue):
        numToWord = {1:"Aces",2:"Twos",3:"Threes",4:"Fours",5:"Fives",6:"Sixes"}
        tempScore = 0
        for item in self.oneHand.dieValues:
            if item == dieValue:
                tempScore += dieValue
        self.scoreCard[numToWord[dieValue]] = tempScore
        return tempScore

    #create a list of the count of each die in the list
    #sort this list desc
    #if the highest occurence is greater than 3, sum all dice
    def ScoreThreeOfKind(self):
        tempScore = 0
        countList = []
        for item in self.oneHand.dieValues:
            countList.append(self.oneHand.dieValues.count(item))
            countList.sort(reverse = True)
        if countList[0] >=3:
            for value in self.oneHand.dieValues:
                tempScore += value

        self.scoreCard["ThreeOfKind"] = tempScore
        return tempScore

    # create a list of the count of each die in the list
    # sort this list desc
    # if the highest occurence is greater than 4, sum all dice
    def ScoreFourOfKind(self):
        tempScore = 0
        countList = []
        for item in self.oneHand.dieValues:
            countList.append(self.oneHand.dieValues.count(item))
            countList.sort(reverse=True)
        if countList[0] >= 4:
            for value in self.oneHand.dieValues:
                tempScore += value

        self.scoreCard["FourOfKind"] = tempScore
        return tempScore

    # create a list of the count of each die in the list
    # if there is two of one dice and three of another then return 25
    def ScoreFullHouse(self):
        tempScore = 0
        countValues = []
        if UniqueDice(self.oneHand) == 2:
            self.oneHand.dieValues.sort()
            countValues.append(self.oneHand.dieValues.count(self.oneHand.dieValues[0]))
            countValues.append(self.oneHand.dieValues.count(self.oneHand.dieValues[4]))
            if all(x in countValues for x in [2,3]):
                tempScore = 25

        self.scoreCard["FullHouse"] = tempScore
        return tempScore

    #Check if the three acceptable dice combos are found in the hand
    def ScoreLowStraight(self):
        tempScore = 0

        if (all(x in self.oneHand.dieValues for x in [1,2,3,4])) or (all(x in self.oneHand.dieValues for x in [2,3,4,5])) or (all(x in self.oneHand.dieValues for x in [3,4,5,6])):
            tempScore = 30

        self.scoreCard["LowStraight"] = tempScore
        return tempScore

    #Check if the two acceptable dice combos are found in the hand
    def ScoreHighStraight(self):
        tempScore = 0
        self.oneHand.dieValues

        if (all(x in self.oneHand.dieValues for x in [1,2,3,4,5])) or (all(x in self.oneHand.dieValues for x in [2,3,4,5,6])):
            tempScore = 40
        self.scoreCard["HighStraight"] = tempScore
        return tempScore

    #Check if there is only one unique die
    def ScoreYahtzee(self):
        tempScore = 0
        if UniqueDice(self.oneHand) == 1:
            tempScore = 50

        self.scoreCard["Yahtzee"] = tempScore
        return tempScore

    #Sum all the dice
    def ScoreChance(self):
        tempScore = 0
        for item in self.oneHand.dieValues:
            tempScore += item
        self.scoreCard["Chance"] = tempScore
        return tempScore


############################################
#Helper functions

#given a hand object
#return the number of unique die
def UniqueDice(myHand):
    dieFound = []
    for die in myHand.dices:
        if die.value not in dieFound:
            dieFound.append(die.value)
    return len(dieFound)





##############################################
#Logic Controls

def Main():
    print("Welcome to my Yahtzee! player!")

    acceptedResponce = ["1","2","3"]
    gameMode = 0
    while gameMode not in acceptedResponce:
        gameMode = input("Please select a game mode from the following list:\n(1) Single Player - Single hand\n(2) Single Player - Full game\n(3) Multi Player - Full game")
        if gameMode not in acceptedResponce:
            print("Expected response not found, please try again.")

    if gameMode == "1":
        #single player single hand
        SinglePlaySingleHand()
    elif gameMode == "2":
        #single player multi hand
        SinglePlayMultiHand()
    elif gameMode == "3":
        #multi player full game
        MultiPlayerMultiHand()


def SinglePlaySingleHand():
    print("\n Single player, single hand mode chosen")
    playerName = input("What is your name?")
    print("\nGreetings {}, let us begin".format(playerName))
    myPlayer = Player(playerName)
    myPlayer.NewHand()
    turnScore = OnePlayerTurn(myPlayer)
    print("\nHand completed. You scored {} points".format(turnScore))
    myPlayer.DisplayScorecard()

    finalScore = myPlayer.TotalScore()
    print("\nThanks for playing!!\nYour final score was {} points!".format(finalScore))


def SinglePlayMultiHand():
    print("\nSingle player, full game chosen.")
    playerName = input("What is your name?")
    print("\nGreetings {}, let us begin".format(playerName))
    myPlayer = Player(playerName)

    for i in range(13):
        myPlayer.NewHand()
        turnScore = OnePlayerTurn(myPlayer)
        print("\nHand completed. You scored {} points".format(turnScore))
        myPlayer.DisplayScorecard()

    finalScore = myPlayer.TotalScore()
    print("\nThanks for playing!!\nYour final score was {} points!".format(finalScore))

def MultiPlayerMultiHand():
    print("\nMulti player, full game chosen.")
    noPlayers = ["2","3","4"]
    noPlayersChoice = ""
    while noPlayersChoice not in noPlayers:
        noPlayersChoice = input("Please select a number of players. (2,3,4)")

    players = []
    for item in range(int(noPlayersChoice)):
        tempName = input("Player {} - What is your name?".format(item+1))
        tempPlayer = Player(tempName)
        players.append(tempPlayer)

    #Run for 13 rounds
    for i in range(13):
        for playerItem in players:
            playerItem.NewHand()
            turnScore = OnePlayerTurn(playerItem)
            print("\nHand Completed. You scored {} points".format(turnScore))
            playerItem.DisplayScorecard()

    #output string
    outStr = "\n"
    for j in players:
        outStr += "{} {} \n".format(j.name,j.TotalScore())
    print("\n\nGame complete\nFinal Scores: {}".format(outStr))



def OnePlayerTurn(myPlayer):
    counter = 1
    while counter < 3:
        rerollCheck = ""
        while rerollCheck not in ["Y", "N"]:
            rerollCheck = input("\nTurn number {}. Would you like to reroll your dice? (Y/N)".format(counter))
        if rerollCheck == "Y":
            rerollPositionsStr = input("\nWhich dice would you like to reroll? (Give answers in the form '1,3,4')")
            rerollList = rerollPositionsStr.split(",")
            rerollListInt = []
            for item in rerollList:
                rerollListInt.append(int(item) - 1)

            myPlayer.oneHand.rerollHand(rerollListInt)
            print(myPlayer.oneHand)
            counter += 1
        elif rerollCheck == "N":
            counter = 4


    # How they want to score it
    scoreInput = "0"
    scoreAvailable = False
    numToWord = {1: "Aces", 2: "Twos", 3: "Threes", 4: "Fours", 5: "Fives", 6: "Sixes", 7:"ThreeOfKind",8:"FourOfKind",9:"FullHouse",10:"LowStraight",11:"HighStraight",12:"Yahtzee",13:"Chance"}
    while int(scoreInput) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] or scoreAvailable == False:
        scoreInput = input("\nWhich value would you like to score your dice against?\n (1) Aces, (2) Twos, (3) Threes, (4) Fours, (5) Fives, (6) Sixes,\n\
                                               (7) Three of a kind, (8) Four of a kind, (9) Full House, (10) Low Straight, (11) High Straight, (12) Yahtzee, (13) Chance")

        scoreInput = int(scoreInput)
        scoreWord = numToWord[scoreInput]
        if myPlayer.scoreCard[scoreWord] == "-":
            scoreAvailable = True
        else:
            scoreAvailable = False
            print("That score has already been assigned, please select a new one.")

    if scoreAvailable == True:
        if scoreInput <= 6:
            outputScore = myPlayer.ScoreSingle(scoreInput)
        elif scoreInput == 7:
            outputScore = myPlayer.ScoreThreeOfKind()
        elif scoreInput == 8:
            outputScore = myPlayer.ScoreFourOfKind()
        elif scoreInput == 9:
            outputScore = myPlayer.ScoreFullHouse()
        elif scoreInput == 10:
            outputScore = myPlayer.ScoreLowStraight()
        elif scoreInput == 11:
            outputScore = myPlayer.ScoreHighStraight()
        elif scoreInput == 12:
            outputScore = myPlayer.ScoreYahtzee()
        elif scoreInput == 13:
            outputScore = myPlayer.ScoreChance()

        return outputScore




######################################################################
#Tests
def test1():
    myHand = Hand()

    print(myHand)

    myHand.rerollHand([1,3])
    myHand.rerollHand([1,3])

    print(myHand)

    myHand.rerollHand([0,1,2,3,4])

    print(myHand)

def test2():
    myPlayer = Player("Mark")
    print(myPlayer)
    myPlayer.NewHand()

    print(myPlayer.oneHand)
    myPlayer.oneHand.rerollHand([1])
    print(myPlayer.oneHand)

    #myPlayer.DisplayScorecard()
    myPlayer.ScoreChance()
    myPlayer.ScoreYahtzee()
    myPlayer.ScoreSingle(3)
    myPlayer.ScoreFullHouse()
    myPlayer.ScoreFourOfKind()
    myPlayer.ScoreHighStraight()
    myPlayer.ScoreLowStraight()
    myPlayer.ScoreThreeOfKind()
    myPlayer.DisplayScorecard()

    print("unique die {}".format(UniqueDice(myPlayer.oneHand)))

def test3():
    listOne = [6,1,3,5,4]

    tempScore = 0

    if (all(x in listOne for x in [1, 2, 3, 4])) or (all(x in listOne for x in [2, 3, 4, 5])) or (all(x in listOne for x in [3, 4, 5, 6])):
        tempScore = 30

    print(tempScore)

def test4():
    tempScore = 0
    sampleHand = [1,6,6,6,1]
    countValues = []

    sampleHand.sort()
    countValues.append(sampleHand.count(sampleHand[0]))
    countValues.append(sampleHand.count(sampleHand[4]))
    if all(x in countValues for x in [2, 3]):
        tempScore = 25

    #self.scoreCard["FullHouse"] = tempScore
    print(tempScore)

def test5():
    tempScore = 0
    egHand = [5,5,5,5,1]
    countList = []
    for item in egHand:
        countList.append(egHand.count(item))
        countList.sort(reverse=True)
    if countList[0] >= 4:
        for value in egHand:
            tempScore += value

    #self.scoreCard["ThreeOfKind"] = tempScore
    return tempScore

#test2()
def test6():
    listTest = ["1","2","3","4","5"]
    print(listTest)
    outList = []
    for item in listTest:
        outList.append(int(item) - 1)

    print(outList)

def test7():
    myPlayer = Player("mark")
    myPlayer.NewHand()

    print(myPlayer.scoreCard["Aces"] == "-")



def test8():
    counter = 1
    checker = False
    while checker == False:
        counter = int(input("Give number"))
        print(counter)
        if counter > 5:
            checker = True
        else:
            checker = False


    print(counter)
    print(5+5)
#test8()

Main()