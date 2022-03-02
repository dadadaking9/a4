# Brandon Chan
# chanbz@uci.edu
# 12383908
import pathlib
import global_items as g
from pathlib import Path
import commands as c
import user_interface_messages

def cmd_checker(user_input)-> bool:
        '''Checks whether the user-entered command is one that the program can process'''
        commands = ['L ', 'C ', 'D ', 'R ', 'O ', 'E ', 'P ', 'S '] # Q, rather than a command, is set up as a program quitter.
        if user_input == 'admin': # Edge Case
                return True

        user_cmd = user_input[0:2]
        cmd_exists = user_cmd in commands
        valid_extension = True

        if len(user_input) < 1: # Empty Input
                return False
        if user_cmd == 'L ':
                l_valid_extensions = [' -r', ' -f']
                l_additional_input = [' -s', ' -e'] 
                l_user_extensions = []
                l_path_exists = True
                counter = 0
                # Process the string 2 characters at a time. After processing the 2 characters, forget about those 2 characters in the string.
                for character in user_input: 
                        remaining_input = user_input[counter:]
                        # if there's a ' -', recognize it as an attempted extension.
                        if (character == '-') and (user_input[counter - 1] == ' '): 
                                l_user_extensions.append(' ' + remaining_input[0:2])
                        counter += 1

                # For every extension detected in the user-input, check if it's an extension that the program supports        
                for extension in l_user_extensions:
                        if not ((extension in l_valid_extensions) or (extension in l_additional_input)):
                                valid_extension = False
                        if extension in l_additional_input:
                                try:
                                        if len(user_input[(user_input.index(extension) + 4):]) < 1: # both -s and -e require additional input. If none, invalid command. Try/except catches index out of bounds.
                                                valid_extension = False
                                except:
                                        valid_extension = False
                if len(l_user_extensions) < 1:
                        p = pathlib.Path(user_input[2:])
                        l_path_exists = p.exists()
                else:
                        p = pathlib.Path(user_input[2:(user_input.find(l_user_extensions[0]))])
                        l_path_exists = p.exists()
                return cmd_exists and valid_extension and l_path_exists
        elif user_cmd == 'E ':
                if g.accessed_file == None:
                        error()
                        return False
                e_valid_extensions = [' -usr', ' -pwd', ' -bio', ' -addpost', ' -delpost']
                e_user_extensions = []
                counter = 0
                for character in user_input:
                        remaining_input = user_input[counter:]
                        if ((character == '-') and (user_input[counter - 1]) == ' '):
                                e_user_extensions.append(' ' + remaining_input[0:remaining_input.index(' ')])
                        counter += 1

                for extension in e_user_extensions:
                        if not (extension in e_valid_extensions):
                                valid_extension = False
                
                
                if cmd_exists and valid_extension:
                        g.edit_requests = e_user_extensions
                        return True
                
                return False
        elif user_cmd == 'P ':
                p_valid_extensions = ['-usr', '-pwd', '-bio','-posts','-post','-all']
                p_user_extensions = user_input.split()
                p_user_extensions.remove("P")

                for extension in p_user_extensions:
                        if not (extension in p_valid_extensions):
                                valid_extension = False

                if cmd_exists and valid_extension:
                        g.print_requests = p_user_extensions
                        return True 

                return False 
        elif cmd_exists: # C, D, and R all have built-in error checking so doing it here is unneccessary
                return True
        else:
                return False

def cmd_processor(command):
        '''Processess the given command by delegating the request to the respective method'''
        primary_command = command[0:1] 
        if primary_command == 'L':
                if '-r' in command:
                        c.list_recursive(command)
                else:
                        c.list_iterative(command)
        elif primary_command == 'C':
                c.create_cmd(command)
        elif primary_command == 'D':
                c.delete_cmd(command)
        elif primary_command == 'R':
                c.read_cmd(command)
        elif primary_command == 'O':
                c.open_cmd(command)
        elif primary_command == 'E':
                c.edit_cmd(command)
        elif primary_command == 'P':
                c.print_cmd(command)
        elif primary_command == 'S':
                c.send_cmd(command)
        elif command == 'admin':
                g.admin = True

def error():
        '''Prints 'ERROR'''
        print('ERROR')
  