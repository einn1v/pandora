import os
import sys
import shutil
import json
import time
import random
import string
import colorama
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as ccp

# Utility

color = colorama.Fore
reset = color.RESET
blue = color.BLUE
lightblue = color.LIGHTBLUE_EX
cyan = color.CYAN
lightcyan = color.LIGHTCYAN_EX
red = color.RED
lightred = color.LIGHTRED_EX
green = color.GREEN
lightgreen = color.LIGHTGREEN_EX

default_hash = b"This is the default verification hash, you should change it for +500 opsec points."

banner = f"""{blue}
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                                                                         │
│   {blue} ██████╗ {lightblue}  █████╗ {cyan} ███╗   ██╗{lightcyan} ██████╗ {cyan}  ██████╗ {lightblue} ██████╗ {blue}  █████╗     │
│   {blue} ██╔══██╗{lightblue} ██╔══██╗{cyan} ████╗  ██║{lightcyan} ██╔══██╗{cyan} ██╔═══██╗{lightblue} ██╔══██╗{blue} ██╔══██╗    │
│   {blue} ██████╔╝{lightblue} ███████║{cyan} ██╔██╗ ██║{lightcyan} ██║  ██║{cyan} ██║   ██║{lightblue} ██████╔╝{blue} ███████║    │
│   {blue} ██╔═══╝ {lightblue} ██╔══██║{cyan} ██║╚██╗██║{lightcyan} ██║  ██║{cyan} ██║   ██║{lightblue} ██╔══██╗{blue} ██╔══██║    │
│   {blue} ██║     {lightblue} ██║  ██║{cyan} ██║ ╚████║{lightcyan} ██████╔╝{cyan} ╚██████╔╝{lightblue} ██║  ██║{blue} ██║  ██║    │
│   {blue} ╚═╝     {lightblue} ╚═╝  ╚═╝{cyan} ╚═╝  ╚═══╝{lightcyan} ╚═════╝ {cyan}  ╚═════╝ {lightblue} ╚═╝  ╚═╝{blue} ╚═╝  ╚═╝    │
│                         {lightcyan}v1.0.0 {reset}── Made by {lightcyan}V{reset}                             {blue}│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┘
│"""

def is_linux():
    return os.name == 'posix'

# CLI managment

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    cls()
    print(banner)

def log(message):
    print(f"{blue}│{reset}  " + message)

def logf(message):
    print(f"{blue}├──{reset}" + message)

def logc(name, value):
    print(f"{blue}├──{reset} {lightblue}{name}")
    log(f"    {blue}└── > {reset}{value}")

def get_input():
    return input(f"{blue}│\n└─── ${reset} ").strip()

def yn():
    log(f"{lightblue}[{reset}y{cyan}/{reset}n{lightblue}]{reset}")

# File managment

if not is_linux():
    path = os.environ.get("APPDATA")
    if not path:
        os.makedirs("stored", exist_ok=True)
        path = "stored\\"
        directory = os.path.join(path)
    
    else:
        os.makedirs(os.path.join(path, "Pandora"), exist_ok=True)
        directory = os.path.join(path, "Pandora")

    if not os.path.exists(os.path.join(directory, "hash.json")):
        # with open(os.path.join(directory, "test.txt"), "w") as file:
        #     file.write("helloworld helloworld")
        #     print("new file made!")
        print("temp data!!!!") # Passwords should be able to be recovered without hash in future versions!!!
elif is_linux():
    path = "/usr/share"
    if not os.path.exists(os.path.join(path, "Pandora")):
        os.makedirs(os.path.join(path, "Pandora"), exist_ok=True)
        directory = os.path.join(path, "Pandora")
    else:
        directory = os.path.join(path, "Pandora")

# Key managment

def save_key(key):
    key = bytes.fromhex(key) if isinstance(key, str) else key

    with open(os.path.join(directory, "key.json"), "w") as file:
        json.dump({"key": key.hex()}, file)
    
