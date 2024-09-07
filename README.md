![user_wizard](https://github.com/user-attachments/assets/9865f0d0-c7dc-44fe-bfef-56c26b06a597)
### User Wizard Script
This is a command-line utility that facilitates the creation of user accounts on a Unix-like system. The script is designed for administrators and utilizes the subprocess module to make system calls for user management. Here's a breakdown of what the script does:


1. It loads environment variables from a `.env` file and sets up `logging` using `Python's built-in logging module`.
2. It defines a function to `send a message to WhatsApp` using the WhatsApp `GREEN API`.
3. The script allows the creation of `standard` user accounts and `superadmin` accounts, with `validation` for usernames and passwords.
4. It organizes users into specific directories (`students` and `administrators`) within a designated `base` directory.
5. It `logs activities` and `errors` to a specified log file, making it easier to audit the actions performed by the script.
6. It `sends notifications` to a `specified` WhatsApp chat upon `successful user creation` using an external API, enhancing real-time communication capabilities.
7. It retrieves `sensitive information` like `WhatsApp API token` and `chat ID` from environment variables, promoting `secure coding practices`.
8. The script includes checks for `valid usernames` and `passwords` to enforce `security best practices`.

The script loops indefinitely, until user ends it.

![user_wizard](https://github.com/user-attachments/assets/5fbe503d-d60b-466a-a9d0-889dedd6aaf0)

### Installing `python3` and its required packages `requests` and `dotenv`

`sudo apt update`

`sudo apt install python3`

`sudo apt install python3-pip`

`pip3 install requests python-dotenv`  

