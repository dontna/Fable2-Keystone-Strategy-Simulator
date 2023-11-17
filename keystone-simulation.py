import random, os

class Dice:
    def __init__(self, dice_max=6):
        self.dice_max = dice_max # the largest number on the die
        self.dice_roll_results = [] # A list contaning each number each die landed on.
        self.dice_total = 0 # The total of all the 'dice_roll_results' added together. Example: 5,6,1 would give 12.

    def roll_dice(self, dice_to_roll: int=3):
        '''randomly "roll" some dice to decide what number each die lands on.

        you can change 'dice_to_roll' to the number of dice you wish to roll. Default: 3'''
        
        # Randomly choose a digit between 1 to 'dice_max' for each 
        for x in range(dice_to_roll):
            self.dice_roll_results.append(random.randint(1, self.dice_max))

        # the total sum of the dice added up.
        self.dice_total = sum(self.dice_roll_results)

    def clear_dice_roll_results():
        self.dice_roll_results = []

class Game:
    def __init__(self, bet_per_space=5, starting_chips=800, bet_on_trips=False, bet_on_sides=False, bet_on_red_black=False, bet_on_keystone=False, bet_on_pair=False, bet_on_run=False, bet_on_odd_even=False, spaces_bet_on=[], rounds_to_simulate=100):
        self.dice = Dice() # Our dice, with default values.
        self.spaces_bet_on = [] # A list of numbers we have bet on, used to check if we won.
        self.starting_chips = starting_chips # How many chips to start with.
        self.current_chips = self.starting_chips # The current chip balance
        self.min_bet = bet_per_space # The minimum ammount of chips for any space.
        self.current_bet = 0 # The total wager of our bet, for this round
        self.wins = 0 # Number of wins
        self.losses = 0 # Number of losses
        self.chips_lost = 0 # How many chips we lost in total
        self.chips_won = 0 # How much profit we made in total
        self.current_round = 0 # Holds the current round number, used to calculate percentages.
        self.bet_on_trips = bet_on_trips # Bool to bet on: trips, triple 1, triple 2, triple 3 and triple 4
        self.bet_on_sides = bet_on_sides # Bool to bet on: 4-9 and 12-17
        self.bet_on_red_black = bet_on_red_black # Bool to bet on: Red and Black
        self.rounds_to_simulate = rounds_to_simulate # Goal of how many rounds to simulate, can be less if we lose our balance.
        self.odds = {
                3:(self.min_bet * 200),
                4:(self.min_bet * 70),
                5:(self.min_bet * 35),
                6:(self.min_bet * 20),
                7:(self.min_bet * 13),
                8:(self.min_bet * 9),
                9:(self.min_bet * 7.6),
                10:(self.min_bet * 7),
                11:(self.min_bet * 7),
                12:(self.min_bet * 7.6),
                13:(self.min_bet * 9),
                14:(self.min_bet * 13),
                15:(self.min_bet * 20),
                16:(self.min_bet * 35),
                17:(self.min_bet * 70),
                18:(self.min_bet * 200),
                "trip_2":(self.min_bet * 200),
                "trip_3":(self.min_bet * 200),
                "trip_4":(self.min_bet * 200),
                "trip_5":(self.min_bet * 200),
                "trips":(self.min_bet * 34),
                "4-9":(self.min_bet * 1.6),
                "12-17":(self.min_bet * 1.6),
                "black":(self.min_bet * 1.6),
                "red":(self.min_bet * 1.6),
                "odd":(self.min_bet * 1.6),
                "even":(self.min_bet * 1.6),
                "keystone":(self.min_bet * 3),
                "pair":(self.min_bet * 1.2),
                "run":(self.min_bet * 8)
                } # Dictionary of all spaces and how much the player wins, gathered data from Fable II not Pub Games.
        self.end_simulation = False # Bool to tell the simulation if we should stop, usually due to not enough chips for anymore bets
        self.single_bet = False # Not used. Was going to be used to see if we had placed any bets on single numbers.
        self.bet_on_keystone = bet_on_keystone # Bool to bet on: 10 and 11
        self.bet_on_pair = bet_on_pair # Bool to bet on the dice rolled having two matching numbers
        self.bet_on_run = bet_on_run # Not used. Bool to bet on the dice rolled having a combination of numbers in a row such as: 1,2,3
        self.bet_on_odd_even = bet_on_odd_even #Bool to bet on: Odd and Even
        self.bets_placed = 0 # Used to tell the simulation how many bets were placed during any given round. used for calculations.
        self.wager_per_round = 0 # How many chips we are betting, in total, each round. Used for calculations.
        self.bets_per_round = 0 # How many spaces we are betting on each round. Used for calculations.
        self.vX = [] # X axis in matplotlib
        self.vY = [] # Y axis in matplotlib

    def did_win(self):
        '''checks if a bet won, returns a bool'''
        if self.bet_on_trips:
            trip_table = [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6]]

            if self.dice.dice_roll_results in trip_table:
                return True
            return False
        elif self.bet_on_sides:
            side_table = [4,5,6,7,8,9,12,13,14,15,16,17]

            if self.dice.dice_total in side_table:
                return True
            return False
        else:
            for bet in self.spaces_bet_on:
                if bet == self.dice.dice_total:
                    return True
            return False
    
    def place_bet(self):
        '''places bets on the correct numbers, depending on which strategy the simulation is using.'''
        # set current bet
        if self.bet_on_trips:
            self.bets_placed += 5

        if self.bet_on_red_black:
            self.bets_placed += 2

        if self.bet_on_sides:
            self.bets_placed += 2

        if self.bet_on_odd_even:
            self.bets_placed += 2

        if self.bet_on_keystone:
            self.bets_placed += 1

        if self.bet_on_pair:
            self.bets_placed += 1

        if self.bet_on_run:
            self.bets_placed += 1

        #if len(self.spaces_bet_on) != 0:
            #self.current_bet += self.min_bet * len(self.spaces_bet_on)
            #self.bets_placed += len(self.spaces_bet_on)
         
        self.current_bet = (self.bets_placed * self.min_bet)

        if self.wager_per_round == 0:
            self.wager_per_round = self.current_bet

        # end simulation if not enough chips for current bet
        if self.current_chips < self.current_bet:
            self.end_simulation = True
            self.current_bet = 0
            return
        else:
            self.current_chips = self.current_chips - self.current_bet

        # set spaces bet on, if bet on a special case
        if self.bet_on_trips:
            self.spaces_bet_on += [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6]]
            
        if self.bet_on_red_black or self.bet_on_sides or self.bet_on_odd_even:
            self.spaces_bet_on += [4,5,6,7,8,9,12,13,14,15,16,17]

        if self.bet_on_keystone:
            self.spaces_bet_on += [10,11]

    def payout(self):
        bets_lost = self.bets_placed
        chips_won_this_round = 0

        black_numbers = [4,7,8,12,15,16]
        red_numbers = [5,6,9,13,14,17]
        odd_numbers = [5,7,9,13,15,17]
        even_numbers = [4,6,8,12,14,16]
        run_numbers = [[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8],[7,8,9]]

        if self.bet_on_trips and self.dice.dice_roll_results in [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6]]:
            if self.dice.dice_roll_results in [[2,2,2],[3,3,3],[4,4,4],[5,5,5]]:
                chips_won_this_round += (self.min_bet + self.odds["trip_5"])
                bets_lost -= 1

            chips_won_this_round += (self.min_bet + self.odds["trips"])
            bets_lost -= 1

        if self.bet_on_odd_even and self.dice.dice_total in self.spaces_bet_on:
            chips_won_this_round += (self.min_bet + self.odds["odd"])
            bets_lost -= 1

        if self.bet_on_sides and self.dice.dice_total in self.spaces_bet_on:
            chips_won_this_round += (self.min_bet + self.odds["4-9"])
            bets_lost -= 1

        if self.bet_on_red_black and self.spaces_bet_on in black_numbers or self.bet_on_red_black and self.spaces_bet_on in red_numbers:
            chips_won_this_round += (self.min_bet + self.odds["black"])
            bets_lost -= 1

        if self.bet_on_odd_even and self.dice.dice_total in odd_numbers or self.bet_on_odd_even and self.dice.dice_total in even_numbers:
            chips_won_this_round += (self.min_bet + self.odds["even"])
            bets_lost -= 1

        if self.bet_on_run and self.dice.dice_roll_results in run_numbers:
            chips_won_this_round += (self.min_bet + self.odds["run"])
            bets_lost -= 1

        # To be finished, need to add and condition
        if self.bet_on_pair:
            chips_won_this_round += (self.min_bet + self.odds["pair"])
            bets_lost -= 1

        if self.bet_on_keystone and self.spaces_bet_on in [10,11]:
            chips_won_this_round += (self.min_bet + self.odds["keystone"])
            bets_lost -= 1
        
        self.chips_won += (chips_won_this_round - self.current_bet)
        self.current_chips += chips_won_this_round

    def cleanup(self):
        '''used to reset values. Not doing so to these values would give inaccurate results.'''
        self.dice.dice_roll_results = []
        self.current_bet = 0
        self.spaces_bet_on = []

        if self.bets_per_round == 0:
            self.bets_per_round = self.bets_placed
        self.bets_placed = 0

    def autoplay_game(self):
        '''play the game in a while loop, until the target simulations are reached OR until we don't have enough chips to wager. whichever comes first'''
        while(self.current_round + 1 <= self.rounds_to_simulate) and not self.end_simulation:
            self.current_round += 1
            #print(f"current round: {self.current_round}")
            
            # Place our bets
            self.place_bet()
            
            # Roll the dice
            self.dice.roll_dice()

            # If we win, payout
            if self.did_win():
                # Payout
                self.payout()
                self.wins += 1
            else:
                self.losses += 1
                self.chips_lost += self.current_bet

            # cleanup needed values
            self.cleanup()

        # if the simulation didn't stop naturally, show a message describing that.
        #if self.end_simulation:
            #print("Simulation ended abruptly, because you don't have enough chips to continue\n")