def load_key():
    try:
        with open(os.path.join(directory, "key.json"), "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return None
            
            if "key" not in data:
                return None

            try:
                return bytes.fromhex(data["key"])
            except ValueError:
                return None
            
    except FileNotFoundError:
        return None
    
def verify_key(key):
    with open(os.path.join(directory, "hash.json"), "r") as file:
        data = json.load(file)
        if "hash" in data and "nonce" in data:
            encrypted_hash = bytes.fromhex(data["hash"])
            nonce = bytes.fromhex(data["nonce"])

            try:
                key = bytes.fromhex(key)
            except ValueError:
                return False

            try:
                hash = ccp(key).decrypt(nonce, encrypted_hash, None)
            except Exception:
                return False

            if hash == default_hash:
                return True
            else:
                return False
        else:
            return False

# Profile managment

def delete_filepath():
    cls()
    print(f"Deleting {directory}")
    print("You have 5 seconds to cancel this operation by pressing Ctrl + C.")
    time.sleep(5)
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            print(f"{lightgreen}SUCCESS{reset} Profile deleted successfully.")
            input()
            exit(0)
        except (Exception, KeyboardInterrupt) as e:
            print(f"{lightred}ERROR{reset} Something went wrong while deleting the profile.")
            input()
            exit(0)


def delete_profile():
    print_banner()
    log("You are about to delete your profile, this will delete aLl your passwords.")
    log("Do you want to continue?")
    yn()

    if get_input().lower() == "y":
        print_banner()
        log("Are you sure you want to delete your profile? This CANNOT be undone.")
        yn()

        if get_input().lower() == "y":
            delete_filepath()
        else:
            print_banner()
            log("Action cancelled.")
            get_input()
            menu()
    else:
        print_banner()
        log("Action cancelled.")
        get_input()
        menu()

# Password managment

def save_password(password, username=None, service=None):
    temp_path = os.path.join(directory, "passwords.json")
    nonce = os.urandom(12)

    try:
        encrypted_password = ccp(bytes.fromhex(key)).encrypt(nonce, password.encode(), None)
    except Exception as e:
        print_banner() # Left here, password cannot be encrypted, its currently trying to encrypt a str value which it cannot do, should make sure that its a byte value tomorrow
        log(f"{lightred}ERROR{reset} Unable to encrypt the password.")
        log(f"Error details: {e}")
        get_input()
        return

    if os.path.exists(os.path.join(temp_path)):
        with open(os.path.join(temp_path), "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    
    data.append({
        "service": service if service else None,
        "username": username if username else None,
        "password": encrypted_password.hex(),
        "nonce": nonce.hex()
    })

    with open(temp_path, "w") as file:
        json.dump(data, file) # No indent, it doesn't need to look pretty, only the machine is reading it

def log_passwords(showCount=True, expectContent=False):
    with open(os.path.join(directory, "passwords.json"), "r") as file:
        if not expectContent: # We want to prevent double error messages if the file is empty
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                log("No passwords stored yet. You can create them from the menu.")
                return
        else:
            data = json.load(file)
        
        if showCount:
            if (len(data) - 1) == 0: logf(f" {lightblue}{len(data)} {reset}password found")
            else: logf(f" {lightblue}{len(data)} {reset}passwords found")
            log("")

        for item in data:
            i = data.index(item) + 1
            if item.get("service") is None:
                log(f"{lightblue}[{cyan}{i}{lightblue}] {reset}{item["username"]}")
            else:
                log(f"{lightblue}[{cyan}{i}{lightblue}] {reset}{item["service"]}")

def create_password():
    print_banner()

    log("What service is this password for? (optional)")
    service = get_input() or None
    print_banner()
    if service is not None:
        logf(f" Service {lightblue}>{reset} {service}")
    else:
        logf(f" Service {lightblue}>{reset} None")
    
    log("")
    if service is None:
        log("What username/email is this password for? (required)")
    else:
        log("What username/email is this password for? (optional)")
    
    username = get_input() or None

    print_banner()
    if service is not None:
        logf(f" Service {lightblue}>{reset} {service}")
    else:
        logf(f" Service {lightblue}>{reset} None")

    log("")

    if username is not None:
        if "@" in username:
            logf(f" Email {lightblue}>{reset} {username}")
        else:
            logf(f" Username {lightblue}>{reset} {username}")
    else:
        logf(f" Username/Email {lightblue}>{reset} None")
    
    log("")
    log("Enter the password. (Type 'RANDOM' to generate a random password.)")
    password = get_input()

    if password == 'RANDOM':
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(24,30)))
    
    print_banner()
    logf(f" Service {lightblue}>{reset} {service if service else 'None'}")
    log("")
    if username is not None:
        if "@" in username:
            logf(f" Email {lightblue}>{reset} {username}")
        else:
            logf(f" Username {lightblue}>{reset} {username}")
    else:
        logf(f" Username/Email {lightblue}>{reset} None")
    
    log("")
    logf(f" Password {lightblue}>{reset} {password}")

    if not service and not username:
        log("")
        log("Please provide either a service or a username/email for the password.")
        get_input()
        menu()
    else:
        log("")
        log("Are you sure you want to save this password?")
        yn()
        if get_input().lower() == "y":
            save_password(password, username, service)
            print_banner()
            log(f"{lightgreen}SUCCESS{reset} Password saved successfully.")
        else:
            print_banner()
            log("Password not saved.")
            get_input()
    
    get_input()
    menu()

