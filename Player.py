import random
def main():
    while True:
        print("Mastermind codecracker")
        count = 0

        #Get the code length
        done = False
        while not done:
            user_response = input("Length of code?\n")
            if user_response.isnumeric():
                count = int(user_response)
                done = True
            else:
                print("Input must be a number")

        #Get the possible characters in code
        user_response = input("Possible values of characters in code, separated by commas?\n(e.g. a,b,c,d or blue,red,green,white)\n")
        choices = user_response.split(",")


        #Initialize the player
        code = Code(choices, count)
        player = Player(code)

        print("Player will now attempt to crack the code")
        print("After each attempt, the user must enter the number of:")
        print("Correct positions")
        print("Correct characters (Including characters in correct positions)")
        input("Press enter to start")
        turns = 1
        solved = False
        while not solved:
            guess = player.guessElements()

            print(code.convertGuess(guess))
            while True:
                right_positions = input("Correct positions? ")
                if right_positions.isdigit():
                    break
            while True:
                right_characters = input("Correct characters? ")
                if right_characters.isdigit():
                    break
            #load result
            if int(right_positions) == count:
                solved = True
            else:
                player.storeResults(guess, int(right_characters), int(right_positions))
                turns += 1

        print("Cracked the code! Attempts: " + turns)
        user_response = input("Play again? (y/n")
        if user_response.upper() == "Y":
            print("Goodbye!")
            break
    return

def run(length, domain):
    code = Code(domain, length)
    player = Player(code, True)
    turns = 0
    while True:
        turns += 1
        guess = player.guessElements()
        #print("Guess: {}".format(guess))
        #print(guess)
        count = code.checkGuessCount(guess)
        #print("Count: " +str(count))
        if turns > 10:
            print("Breakpoint")
        if count == code.count:
            print("All elements found! Turns: " + str(turns))
            return turns
        player.storeResults(guess, count, 0)

def competeGuided(length, domain):
    code = Code(domain, length)
    player = Player(code, True)
    guided_turns = 0
    while True:
        guided_turns += 1
        if guided_turns > (len(domain)*len(domain)):
            print("Game turns in excess of |domain|^2, Game stopped")
            break
        guess = player.guessElements()
        # print("Guess: {}".format(guess))
        # print(guess)
        count = code.checkGuessCount(guess)
        # print("Count: " +str(count))
        if count == code.count:
            # print("All elements found! Turns: " + str(turns))
            break
        player.storeResults(guess, count, 0)

    player = Player(code, False)
    unguided_turns = 0
    while True:
        unguided_turns += 1
        if unguided_turns > (len(domain) * len(domain)):
            print("Game turns in excess of |domain|^2, Game stopped")
            break
        guess = player.guessElements()
        # print("Guess: {}".format(guess))
        # print(guess)
        count = code.checkGuessCount(guess)
        # print("Count: " +str(count))
        if count == code.count:
            #print("All elements found! Turns: " + str(turns))
            break
        player.storeResults(guess, count, 0)
    return [guided_turns, unguided_turns]

def competeTimed(length, domain, guesses, guided):
    code = Code(domain, length)
    player = Player(code, guided)
    turns = 0
    while True:
        turns += 1
        guess = player.guessElements()
        # print("Guess: {}".format(guess))
        # print(guess)
        count = code.checkGuessCount(guess)
        # print("Count: " +str(count))
        if count == code.count:
            #print("All elements found! Turns: " + str(turns))
            return [True, turns]
        elif turns >= guesses:
            return [False, turns]
        player.storeResults(guess, count, 0)


#Store this in a database, figure out what best operation is by analyzing this
 # [ [guess], characters, positions, [answer] ]

class Player:
    def __init__(self, code, guided):
        self.n = len(code.choices)
        self.domain = {a for a in range(self.n)}
        self.k = code.count
        self.element_guesses = { frozenset(self.domain):self.k }
        self.code = code
        self.guided = guided

    #Log the results
    def storeResults(self, guess_set, elements, positions):
        self.element_guesses[frozenset(guess_set)] = elements
    #Guesses the elements in the code based on prior guesses
    def guessElements(self):
        guess = set()
        #P(x element Code) = *Sum of P(Guess | x element Guess)

        #Try every number once if guided
        if self.guided and len(self.element_guesses)-1 < self.n/self.k:
            i = (len(self.element_guesses)-1) * self.k
            while len(guess) < self.k:
                guess.add((i%self.n))
                i += 1
        else:
            #We have probability for each group of numbers, build a sequence

            for position in range(self.k):
                #For each number...
                element_probability = { el : self.k/self.n for el in (self.domain - guess) }
                for prior_guess in self.element_guesses:
                    intersection = guess.intersection(prior_guess)
                    intersection = len(intersection)
                    for element in prior_guess:
                        if element not in guess:
                            #if intersection != 0: print(intersection)

                            probability = 1
                            if self.element_guesses[prior_guess]-intersection >= 0 and self.k-intersection > 0 and self.element_guesses[prior_guess]/self.k >= 0:
                                probability = (self.element_guesses[prior_guess]-intersection)/(self.k-intersection)

                            element_probability[element] *= probability
                        #else:
                        #    element_probability[element] = 0
                sorted_prob = sorted(element_probability, key=element_probability.get, reverse=True)
                #print("Probabilities for position {} on guess {}".format(position, len(self.element_guesses)))
                #print(element_probability)
                #print("Selected {}".format(sorted_prob[0]))
                if element_probability[sorted_prob[0]] < 0:
                    print("---NEGATIVE PROBABILITY---")
                i = 0
                while True:
                    check = guess.copy()
                    if i >= len(sorted_prob):
                        print("INDEX OUT OF BOUNDS")
                        i -= 1
                        break
                    check.add(sorted_prob[i])
                    if frozenset(check) not in self.element_guesses:
                        break
                    i += 1
                guess.add(sorted_prob[i])



        return guess

class PlayerOld:
    known_states = [] #[ right_place, right_choice, [state] ]
    position_probability = []
    choice_probability = []
    def __init__(self, code):
        self.code = code
        self.tries = 0
        self.guess = Guess(code)

        #Initialize the probability arrays
        for i in range(self.code.count):
            position = []
            for j in range(len(self.code.choices)):
                position.append(0)
            self.choice_probability.append(position)
            self.position_probability.append(position)



    def guessSolution(self):
        if not self.tries == 0:
            #do stuff
            print("Performing operations on the guess to make it a better guess")
        return self.guess




    def results(self, right_place, right_choice, state):
        self.known_states.append([right_place, right_choice, state])

        #Initial memory only #NOT SURE HOW THIS WILL WORK...
        for position in range(self.code.count):
            self.choice_probability[position][ state[position] ] += right_choice/self.code.count
            self.position_probability[position][state[position]] += right_place/self.code.count

        self.tries += 1

class Code:
    def __init__(self, domain, size):
        self.choices = domain
        self.count = size

        if self.count < len(self.choices):
            self.code = []
            self.codeset = set()
            while len(self.codeset) < self.count:
                random_int = int(random.randrange(0, len(self.choices)))
                if random_int not in self.codeset:
                    self.code.append(random_int)
                    self.codeset.add(random_int)
                #self.code.append(self.choices.pop())
            self.codeset = frozenset(self.codeset)
            self.choices = self.choices.union(self.codeset)


    def convertGuess(self, guess):
        string_guess = []
        for pos in guess:
            string_guess.append(self.choices[pos])
        return string_guess

    def checkGuessCount(self, guess):
        count = 0
        for item in guess:
            if item in self.codeset:
                count += 1
        return count



