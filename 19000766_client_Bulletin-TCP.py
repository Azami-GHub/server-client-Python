#!/usr/bin/env python3
# Sys for error handling and taking parameters from command line
import sys
import json

from socket import *


def send_to_server(message):
    server_name = '192.168.0.115'
    server_port = 12000
    clientsocket = socket(AF_INET, SOCK_STREAM)
    # Set a timeout of 10 seconds for all requests
    clientsocket.settimeout(10)
    clientsocket.connect((server_name, server_port))
    # Convert the message to a JSON string
    message = json.dumps(message)
    # Send the message
    clientsocket.send(message.encode())
    # Get the whole response
    receive = clientsocket.recv(1024).decode()
    total_response = ""
    while receive:
        total_response = total_response + receive
        receive = clientsocket.recv(1024).decode()
    # Convert into a python dictionary
    total_response = json.loads(total_response)
    clientsocket.close()
    return total_response


def get_messages(board):
    message = {"command": "GET_MESSAGES", "board": board}
    response_get_messages = send_to_server(message)
    if response_get_messages["error"] != "none":
        print(response_get_messages["error"])
        return
    response_get_messages = response_get_messages["messages"]
    if response_get_messages == {}:
        print("There are no messages in this board")
    else:
        for title, message in response_get_messages.items():
            print("Title:" + title + " Message:" + message)


def post_message(board_number, title, content):
    sentence = {
        "command": "POST_MESSAGE",
        "board": board_number,
        "title": title,
        "content": content,
    }
    response = send_to_server(sentence)
    if response["error"] != "none":
        print(response["error"])


def quit_all():
    message = {"command": "QUIT"}
    response = send_to_server(message)
    if response["error"] == "none":
        sys.exit()

print("----------THONNY BULLETIN BOARD----------")
print("(No.) Indicates board number")
boards_request = {"command": "GET_BOARDS"}

get_boards = send_to_server(boards_request)
if get_boards["error"] != "none":
    print(get_boards["error"])
    sys.exit()

for counter, value in enumerate(get_boards["boards"]):
    print(str(counter + 1) + "." + str(value))

print("Please enter User ID and Password for registered user")
print("*for unregistered user may skip this section by pressing enter")



def main():
    global get_boards
    # Take the input from the user
    match_both = False
    match_one = False
    userID = input("UserID: ")
    userPassword = input("Password: ")
    for line in open("user-data.txt", "r").readlines():
        login_info = line.replace("\n", "").split(";")
        txt_userID = login_info[0]
        txt_userPassword = login_info[1]
        if userID == txt_userID and userPassword == txt_userPassword:
            match_both = True
            break
            
            
                

        elif userID != txt_userID and userPassword == txt_userPassword:
            match_one = True
            
        
        
        elif userID == txt_userID and userPassword != txt_userPassword:
            match_one = True
            
     
    if match_both:
        print("Active ID :",userID," ","User status :","Registered user")
        print("")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("")
        print("Enter the following command upon continuation to use Thonny Bulletin Board")
        print("(No.) = to read news in Thonny Bulletin Board based on board numbers")
        print("POST = to publish news in Thonny Bulletin Board(only for registered user)")
        print("QUIT = to stop the program")
        command = input("What do you want to do? : ")
        # If the command is a number and is from the list
        if command.isdigit():
            if 1 <= int(command) <= len(get_boards["boards"]):
                get_messages(get_boards["boards"][int(command) - 1])
            else:
                print("The specified board does not exist")
        elif command == "POST":
            board_number = input("What board number do you want to post to?")
            title = input("What is the title of your message?")
            content = input("What is the content of your message?")
            post_message(board_number, title, content)
        elif command == "QUIT":
            quit_all()
        else:
            print("Not a command")
    elif match_one:
        print("Active :",userID," ","User status :","Not a registered user")
        print("")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("")
        print("Enter the following command upon continuation to use Thonny Bulletin Board")
        print("(No.) = to read news in Thonny Bulletin Board based on board numbers")
        print("POST = to publish news in Thonny Bulletin Board(only for registered user)")
        print("QUIT = to stop the program")
        command = input("What do you want to do? : ")
        # If the command is a number and is from the list
        if command.isdigit():
            if 1 <= int(command) <= len(get_boards["boards"]):
                get_messages(get_boards["boards"][int(command) - 1])
            else:
                print("The specified board does not exist")
        elif command == "POST":
            print("Error, only registered user can post message in bulletin board")
        elif command == "QUIT":
            quit_all()
        else:
            print("Not a command")
    else:
        print("Active :",userID," ","User status :","Not a registered user")
        print("")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("")
        print("Enter the following command upon continuation to use Thonny Bulletin Board")
        print("(No.) = to read news in Thonny Bulletin Board based on board numbers")
        print("POST = to publish news in Thonny Bulletin Board(only for registered user)")
        print("QUIT = to stop the program")
        command = input("What do you want to do? : ")
        # If the command is a number and is from the list
        if command.isdigit():
            if 1 <= int(command) <= len(get_boards["boards"]):
                get_messages(get_boards["boards"][int(command) - 1])
            else:
                print("The specified board does not exist")
        elif command == "POST":
            print("Error, only registered user can post message in bulletin board")
        elif command == "QUIT":
            quit_all()
        else:
            print("Not a command")
            
        
    
        
        
        
        
        
        

while True:
    
    main()