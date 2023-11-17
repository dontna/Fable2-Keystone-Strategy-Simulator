# Fable2-Keystone-Strategy-Simulator
A Python script which simulates multiple betting strategies, in Fable 2's Keystone.

# Why was this made?
I recently started playing Fable 2 again on the Xbox 360. I was trying to farm gold and after looking online most users say you can win lots by playing the betting game Keystone. Everyone seems to have their own "winning system" to "beat" the game, however it didn't seem right to me. So I created this script to put their bettings strategies to the test.

# How to use?
To configure the script, open it up and find the line 
`game = Game(bet_per_space=5, starting_chips=chips, rounds_to_simulate=2000, bet_on_trips=True)` (it should be on line 254)

From here you can change / add the following options:

**bet_per_space** - The number of chips to simulate per space. [Default: 5]

**stating_chips** - The number of total chips to start with. [Default:800]

**bet_on_trips** - Set the betting strategy to only bet on all triples and the Trips space. [Default: False]

**bet_on_sides** - Set the betting strategy to bet on 4-9 and 12 - 17. [Default: False]

**bet_on_red_black** - Set the betting strategy to bet on both Red and Black. [Default: False]

**bet_on_pair** - Set the betting strategy to bet on the dice having two matching numbers. [Default: False]

**bet_on_keystone** - Set the betting strategy to bet on both 10 and 11. [Default: False]

**bet_on_odd_even** - Set the betting strategy to bet on both odd and even. [Default: False]

**rounds_to_simulate** - Number of rounds to simulate. [Default: 100]


# Problems
This script is accurate enough for my point, however doesn't include the feature of betting on the outer rim of the Keystone board.

This script also doesn't use any sort of multithreading, so depending on how many rounds their are; it can take a while. I couldn't figure out how to change the script to use multithreading, but I'm sure someone else can!

This could also have other issues with the way it simulates, however nothing I have been able to find myself. So please let me know if it does!
