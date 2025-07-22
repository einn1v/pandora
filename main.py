# from cryptography.fernet import Fernet

# def generate_key():
#     key = Fernet.generate_key()
#     return key

# def generate_instance(key):
#     return Fernet(key)

# def encrypt_data(instance, data):
#     return instance.encrypt(data.encode())

# key = generate_key()

# print(f"Generated key: {key.decode()}")

# instance = generate_instance(key)

# print(instance)
# input_data = input("Enter test data >>")
# encrypted_data = encrypt_data(instance, input_data)
# print(f"Encrypted data: {encrypted_data.decode()}")

## SECOND TRY

# import os
# from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as ccp

# data = input("Enter test data >>").encode()

# key = ccp.generate_key()
# print(f"Generated key: {key.hex()}")

# instance = ccp(key)
# nonce = os.urandom(12)

# encrypted_data = instance.encrypt(nonce, data, None)
# print(f"Encrypted data: {encrypted_data.hex()}")

# data_to_decrypt = input("Enter data to decrypt >>").encode()
# key_to_try = input("Enter key to try (hex) >>").encode()
# try:
#     instance = ccp(bytes.fromhex(key_to_try.decode()))
#     decrypted_data = instance.decrypt(nonce, bytes.fromhex(data_to_decrypt.decode()), None)
#     print(f"Decrypted data: {decrypted_data.decode()}")
# except Exception as e:
#     print(f"Decryption failed: {e}")

import os
import shutil
import time
import json
import random
import string
import colorama as clr
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as ccp

color = clr.Fore
reset = color.RESET
white = color.WHITE
cyan = color.CYAN
lightcyan = color.LIGHTCYAN_EX
blue = color.BLUE
lightblue = color.LIGHTBLUE_EX

default_hash = b"This is the default verification hash, you should change it for +500 opsec points." # Default verification hash, not necessary to change but is recommended to prevent key bruteforcing when the /stored directory is compromised.

# CLI managment functions

def cls():
    os.system("cls" if os.name == "nt" else "clear")

title_binary = "01010000 01100001 01101110 01000100 01101111 01010010 01100001"

title = f"""{blue}
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                                                                         │
│   {blue} ██████╗ {lightblue}  █████╗ {cyan} ███╗   ██╗{lightcyan} ██████╗ {cyan}  ██████╗ {lightblue} ██████╗ {blue}  █████╗     │
│   {blue} ██╔══██╗{lightblue} ██╔══██╗{cyan} ████╗  ██║{lightcyan} ██╔══██╗{cyan} ██╔═══██╗{lightblue} ██╔══██╗{blue} ██╔══██╗    │
│   {blue} ██████╔╝{lightblue} ███████║{cyan} ██╔██╗ ██║{lightcyan} ██║  ██║{cyan} ██║   ██║{lightblue} ██████╔╝{blue} ███████║    │
│   {blue} ██╔═══╝ {lightblue} ██╔══██║{cyan} ██║╚██╗██║{lightcyan} ██║  ██║{cyan} ██║   ██║{lightblue} ██╔══██╗{blue} ██╔══██║    │
│   {blue} ██║     {lightblue} ██║  ██║{cyan} ██║ ╚████║{lightcyan} ██████╔╝{cyan} ╚██████╔╝{lightblue} ██║  ██║{blue} ██║  ██║    │
│   {blue} ╚═╝     {lightblue} ╚═╝  ╚═╝{cyan} ╚═╝  ╚═══╝{lightcyan} ╚═════╝ {cyan}  ╚═════╝ {lightblue} ╚═╝  ╚═╝{blue} ╚═╝  ╚═╝    │
│                         {lightcyan}v1.0.0 {white}── Made by {lightcyan}V{reset}                             {blue}│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┘
│"""
def print_banner():
    cls()
    print(title)

base_input = f"{blue}│\n└─── ${reset}"

def get_input():
    return input(f"{base_input} ").strip()

def log(message):
    print(f"{blue}│{reset}  " + message)

def logf(message):
    print(f"{blue}├──{reset}" + message)

# Key managment functions

def save_key(key):
    with open("stored/key.json", "w") as file:
        json.dump({"key": key.hex()}, file)

def get_stored_key():
    try:
        with open("stored/key.json", "r") as file:
            return json.load(file)["key"]
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
# File managment functions