betters_made_profit = 0
num_betters_simulated = 0
made_profit = []
profit_percent_target = 10
print("Simulation running, please wait.")
while betters_made_profit != 1000:
    # randomly assign betters some chips
    chips = 10000 #random.randint(1000000,10000000)

    # Settings to simulate
    game = Game(bet_per_space=5, starting_chips=chips, rounds_to_simulate=2000, bet_on_trips=True)

    # Start simulating rounds
    game.autoplay_game()

    if round(((game.current_chips - chips) / chips) * 100, 2) >= profit_percent_target:
        stats = {"starting_chips":chips, "ending_chips":round(game.current_chips), "bet_per_space":5, "num_spaces_bet_on":game.bets_placed, "wager_per_round":game.wager_per_round, "profit_percent":round(((game.current_chips - chips) / chips) * 100, 2)}
        betters_made_profit += 1
        print(betters_made_profit)

        made_profit.append(stats)
    num_betters_simulated += 1

for winner in made_profit:
    print(winner)

# Show results
print("\tBETTOR DATA")
print("Total Bettors Played:", num_betters_simulated)
print("Total Bettors Profited:",(betters_made_profit))
print("Total Bettors Loss:",(num_betters_simulated - betters_made_profit))
print("\n\tSIMULATION SETTINGS\t")
print("Simulated Rounds Target:", game.rounds_to_simulate)
print("Simulated Rounds Completed:", game.current_round)
print("Betting on 4-9 & 12-17:", game.bet_on_sides)
print("Betting on Red & Black:", game.bet_on_red_black)
print("Betting on Trips:", game.bet_on_trips)
print("Betting on Odd & Even:", game.bet_on_odd_even)
print("Betting on Keystone:", game.bet_on_keystone)
print("Betting on Pair:", game.bet_on_pair)
print("Betting on Run:", game.bet_on_run)
print("\n\tBETTING DATA")
print("Bet:",game.min_bet)
print("Bets placed per round:", game.bets_per_round)
print("Wager per Round:", game.wager_per_round)
print("\n\tCHIPS DATA")
print("Starting Chips:", game.starting_chips)
print("Ending Chips:", game.current_chips)
print("Chip Difference",(game.current_chips - game.starting_chips))
print("Total Chips Won:", game.chips_won)
print("Total Chips Lost:", game.chips_lost)
print("\n\tROUND DATA")
print("Rounds Won:", game.wins)
print("Rounds Loss:", game.losses)
print("\n\tPERCENTAGE DATA")
print("Win Percent:", f"{round(((game.wins * 100) / game.current_round), 2)}%")
print("Loss Percent:", f"{round(((game.losses * 100) / game.current_round), 2)}%")
