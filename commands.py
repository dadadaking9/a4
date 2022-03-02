# Brandon Chan
# chanbz@uci.edu
# 12383908
import pathlib
import global_items as g
from pathlib import Path
import Profile as p
import user_interface_messages
import ds_client
from LastFM import LastFM
from OpenWeather import OpenWeather

def list_iterative(command):
        '''Runs the list command along with user-specifications iteratively'''
        file_l = []
        directory_l = []
        path_input = ''

        possible_extensions = [' -f',' -s',' -e']
        has_extension = False
        the_extension = ''
        
        for extension in possible_extensions:
                if extension in command:
                        the_extension = extension
                        has_extension = True
        
        if has_extension:
                path_input = command[2:command.index(the_extension)]
        else:
                path_input = command[2:]

        data_folder = pathlib.Path(path_input)

        for file_obj in data_folder.iterdir():
                if file_obj.is_file():
                        file_l.append(file_obj)
                elif file_obj.is_dir():
                        directory_l.append(file_obj)

        for file in file_l:
                if the_extension == '' or the_extension == ' -f':
                        print(file)
                elif the_extension == ' -s':
                        if str(file.name) == command[command.index(' -s ') + 4:]:
                                print(file)
                elif the_extension == ' -e':
                        if file.suffix == '.' + str(command[command.index(' -e ' + 4):]):
                                print(file)

        for directory in directory_l:
                if not (the_extension == ' -f'):
                        if not (the_extension == ' -s'):
                                print(directory)
                        else:
                                if directory.name == command[command.index(' -s ') + 4:]:
                                        print(directory)

def list_recursive(command):
        '''Runs the list command along with user-specifications recursively. Looks into directories in the specified path for more
        files if they exist.'''
        starting_location = pathlib.Path(command[2:command.index(' -r')])
        list_recursive_helper(command, starting_location)
                         
def list_recursive_helper(command, location): 
        '''Helper method for list_recursive.'''
        file_l = []
        directory_l = []

        for item in location.iterdir():
                if item.is_file():
                        file_l.append(item)
                elif item.is_dir():
                        directory_l.append(item)

        for f in file_l:
                if ' -s ' in command: 
                        if command[(command.index(' -s ') + 4):] == f.name:
                                print(f)
                elif ' -e ' in command:
                        if command[(command.index(' -e ') + 4):] == f.suffix[1:]: #[1:] is to skip the . in the file's suffix
                                print(f)
                else:
                        print(f)
                                
        for directory in directory_l:
                if not ((' -f' in command) or (' -s' in command) or (' -e' in command)):
                        print(directory)
                elif ' -s ' in command:
                        if command[(command.index(' -s ') + 4):] == directory.name:
                                print(directory)
                list_recursive_helper(command, directory)
                        
def create_cmd(command):
        '''Create a new user-named file in a user-specified directory. Collects and stores username, password and potentially
        a biography regarding the user'''
        try:
                name_index = command.index(' -n ')
                file_name = command[name_index + 4:]
                specified_dir = command[2:name_index]
                item = pathlib.Path(specified_dir)
                new_item = file_name + '.dsu'
                item.joinpath(new_item).touch(exist_ok = False)
                print("Created new item at the following location: ", item.joinpath(new_item))
                # The following process is coded in this way (rather than taking a direct input) because usernames and passwords are
                # required. If they weren't required, this could all be replaced with much less code.
                uname = ''
                while len(uname) < 1:
                    uname = input("Enter your mandatory desired username (Must be 1 or more characters): ")
                pword = ''
                while len(pword) < 1:
                    pword = input("Enter your mandatory desired password: (Must be 1 or more characters): ")
                
                biography = input("Enter your optional desired biography: ")

                new_user = p.Profile(username=uname, password=pword)
                new_user.bio = biography
                print("~-~" * 15)
                print("Your username:", new_user.username)
                print("Your password:", new_user.password)
                print("Your biography:", new_user.bio)
                print()
                new_user.save_profile(item.joinpath(new_item))

                open_pass_string = "O " + command[2:name_index] + "\\" + file_name + ".dsu"
                g.accessed_file_path = command[2:name_index] + "\\" + file_name + ".dsu"
                open_cmd(open_pass_string)

        except:
                error()

def delete_cmd(command):
        '''Deletes a specified DSU file. Errors if file specified is
        not a DSU file.'''
        try:
                del_item = pathlib.Path(command[2:])
                if del_item.suffix == '.dsu':
                        del_item.unlink(missing_ok = False)
                        print (str(del_item) + ' DELETED')
                else:
                        error()
        except:
                error()