def generate_hash(instance):
    unsecure_nonce = os.urandom(12) # It's unsecure because nonces should be private, but I can't be bothered to implement a solution for that.
    encrypted_hash = instance.encrypt(unsecure_nonce, default_hash, None)
    with open("stored/hash.json", "w") as file:
        json.dump({
            "hash": encrypted_hash.hex(),
            "nonce": unsecure_nonce.hex()
        }, file)

def save_password(key, password, username, service):
    instance = ccp(key)
    nonce = os.urandom(12)
    aad = service.lower().encode()
    encrypted_password = instance.encrypt(nonce, password.encode(), aad)

    if os.path.exists("stored/passwords.json"):
        with open("stored/passwords.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append({
            "service": service.lower(),
            "username": username,
            "nonce": nonce.hex(),
            "password": encrypted_password.hex()
        })

    with open("stored/passwords.json", "w") as file:
        json.dump(data, file)

# def retrieve_password(key, service):
#     instance = ccp(key)
#     try:
#         with open("stored/passwords.json", "r") as file:
#             data = json.load(file)
#             for entry in data:
#                 if entry["service"] == service.lower():
#                     nonce = bytes.fromhex(entry["nonce"])
#                     encrypted_password = bytes.fromhex(entry["password"])
#                     aad = entry["service"].lower().encode()
#                     try:
#                         return instance.decrypt(nonce, encrypted_password, aad)
#                     except Exception:
#                         return "Something went wrong\n"
#     except (FileNotFoundError, json.JSONDecodeError):
#         return None

def verify_key(key):
    with open("stored/hash.json", "r") as file:
        data = json.load(file)
        if "hash" in data and "nonce" in data:
            encrypted_hash = bytes.fromhex(data["hash"])
            nonce = bytes.fromhex(data["nonce"])

            instance = ccp(key)

            hash = instance.decrypt(nonce, encrypted_hash, None)
            if hash == default_hash:
                return True
            else:
                log("Key incorrect or hash file corrupted.")
                log("If you lost your key, you will need to make a new profile.")
                return False

def delete_profile():
    print_banner()
    log("You are about to delete your profile, this will delete all your passwords.")
    log("Do you want to continue? [y/n]")
    choice = get_input().lower()

    if choice == "y":
        print_banner()
        log("Are you sure you want to delete your current profile? This function cannot be undone.")
        log("[y/n]")
        choice = get_input()
        if choice == "y":
            if os.path.exists("stored"):
                shutil.rmtree("stored")
            time.sleep(1)
            log("/stored directory deleted. Restart the program to create a new profile.")
        else:
            log("Action cancelled.")
            time.sleep(1)
    else:
        cls()
        exit(0)

key, instance = None, None

