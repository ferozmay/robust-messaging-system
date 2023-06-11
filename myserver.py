import sys
import re
from ex2utils import Server


class MyServer(Server):

    def onStart(self):
        print("My server has started")
        self.client_count = 0
        self.users = {}

    def onStop(self):
        print("My server has stopped.")

    def onConnect(self, socket):
        self.client_count += 1
        print("A client has connected")
        print(f"Currently active clients: {self.client_count}")

        socket.screenName = ""
        socket.set = False

        socket.send("Welcome".encode())

    def onMessage(self, socket, message):
        # print("Message received from client.")

        (command, sep, parameter) = message.strip().partition(' ')

        if command == "name":
            # set client's name
            new_name = parameter

            # validate name
            pattern = re.compile(r'^\w{3,20}$')
            if bool(pattern.match(new_name)) != True:
                print("Client entered an invalid screen name")
                socket.send(
                    "INVALID_NAME: - Name must contain only letters, numbers and underscores. - Name must be 3-20 characters".encode())
                return True

            else:

                if new_name in self.users:
                    print("Client tried to choose a name which is already registered")
                    if socket.screenName == new_name:
                        socket.send(
                            b"CURRENT_NAME: You're name is already registered.")
                    else:
                        socket.send(
                            b"NAME_TAKEN: Screen name already taken! Please choose a different one.")
                else:

                    if socket.screenName:
                        del self.users[socket.screenName]
                        print(
                            f"'{socket.screenName}' renamed themselves to '{new_name}'")

                    socket.screenName = new_name
                    self.users[new_name] = socket
                    socket.set = True
                    socket.send(
                        f"NAME_REGISTERED: '{new_name}' registered!".encode())

        elif command == "sendall":
            if socket.set == True:

                # check for blank message
                if parameter.strip() == "":
                    socket.send(b"EMPTY: Message cannot be blank")

                else:
                    # Send message to all connected users
                    for user_socket in self.users.values():
                        if user_socket != socket:
                            message = f"{socket.screenName}: {parameter}".encode()
                            user_socket.send(message)
                    print(
                        f"'{socket.screenName}' sent a message to all active users")
            else:
                socket.send(
                    b"DENIED: Command restricted, please identify yourself first.")

        elif command == "sendto":
            if socket.set == True:
                # Send message to a specific user
                (recipient, sep, msg) = parameter.strip().partition(' ')
                if recipient not in self.users:
                    socket.send(b"Error: User not found. \n")
                    print(
                        f"'{socket.screenName}' tried to send a message to an unknown user")

                elif msg == "":
                    socket.send("EMPTY: Empty message".encode())

                else:
                    message = f"{socket.screenName}: {msg}".encode()
                    self.users[recipient].send(message)
                    print(
                        f"'{socket.screenName}' sent a message to '{recipient}'")
            else:
                socket.send(
                    b"DENIED: Command restricted, please identify yourself first.")

        elif command == "list":
            # Return a list of connected users
            user_list = f"Connected users: {len(self.users)} active client(s)!\n"
            for user in self.users:
                if user == socket.screenName:
                    x = f" - {user} (you)\n"
                    user_list += x
                else:
                    user_list += f" - {user}\n"

            user_list = user_list.encode()
            socket.send(user_list)

        elif command == "quit":
            print("Client requested to disconnect")
            print("Client closed connection")
            socket.send(b"DISCONNECTED: disconnection approved")

        elif command == "help":
            socket.send(b"HELP")

        elif command == "hello":
            print("hello world")

        else:
            print(f"Client tried invalid command: '{message}'")
            socket.send(f"Error: Invalid command '{command}'".encode())

        return True

    def onDisconnect(self, socket):
        self.client_count -= 1

        # Remove user from dictionary
        if self.users.pop(socket.screenName, None):
            print(f"'{socket.screenName}' has disconnected.")

        else:
            print("Unnamed client has disconnected.")

        socket.close()
        print(f"Currently active clients: {self.client_count}")


# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create my server
server = MyServer()

# Start server
server.start(ip, port)
