# Brandon Chan  
# chanbz@uci.edu
# 12383908
import global_items as g
from pathlib import Path
import input_processor as ip
import user_interface_messages as ui

def input_terminal(): 
        '''Takes user-input and delegates it accordingly'''
        print("Welcome.")
        ui.command_list()
        user_input = input()
        # If the user types in 'Q', quit the program
        while user_input != "Q":
                print()
                is_valid = ip.cmd_checker(user_input)
                if is_valid:
                        ip.cmd_processor(user_input)
                        ui.command_list()
                        user_input = input()
                else:
                        error()
                        ui.command_list()
                        user_input = input()
                        

def main():
        input_terminal()


def error():
        '''Prints 'ERROR'''
        print('ERROR')
    
if __name__ == "__main__":
        main()