def log_passwords(showCount=True):
    with open("stored/passwords.json", "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            log("No passwords stored yet.")
        
        if showCount:
            if (len(data) - 1) == 0: logf(f" {len(data)} password found")
            else: logf(f" {len(data)} passwords found")
            log("")
        for item in data:
            i = data.index(item) + 1
            log(f"{lightblue}[{cyan}{i}{lightblue}] {reset}{item["service"]}")

def view_passwords(key):
    print_banner()

    if not os.path.exists("stored/passwords.json"):
        open("stored/passwords.json", "w").close()

    with open("stored/passwords.json", "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            log("No passwords stored yet.")
            
        # if (len(data) - 1) == 0: logf(f" {len(data)} password found") 
        # else: logf(f" {len(data)} passwords found")

        # log("")
        # for item in data:
        #     i = data.index(item) + 1
        #     log(f"{cyan}[{lightcyan}{i}{cyan}] {reset}{item["service"]}")
        
        log_passwords()

        log("")
        log("What password would you like to view?")
        choice = get_input()

        requested_index = int(choice) - 1
    
        requested_password = data[requested_index]
        req_aad = requested_password["service"].lower().encode()
        req_encrypted = bytes.fromhex(requested_password["password"])
        req_nonce = bytes.fromhex(requested_password["nonce"])
        
        instance = ccp(key)
        decrypted_password = instance.decrypt(req_nonce, req_encrypted, req_aad)

        print_banner()

        logf(f"{lightcyan} {reset}Requested service{lightcyan} {lightblue}> {reset}{requested_password['service']}")
        log("")
        log(f"{cyan}[{reset} Username {cyan}]{reset} {lightblue}> {reset}{requested_password['username']}")
        log("")
        log(f"{cyan}[{reset} Password {cyan}]{reset} {lightblue}> {reset}{decrypted_password.decode()}")

        get_input()
        menu(key)

def delete_passwords(key):
    print_banner()
    log_passwords()
    log("")
    log("What password would you like to delete?")
    choice = get_input()

    requested_index = int(choice) - 1
    with open("stored/passwords.json", "r") as file:
        data = json.load(file)
        if requested_index < 0 or requested_index >= len(data):
            log("Please enter a valid index.")
        else:
            requested_service = data[requested_index]["service"]
            cls()
            print_banner()
            log(f"You are about to delete the password for {lightblue}{requested_service}{reset}. are you sure you want to do this?")
            log("Type 'confirm' to continue, press Enter to cancel.")

            if get_input() == 'confirm':
                del data[requested_index]
                with open("stored/passwords.json", "w") as file:
                    json.dump(data, file)

                print_banner()
                log(f"Password for {lightblue}{requested_service}{reset} deleted successfully.")
                get_input()
                menu(key)
            else:
                print_banner()
                log("Action cancelled.")
                exit(0)

def create_password(key):
    print_banner()

    log("What service would you like to save the password for?")
    service = get_input()
    print_banner()
    logf(f" Service {lightblue}>{reset} {service}")
    log("")

    log("What email/username do you want to associate with this service?")
    username = get_input()
    print_banner()
    logf(f" Service {lightblue}>{reset} {service}")
    log("")
    logf(f" Username {lightblue}>{reset} {username}")
    log("")

    log("Enter the password. (Type 'RANDOM' to generate a random password.)")
    password = get_input()

    if password == 'RANDOM':
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(28,32)))

    print_banner()
    logf(f" Service {lightblue}>{reset} {service}")
    log("")
    logf(f" Username {lightblue}>{reset} {username}")
    log("")
    logf(f" Password {lightblue}>{reset} {password}")

    if service and password:
        log("")
        log("Are you sure you want to save this password?")
        log(f"{lightcyan}[{white}y{lightblue}/{white}n{lightcyan}]{reset}")
        if get_input() == "y":
            save_password(key, password, username, service)

    menu(key)

def menu(key):
    print_banner()
    log(f"{lightblue}[{cyan}1{lightblue}] {reset}View passwords")
    log(f"{lightblue}[{cyan}2{lightblue}] {reset}Add a password")
    log(f"{lightblue}[{cyan}3{lightblue}] {reset}Delete a password")
    if not os.path.exists("stored/key.json"):
        log(f"{lightblue}[{cyan}4{lightblue}] {reset}Save key")
    log(f"{lightblue}[{cyan}0{lightblue}] {reset}Exit")

    choice = get_input()

    match choice:
        case "1": view_passwords(key)
        case "2": create_password(key)
        case "3": delete_passwords(key)
        case "4": 
            save_key(key)
            cls()
            print_banner()
            log("Key saved successfully.")
            get_input()
            menu(key)
        case "0": exit(0)

# Main

