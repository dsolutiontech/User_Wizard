import os
import re
import subprocess
import getpass
import logging
import socket
import requests
from dotenv import load_dotenv
# Function to print the User Wizard logo
def print_logo():
    print(r"""
 _____            _       _   _          _______        _
|  __ \          | |     | | (_)        |__   __|      | |
| |  | |___  ___ | |_   _| |_ _  ___  _ __ | | ___  ___| |__
| |  | / __|/ _ \| | | | | __| |/ _ \| '_ \| |/ _ \/ __| '_ '\
| |__| \__ \ (_) | | |_| | |_| | (_) | | | | |  __/ (__| | | |
|_____/|___/\___/|_|\__,_|\__|_|\___/|_| |_|_|\___|\___|_| |_|
                    +-+-+-+-+-+-+-+-+-+-+-+
                    |U|s|e|r|_|W|i|z|a|r|d|
                    +-+-+-+-+-+-+-+-+-+-+-+
""")

print_logo() # Print the User Wizard logo
# Configure logging to write logs to a file (default: user_creation.log) (adjust the path as needed)
logging.basicConfig(filename='/workspaces/python-development/python/User_Wizard/user_creation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger() # Get the logger
# Load environment variables
load_dotenv()
# Get the WhatsApp API token, chat ID, and instance ID from the environment variables
WHATSAPP_API_TOKEN = os.environ.get('WHATSAPP_API_TOKEN')
WHATSAPP_CHAT_ID = os.environ.get('WHATSAPP_CHAT_ID')
WHATSAPP_INSTANCE_ID = os.environ.get('WHATSAPP_INSTANCE_ID')
WHATSAPP_URL = f'https://7103.api.greenapi.com/waInstance{WHATSAPP_INSTANCE_ID}/sendMessage/{WHATSAPP_API_TOKEN}'
headers = {'Content-Type': 'application/json'}
# Function to send a message to WhatsApp
def send_message(message):
    data = {"chatId": WHATSAPP_CHAT_ID, "message": message}
    try: 
        response = requests.post(WHATSAPP_URL, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f'Message sent to {WHATSAPP_CHAT_ID}')
        else:
            logger.error(f'Failed to send message to {WHATSAPP_CHAT_ID}')
            logger.error(response.text)
    except Exception as e:
        logger.error(f'Error sending message: {str(e)}')
        
# Define the base directory and create the 'students' and 'administrators' directories
BASE_DIR = "/workspaces/python-development/python/User_Wizard" # Set the base directory (adjust the path as needed)
STUDENT_DIR = os.path.join(BASE_DIR, "students") 
ADMIN_DIR = os.path.join(BASE_DIR, "administrators")
# Create the 'students' and 'administrators' directories if they do not exist
os.makedirs(STUDENT_DIR, exist_ok=True)
os.makedirs(ADMIN_DIR, exist_ok=True)
# Function to check if the username is valid
def is_valid_username(username):
    return re.match("^[a-z0-9_]{3,20}$", username) is not None and not username.isdigit() # Return True if the username is valid, False otherwise (check for 3-20 characters containing lowercase letters, numbers, and underscores only)
# Function to check if the password is valid
def is_valid_password(password):
    return len(password) >= 8 # Return True if the password is at least 8 characters long, False otherwise (check for a minimum length of 8 characters)
# Function to check if the user exists
def user_exists(username):
    result = subprocess.run(['id', username], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return result.returncode == 0 # Return True if the user exists, False otherwise
# Function to create a new user
def create_user(username, password, user_type):
    home_dir = os.path.join(STUDENT_DIR if user_type == 'student' else ADMIN_DIR, username) # Set the home directory for the new user
    
    if user_type == 'student': # Check if the user type is 'student'
        command = ['sudo', 'useradd', '-m', '-d', home_dir, username] # Create a new user without sudo privileges
    else: # If the user type is 'admin'
        command = ['sudo', 'useradd', '-m', '-d', home_dir, '-G', 'sudo', username] # Create a new user with sudo privileges

    try: # Try to create the new user
        subprocess.run(command, check=True) # Run the command to create the new user
        subprocess.run(['sudo', 'chpasswd'], input=f"{username}:{password}".encode(), check=True) # Set the password for the new user
        logger.info(f"{user_type.capitalize()} '{username}' created successfully with home directory '{home_dir}'.")
        print(f"{user_type.capitalize()} '{username}' created successfully.")
        send_message(f"*{getpass.getuser()}* has created a new {'superuser' if user_type == 'admin' else 'user'} '{username}' on *{socket.gethostname()}*.") # Send a WhatsApp message
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating user '{username}': {e}")
        print(f"Error creating user '{username}': {e}")
        
# Main function to create a new user or superadmin
def main():
    current_username = getpass.getuser() # Get the current username

    while True: # Run the user creation loop
        # Print a welcome message and the options
        print(f"\nWelcome {current_username}, please select an option.") 
        print("1) Create a new user")
        print("2) Create a new superadmin") 
        print("3) Done") 
        choice = input("Enter your choice [1-3]: ").strip() # Get the user's choice
        
        if choice == '1': # Create a new user
            username = input("Enter (new user) username: ").strip() # Get the username for the new user
            
            if not is_valid_username(username): # Validate the username first
                logger.error(f"Invalid username provided: '{username}'.")
                print("Error: Username must be 3-20 characters containing lowercase letters, numbers, and underscores only.")
                continue # Continue to the next iteration of the loop

            if user_exists(username): # Check if the user already exists
                logger.info(f"User '{username}' already exists.") 
                print(f"Sorry, username: '{username}' already exists.")
                continue # Continue to the next iteration of the loop
    
            password = getpass.getpass(f"Enter password for '{username}': ") # Get the password for the new user
            if not is_valid_password(password): # Check if the password is valid
                logger.error(f"Weak password provided for user: {username}")
                print("Error: Password should be at least 8 characters.")
                continue # Continue to the next iteration of the loop
            
            create_user(username, password, 'student') # Create a new user
            
        elif choice == '2': # Create a new superadmin
            username = input("Enter (new superadmin) username: ").strip() # Get the username for the new superadmin
            
            if not is_valid_username(username): # Validate the username first
                logger.error(f"Invalid username provided: '{username}'.")
                print("Error: Username must be 3-20 characters containing lowercase 1letters, numbers, and underscores only.")
                continue # Continue to the next iteration of the loop

            if user_exists(username): # Check if the user already exists
                logger.info(f"User '{username}' already exists.") 
                print(f"Sorry, username '{username}' already exists.")
                continue # Continue to the next iteration of the loop
            
            password = getpass.getpass(f"Enter password for '{username}': ") # Get the password for the new superadmin
            if not is_valid_password(password): # Check if the password is valid
                logger.error(f"Weak password provided for user: {username}") 
                print("Error: Password should be at least 8 characters.")
                continue # Continue to the next iteration of the loop
            
            create_user(username, password, 'admin') # Create a new superadmin

        elif choice == '3': # Exit the script
            logger.info(f"Exiting the script. Goodbye!")
            print("Exiting the script. Goodbye!")
            break # Break out of the loop

        else: # Handle invalid choices
            logger.error(f"Invalid option selected: '{choice}'.") 
            print("Uh oh.. You have selected an invalid option.")
            
# Run the main function
if __name__ == "__main__":
    main()
