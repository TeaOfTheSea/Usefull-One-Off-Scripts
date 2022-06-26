import os

def main():
    os.chdir("/home/monkey/")
    data = open(".bashrc").readlines()
    foundStart = False
    for i in data:
        if foundStart:
            end = i.find("=")
            print(i.strip()[6:end:])
        else:
            index = i.find("#aliases")
            if index != -1:
                foundStart = True

if __name__ == "__main__": main()