def read_cmd(command):
        '''Attempts to read the user-specified file. If empty, prints "EMPTY". '''
        try:
                read_item = pathlib.Path(command[2:])
                if read_item.suffix == '.dsu':
                        if read_item.stat().st_size == 0:
                                print('EMPTY') 
                        else:
                                try:
                                        read_item.open('r')
                                        print(read_item.read_text(),end='')
                                except:
                                        error()
                else:
                        error()
        except:
                error()
        print()

def open_cmd(command):
    '''Opens an existing .dsu file to be modified'''
    current_file = p.Profile()
    current_file.load_profile(command[2:])
    g.accessed_file = current_file
    g.accessed_file_path = command[2:]
    print("Successfully loaded into user", current_file.username)

def edit_cmd(command): # Fix 3+ combo
   '''Given a file has been accessed (via open/edit), prompts the user to modify the noted properties'''  
   counter = 2
   edited_properties = {"-usr": g.accessed_file.username, "-pwd": g.accessed_file.password, "-bio" : g.accessed_file.bio, "-addpost" : None, "-delpost" : None}
   for character in command: #Not optimized / correct, fix
        remaining_input = command[counter:]
        if len(g.edit_requests) > 1:
                edited_properties[remaining_input[0:remaining_input.index(' ', 2)]] = remaining_input[remaining_input.index(' ', 2) + 1:remaining_input.index(' -')] # Given there's more requests
                counter = remaining_input.index(' -') + 2
        else: # If there is 1
                #Problem, remain_input.index(' ') will return 0 since the very first value in the properties is 
                # print("remaining input: " + remaining_input)
                edited_properties[remaining_input[0:remaining_input.index(' ', 2)]] = remaining_input[remaining_input.index(' ') + 1:] # Given this is the last request in the command
                break # to stop an overflow on the counter
        counter += 1
       
   g.accessed_file.username = edited_properties["-usr"]
   g.accessed_file.password = edited_properties["-pwd"]
   g.accessed_file.bio = edited_properties["-bio"]

   if not (edited_properties["-addpost"] == None):
       # try:
        message_to_post = edited_properties['-addpost']
        defaultFM = LastFM()
        defaultFM.load_data()
        message_to_post = defaultFM.transclude(message_to_post) #Both of these need to be objects, not the base class
        print(message_to_post)

        defaultWeather = OpenWeather()
        defaultWeather.load_data()
        message_to_post = defaultWeather.transclude(message_to_post)
        print(message_to_post)

        print()
        g.accessed_file.add_post(p.Post(message_to_post))
        onlinep = input('Post Online? Y for yes, anything else for No')
        if onlinep == 'Y':
                users_posts = g.accessed_file.get_posts()

                ds_client.send('168.235.86.101', 3021, g.accessed_file.username, g.accessed_file.password, users_posts[len(users_posts) - 1])
                #ds_client.send('168.235.86.101', 3021, g.accessed_file.username, g.accessed_file.password, passed_post, g.accessed_file.bio)
       # except:
                error()


   if not (edited_properties["-delpost"]) == None:
        g.accessed_file.del_post(int(edited_properties["-delpost"])) #Check if ' -delpost- is actually an int
   g.accessed_file.save_profile(g.accessed_file_path)

def print_cmd(command):
        '''Given a file has been accessed (via open/edit), prints the user specified properties'''
        try:
                if '-usr' in command:
                        print("User's username: " + g.accessed_file.username)
                
                if '-pwd' in command:
                        print("User's password: " + g.accessed_file.password)

                if '-bio' in command:
                        print("User's biography: " + g.accessed_file.bio)
                
                if '-posts' in command:
                        print("User's posts: ")
                        for post in g.accessed_file.get_posts():
                                print(post)
                
                if '-post' in command:
                        users_posts = g.accessed_file.get_posts()
                        print("User's Post: " + users_posts[command.index('-post ') + 7])

                if '-all' in command:
                        users_posts = g.accessed_file.get_posts()
                        print("User's username: " + g.accessed_file.username)
                        print("User's password: " + g.accessed_file.password)
                        print("User's biography: " + g.accessed_file.bio)
                        print("User's posts: ")
                        for post in g.accessed_file.get_posts():
                                print(post)
        except:
                error()
           
def send_cmd(command):
        '''Given the index of the post of the open file, send the post in to the website'''
        #server:str, port:int, username:str, password:str, message:str, bio:str=None)
        # Add a try here
        users_posts = g.accessed_file.get_posts()
        passed_post = ' '

        if len(users_posts) <= int(command[2]): #If the requested post doesn't exist, pass empty string
                passed_post = ' '
        else:
                passed_post = users_posts[int(command[2])] # Otherwise, pass the indicated post
        ds_client.send('168.235.86.101', 3021, g.accessed_file.username, g.accessed_file.password, passed_post, g.accessed_file.bio)
        # Add an except here


def error():
        '''Prints 'ERROR'''
        print('ERROR')
        
