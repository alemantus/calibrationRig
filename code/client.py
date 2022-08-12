from urllib import response
import requests  
import numpy as np
import urllib.request
import os
import glob

class Menu():
    def __init__(self):
        #self.rigIP = "calibrationPlatform.local"
        #self.wandIP = input("Input IP of wand (default: danwand.local): ")

        self.rigIP = "10.11.131.184"
        self.wandIP = "10.11.131.182"
        self.clearImg()

    def infoPage(self):
        print("\n Welcome! You have the following options. \n \
    1: Calibrate \n \
    2: Get current pose\n \
    3: Move stepper x mm in y direction \n \
    4: Go to pose x in mm \n \
    5: Take a picture \n \
    6: move n steps with x mm spacing\n \
    7: Clear all images")

        self.option = 0

        self.option = int(input("Please enter a number: "))
        if (self.option == 1):
            self.height = self.calibrate()
        elif(self.option == 2):
            self.heigt = self.getCurrentPose()
        elif(self.option == 3):
            self.height = self.moveStepper()
        elif(self.option == 4):
            pose = input("Enter pose in mm: ")
            self.height = self.go2pose(pose)
        elif(self.option == 5):
            name = input("input pic fileName: ")
            self.takePic(name)
        elif(self.option == 6):
            self.height = self.moveInterval()
        elif(self.option == 7):
            self.clearImg()
        else:
            self.infoPage()
            
    def calibrate(self):
        response = requests.get(f"http://{self.rigIP}:5000/calibrate/") 
        return response

    def getCurrentPose(self):
        response = requests.get(f"http://{self.rigIP}:5000/getCurrentPose_mm/") 
        print(f"\nCurrent pose is: {response.text}")
        return response

    def moveStepper(self):
        direction = input("Enter direction 1 for up. 0 for down: ")
        if (direction == "1"):
            direction = "up"
        elif (direction == "0"):
            direction = "down"
        else:
            print(f"{direction} is an invalid option")
            self.moveStepper()

        x_mm = input("Enter travel in mm: ") 

        response = requests.get(f"http://{self.rigIP}:5000/moveStepper_mm/{direction}/{x_mm}/")
        return response

    def go2pose(self, pose):
        print("Moving stepper")
        #pose = input("Enter desired pose: ")
        response = requests.get(f"http://{self.rigIP}:5000/go2pose_mm/{pose}/")
        return response
    
    def takePic(self,name):
        
        url = "http://10.11.131.182:8080/pic/picture?size=100"
        response = requests.get(url)
        pwd = os.path.dirname(os.path.realpath(__file__))

        print("Taking a picture - no light")
        urllib.request.urlretrieve(f"{url}", f"{pwd}/pictures_noLight/{name}.png")

        print("Taking a picture - flash")
        urllib.request.urlretrieve(f"{url}&flash=1", f"{pwd}/pictures_flash/{name}.png")

        print("Taking a picture - dias")
        urllib.request.urlretrieve(f"{url}&dias=1", f"{pwd}/pictures_dias/{name}.png")

    def moveInterval(self):
        print("The platform will start at height A and move down to heigt B at a interval x given in mm")
        startPose = input("Enter start pose A: ")
        endPose = input("Enter end pose B: ")
        stepInterval = input("Enter step interval x in mm: ")

        stepArray = np.arange(float(startPose),float(endPose),float(stepInterval))
        print(stepArray)
        for idx,i in enumerate(stepArray):
            self.go2pose(i)
            self.takePic(idx)
            print(f"moving to: {i}")
            name_height_translation += f"{idx}:{i}\n"
        # post-fence fix
        self.go2pose(i+float(stepInterval))
        self.takePic(idx+1)


        
        pwd = os.path.dirname(os.path.realpath(__file__))
        f = open(f"{pwd}/params.txt", 'w')
        f.write(f"Number of images: {len(stepArray)+1}\n \
        Start height: {startPose} mm\n \
        End height : {endPose} mm\n \
        Distance between images: {stepInterval} mm\n \
        Name Height translation (name:height): {name_height_translation}")

        f.close()


    def clearImg(self):
        pwd = os.path.dirname(os.path.realpath(__file__))
        files = glob.glob(f"{pwd}/pictures_noLight/*")
        for f in files:
            os.remove(f)
        
        files = glob.glob(f"{pwd}/pictures_flash/*")
        for f in files:
            os.remove(f)
        
        files = glob.glob(f"{pwd}/pictures_dias/*")
        for f in files:
            os.remove(f)
        
if __name__ == "__main__":
    menu = Menu()

    if(menu.wandIP==""):
        menu.wandIP = "danwand.local"

    while(1):
        menu.infoPage()