def view_passwords():
    print_banner()

    def no_passwords():
        log("No passwords stored yet. You can create them from the menu.")
        get_input()
        menu()

    temp_path = os.path.join(directory, "passwords.json")

    if not os.path.exists(temp_path):
        with open(temp_path, "w") as file:
            file.close()

    with open(temp_path, "r") as file:
        try:
            data = json.load(file)
            if data == [{}] or data == []:
                no_passwords()
        except json.JSONDecodeError:
            no_passwords()

        log_passwords(True, True)

        log("")
        log("What password would you like to view?")

        choice = get_input()

        try:
            requested_index = int(choice) - 1
        except ValueError:
            if choice != "":
                log(f"{lightred}ERROR{reset} Invalid input, please enter a number.")
                get_input()
                view_passwords()
            else:
                menu()

        requested_item = data[requested_index]
        requested_password = bytes.fromhex(requested_item["password"])
        requested_nonce = bytes.fromhex(requested_item["nonce"])
        service = requested_item.get("service")
        username = requested_item.get("username")

        try:
            password = ccp(bytes.fromhex(key)).decrypt(requested_nonce, requested_password, None)
        except Exception:
            log(f"{lightred}ERROR{reset} Unable to decrypt the password, please check your key.")
            get_input()
            return

        print_banner()

        if service is None:
            if "@" in username:
                logc("Email", username)
                # log(f"{lightblue}[ {reset}Email {cyan}] {lightblue}> {reset}{username}")
            else:
                logc("Username", username)
                # log(f"{lightblue}[ {reset}Username {cyan}] {lightblue}> {reset}{username}")
        elif username is None:
            logc("Service", service)
        else:
            logc("Service", service)
            # log(f"{lightblue}[ {reset}Service {cyan}] {lightblue}  > {reset}{service}")
            log("")

            if "@" in username:
                logc("Email", username)
                # log(f"{lightblue}[ {reset}Email {cyan}] {lightblue} > {reset}{username}")
            else:
                logc("Username", username)
                # log(f"{lightblue}[ {reset}Username {cyan}] {lightblue} > {reset}{username}")
        
        log("")
        logc("Password", password.decode())
        # log(f"{lightblue}[ {reset}Password {cyan}] {lightblue} > {reset}{password.decode()}")

        get_input()
        menu()

