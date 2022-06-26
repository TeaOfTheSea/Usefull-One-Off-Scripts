import os


def command(arg):
    stream = os.popen(arg)
    output = stream.read()
    if ((len(output) > 1) and (output != "1\n")): print(output)

def main():
    from dotenv import load_dotenv

    load_dotenv()
    gateway = os.getenv("GATEWAY")
    id = os.getenv("ID")
    secret = os.getenv("SECRET")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    command("sudo vpnc --gateway " + gateway + " --id " + id + " --secret " + secret + " --username " + username + " --password " +password)
    
if __name__ == "__main__": main()