def main():
    if not os.path.exists("stored"):
        os.makedirs("stored")

    cls()

    if not os.path.exists("stored/passwords.json") and not os.path.exists("stored/hash.json"):
        cls()
        print_banner()
        log("This seems to be your first time using Pandora, do you want to create a new profile?")
        log(f"{lightcyan}[{white}y{lightblue}/{white}n{lightcyan}]{reset}")
        choice = get_input().lower()

        if choice == "y":
            print_banner()

            if (get_stored_key() != None):
                key = bytes.fromhex(get_stored_key())
            else:
                key = ccp.generate_key()

            logf(f" Key {lightblue}>{reset} {key.hex()}")
            log("")
            log("Please store this key in a safe place and do not share it with anyone.")
            log("This key will be used to view your passwords.")
            log("After this key has been generated, you will not be able to view it again.")

            instance = ccp(key)
            generate_hash(instance)

            log("Would you like to save the key?")
            log("(Recommended for easy access, but less secure if the device gets compromised.)")
            log(f"{lightcyan}[{white}y{lightblue}/{white}n{lightcyan}]{reset}")

            choice = get_input().lower()
            if choice == "y":
                save_key(key)
    else:
        if not os.path.exists("stored/hash.json"):
            print_banner()
            log("Your hash file is missing. Enter your key to create a new one.")
            choice = get_input()
            generate_hash(ccp(bytes.fromhex(choice)))

    try:
        if get_stored_key() is not None:
            key = bytes.fromhex(get_stored_key())
        else:
            print_banner()
            log("Please enter your key.")
            key = bytes.fromhex(get_input())
        
    except ValueError:
        print_banner()
        log("Invalid key entered. If you want to exit and try again later, press Enter.")
        log("If you forgot your key, you can delete your profile by typing 'DELETE'.")
        choice = get_input()
        if choice == "DELETE":
            delete_profile()
        else:
            cls()
            exit(0)

    if not verify_key(key):
        print("\nInvalid key entered. If you want to exit and try again later, press Enter.\nIf you forgot your key, you can delete your profile by typing 'DELETE'.")
        choice = input("\n>> ").strip()
        if choice == "DELETE":
            delete_profile()
        else:
            cls()
            exit(0)

    instance = ccp(key)

    # print_banner()
    # log("Hello world!!!")
    # helloworld = get_input()
    menu(key)




    # if not os.path.exists("stored/hash.json"):
    #     if os.path.exists("stored/passwords.json"):
    #         print("+ Your hash file is missing. Do you want to create a new one?")
    #         choice = input("\n[y/n]\n>> ").strip().lower()
    #         if choice == "y":
    #             print("+ Please enter your encryption key. If you don't have one, you have to create a new profile.")
    #             print("+ Please note that without this key, you will not be able to view your passwords. Even if you've already created a profile before.")
                
    #             if (get_stored_key() != None):
    #                 key = bytes.fromhex(get_stored_key())
    #             else:
    #                 key = ccp.generate_key()

    #     print("+ You don't have a hash setup yet. \n+ Do you want to create a new profile? (If this is your first time using the tool, you should say yes.)")
    #     choice = input("\n[y/n]\n>> ").strip().lower()
    #     if choice == "y":
    #         cls()
    #         if (get_stored_key() != None):
    #             key = bytes.fromhex(get_stored_key())
    #         else:
    #             key = ccp.generate_key()

    #         instance = ccp(key)
    #         print(f"\nEncryption key: {key.hex()}\n\nPlease store this key in a safe place and do not share it with anyone.\nThis key will be used to view your passwords.\nAfter this key has been generated, you will NEVER be able to view it again.")
    #         generate_hash(instance)
    #         print("\n+ Would you like to save the key? (Recommended for easy access, but less secure if the /stored directory is compromised.)")
    #         choice = input("\n[y/n]\n>> ").strip().lower()
    #         if choice == "y":
    #             save_key(key)
            
    #         print("Verification hash has been created, do not change this file.")
    #         time.sleep(1)
    # else:
    #     try:
    #         if (get_stored_key() != None):
    #             key = bytes.fromhex(get_stored_key())
    #         else:
    #             key = bytes.fromhex(input("\nEnter your key >> "))
    #     except ValueError:
    #         print("\nInvalid key entered. If you want to exit and try again later, press Enter.\nIf you forgot your key, you can delete your profile by typing 'DELETE'.")
    #         choice = input("\n>> ").strip()
    #         if choice == "DELETE":
    #             delete_profile()
    #         else:
    #             cls()
    #             exit(0)

    #     if verify_key(key) == False:
    #         print("Key verification failed. Your key file may be corrupted or you entered the wrong key.\nDo you want to create a new profile? (This will delete your current passwords and hash file.)")
    #         choice = input("\n[y/n]\n>> ").strip().lower()

    #         if choice == "y":
    #             print("\nAre you sure you want to delete your current profile? This function cannot be undone.")
    #             choice = input("\n[y/n]\n>> ").strip().lower()
    #             if choice == "y":
    #                 os.rmdir("stored")
    #                 time.sleep(1)
    #                 cls()
    #                 print("stored directory deleted. Restart the program to create a new profile.")
    #             else:
    #                 time.sleep(1)
    #                 print("Action cancelled.")
    #         else:
    #             cls()
    #             exit(0)
    #     else:
    #         print("Key verified successfully.")

if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt):
        print("\nSomething went wrong, exiting the program.\n")
        exit(0)

# try:
#     with open("stored/key.json", "r") as file:
#         key = json.load(file)["key"].encode()
# except FileNotFoundError or json.JSONDecodeError:
#     print("1. Load new profile")
#     if os.path.exists("stored/passwords.json"):
#         print("2. Retrieve passwords\n")


# first_choice = input(">> ")

# print("You chose:", first_choice)