def delete_password():
    print_banner()

    def no_passwords():
        log("No passwords stored yet. You can create them from the menu.")
        get_input()
        menu()

    temp_path = os.path.join(directory, "passwords.json")
    if not os.path.exists(temp_path):
        no_passwords()
    
    with open(temp_path, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            no_passwords()
        
        if not data:
            no_passwords()
        
        log_passwords(True, True)
        log("")
        log("What password would you like to delete?")

        choice = get_input()

        try:
            requested_index = int(choice) - 1
        except ValueError:
            menu()

        if requested_index < 0 or requested_index >= len(data):
            print_banner()
            log(f"{lightred}ERROR{reset} Invalid input, please enter a valid number.")
            get_input()
            delete_password()
        
        requested_service = data[requested_index]["service"]
        requested_username = data[requested_index].get("username")
        
        print_banner()
        log(f"You are about to delete the password for {lightblue}{requested_service if requested_service is not None else requested_username}{reset}. Are you sure you want to do this?")
        log("Type 'confirm' to continue, press Enter to cancel.")

        if get_input().lower() == 'confirm':
            del data[requested_index]
            with open(temp_path, "w") as file:
                json.dump(data, file)
            
            print_banner()
            log(f"{lightgreen}SUCCESS{reset} Password for {lightblue}{requested_service if requested_service is not None else requested_username}{reset} deleted successfully.")
            get_input()
            menu()
        else:
            print_banner()
            log("Action cancelled.")
            get_input()
            menu()


# Interface managment

def menu(cls = True):
    if cls:
        print_banner()
    else:
        if key:
            log(f"{lightgreen}[+] {reset}Key loaded successfully.")
            log("")

    log(f"{lightblue}[{cyan}1{lightblue}] {reset}View passwords")
    log(f"{lightblue}[{cyan}2{lightblue}] {reset}Add a password")

    try:
        with open(os.path.join(directory, "passwords.json"), "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            
            if data != [{}] and data != []:
                log(f"{lightblue}[{cyan}3{lightblue}] {reset}Delete a password")
    except FileNotFoundError:
        None
    if not load_key():
        log(f"{lightblue}[{cyan}4{lightblue}] {reset}Save key locally")
    log(f"{lightblue}[{cyan}0{lightblue}] {reset}Exit")

    match get_input():
        case "1":
            view_passwords()
        case "2":
            create_password()
        case "3":
            delete_password()
        case "4":
            if load_key() is None:
                save_key(key)
                print_banner()
                log("Key saved successfully.")
            else:
                print_banner()
                log("You already have a key saved.")

            get_input()
            menu()

        case "0":
            exit(0)
    

def main():
    global directory

    print_banner()

    # Checks for file system to setup directory
    if not is_linux():
        path = os.environ.get("APPDATA")

        if not os.path.exists(os.path.join(path, "Pandora")):

            if not path:
                os.makedirs("stored", exist_ok=True)
                path = "stored\\"
                directory = os.path.join(path)
            
            else:
                os.makedirs(os.path.join(path, "Pandora"), exist_ok=True)
                directory = os.path.join(path, "Pandora")

    # First time startup!!

    if not os.path.exists(os.path.join(directory, "hash.json")):
        log("This seems to be your first time running Pandora,")
        log("We will setup your profile now.")

        global key
        key = ccp.generate_key()

        with open(os.path.join(directory, "hash.json"), "w") as file:
            nonce = os.urandom(12)
            encrypted_hash = ccp(key).encrypt(nonce, default_hash, None)

            json.dump({
                "nonce": nonce.hex(),
                "hash": encrypted_hash.hex(),
            }, file)
            file.close()
        
        log("")
        logf(f" Key {lightblue}>{reset} {key.hex()}")
        log("")
        log("This is your encryption key, keep it somewhere safe and private.")
        log("This key will be used to view your passwords.")
        log("")
        log("Do you want to save the key locally?")
        log("Recommended for easier access, but less secure if the device is compromised.")
        yn()

        if get_input().lower() == "y":
            save_key(key)
        else:
            print_banner()
            log(f"{lightred}WARNING")
            log("Please note that if you don't save the key somewhere, you will not be able to access your passwords later.")
            log("")
            logf(f" Key {lightblue}>{reset} {key.hex()}")
            log("")
            log("If you've made sure that the key is saved, press Enter.")

            get_input()

    if load_key() is None:
        print_banner()
        log("You don't have a key saved, please enter your key to continue.")
        
        given_key = get_input()

        if verify_key(given_key):
            key = given_key
            log("Key verified successfully!")
        else:
            print_banner()
            key = None
            log(f"{lightred}ERROR")
            log("Key couldn't be verified, please try again later.")
            log("If you lost your key, you can delete your profile by typing 'DELETE'.")

            if get_input() == "DELETE":
                delete_profile()
    else:
        # print(type(load_key())) Debugging only
        if verify_key(load_key().hex()):
            key = load_key().hex()

    if key:
        print_banner()
        menu(False)

if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt):
        print(f"{reset}")
        sys.exit(0)
