# Brandon Chan
# chanbz@uci.edu
# 12383908
import pathlib
import global_items as g
from pathlib import Path
import commands as c

tab = ' ' * 4
def command_list():
    '''Prints the list of commands the user can use'''
    if not g.admin:
        print('-~' * 20)
        print("Enter any of the following commands in the described format to continue.")
        print('"Q" - Quit the program')
        print('"L (path) -r/-f/-s/-e (additional info)" - Lists out a specified directory\'s contents based on the following mix (or lack thereof) of specifications')
        print(tab + "-r ~ Also lists/searches content of directories contained in the given directory path")
        print(tab + "-f ~ Output only files, excluding directories in the results")
        print(tab + "-s (name) ~ Output only files that match a given file name")
        print(tab + "-e (extension) ~ Output only files that match a given file suffix")
        print('"D (path)" - Deletes the file given that it has a .dsu suffix')
        print('"R (path)" - Reads the file given that it has a .dsu suffix')
        print('"C (path) -n (file name)" - Creates a .dsu file of the given name at the given path. Automatically opens the file for commands E and P')
        print('"O (path)" - Opens a file given that it is a .dsu file. Unlocks commands E and P')
        if g.accessed_file != None:
            print('"E -usr/-pwd/-bio/-addpost/-delpost (additional info)" - Edits an open file\'s respective property as shown below')
            print(tab + "-usr (input) ~ Replaces username of profile with given input")
            print(tab + "-pwd (input) ~ Replaces password of profile with given input")
            print(tab + "-bio (input) ~ Replaces biography of profile with given input")
            print(tab + "-addpost (input) ~ Adds a post with the given input as an entry")
            print(tab*2 + 'Avaliable Keywords: @weather, @lastfm')
            print(tab + "-delpost (index) ~ Deletes a post from a profile given the post's index")
            print('"P" -usr/-pwd/-bio/-posts/-post(index)/-all - Prints the listed item(s). Seperate requests by a space')
        print('-~' * 20)