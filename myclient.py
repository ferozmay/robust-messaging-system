"""

IRC client exemplar.

How to run and test the code:

1. Install Python 3 (if not already installed).
2. Ensure that the 'ex2utils.py' file is in the same directory as this script.
3. Start the server that this client will connect to (refer to the server documentation for details).
4. Open a terminal/command prompt and navigate to the directory containing this script.
5. Run the script using the command: `python3 myclient.py localhost 8090`
6. Follow the on-screen prompts to register a screen name and interact with the server using the available commands.

Testing the functionality:

1. Register a screen name: Use the 'name' command followed by your desired screen name.
2. Send a private message to a specific user: Use the 'sendto' command followed by the recipient's screen name and your message.
3. Send a message to all connected users: Use the 'sendall' command followed by your message.
4. List all connected (active) users: Use the 'list' command. 
5. Display the list of available commands: Use the 'help' command.
6. Close the connection with the server: Use the 'quit' command.

Make sure to test various scenarios, such as 
    - using invalid screen names
    - sending messages to non-existent users
    - testing multiple clients connecting to the server simultaneously

Note: This client assumes that the server is running and ready to accept connections. 
If the server is down, the client will raise an OSError and print an error message.

"""

import sys
from ex2utils import Client


class IRCClient(Client):

    def __init__(self):
        super().__init__()
        self.set = False

    def onMessage(self, socket, message):
        # *** process incoming messages here ***
        cmd = '''
    The list of commands are given below:
        
            Usage                            Description

    name <your_name>                Set a screen name
    sendto <user> <message>         Send a message to a partiular user
    sendall <message>               Send a message to all users
    list                            List all connected (active) users
    help                            Display the list of available commands
    quit                            Close the connection with the server

            '''

        if message.startswith("Welcome"):
            welcome = '''Welcome!
    _________________________________________________________________
          __  __  __       __          __     __      __ ___  __      
    |\/| |_  (_  (_   /\  / _  | |\ | / _    (_  \_/ (_   |  |_  |\/| 
    |  | |__ __) __) /--\ \__) | | \| \__)   __)  |  __)  |  |__ |  | 
    _________________________________________________________________            

            '''
            print(welcome, cmd)

        if message.startswith("INVALID_NAME"):
            print(
                "\n- Name must contain only letters, numbers and underscores\n- Name must be 3-20 characters long")

        elif message.startswith("NAME_TAKEN"):
            print("\nScreen name is already taken. Please choose another one.")
        elif message.startswith("CURRENT_NAME"):
            print("\nThis is already registered as your current name")
        elif message.startswith("NAME_REGISTERED"):
            self.set = True
            print("\nScreen name successfully registered.")
        elif message.startswith("DISCONNECTED"):
            print("\nServer has received your request to disconnect")
        elif message.startswith("EMPTY"):
            print("\nCannot send a blank message!")
        elif message.startswith("HELP"):
            print(cmd)

        else:
            print(message)

        return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

# send message to the server
message = "hello world"
client.send(message.encode())

# Main loop to handle user input.
try:
    while client.isRunning():
        q = False
        while not client.set:
            intro = input(
                "\nPlease identify yourself using the 'name' command:\n> ")

            if intro.lower() == "quit":
                client.send(b"quit")
                q = True
                break

            client.send(intro.encode())

        if q:
            break

        user_input = input("\nEnter a command:\n> ")

        if user_input.lower() == "quit":
            client.send(b"quit")
            break
        else:
            client.send(user_input.encode())
except KeyboardInterrupt:
    client.send(b"quit")

except OSError:

    print("Error: Server down! Please check your server status.")


# stops client
client.stop()
