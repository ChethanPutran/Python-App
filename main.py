from kivy.app import *
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
import time

Builder.load_file("design.kv")

class LoginScreen(Screen):
    
    
    def toSignUpScreen(self):
        self.manager.current = "signup_screen"
        
    def login(self,userName,password,check):
        trueUserName = '1'
        truePassword='1'
        
        with open('users.json') as file:
            users = json.load(file)
            if userName.text in users:
                if(users[userName.text]['password'] == password.text):
                    self.manager.current = "login_success_screen"
                else:
                    check.text = "Invalid Credentials!"
            else:
                    check.text = "Invalid Credentials!"    
    
    
    def toForgotPassword(self):
        self.manager.current = "forgot_password_screen"
        
        
class SignUpScreen(Screen):
    def signUp(self,fullName,email,password,phone,gender):
        userData = {
            "id":0,
            "full_name":fullName.text,
            "email":email.text,
            "password":password.text,
            "phone_number":phone.text,
            "gender":gender.text,
            "create_on":datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            }
        
        with open("users.json") as file:
           usersDb = json.load(file)
           usersDb[email.text] = userData
     
        with open("users.json",'w') as file:
           json.dump(usersDb,file)
           
        self.manager.current = "signup_success_screen"   

class SignUpScreenSuccess(Screen):
    def goForlogin(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "login_screen"
           

class LoginScreenSuccess(Screen):
    def getQuote(self,feeling):
        feelings = glob.glob("quotes\\*txt")
        availableFeelings =[Path(filename).stem for filename in feelings]
        feeling=feeling.lower()      
        if(feeling in availableFeelings):
            with open(f'quotes/{feeling}.txt',encoding='utf-8') as file:
                quotes = file.readlines()
            self.ids.wrongFeeling.text = random.choice(quotes) 
        else:    
            self.ids.wrongFeeling.text = "Try another feeling!"
            
            
    def logout(self):
        self.manager.current = "login_screen"


email_ = ''

class ForgotPasswordScreen1(Screen):
    def validateEmail(self,email):
        with open('users.json') as file:
            users = json.load(file)
        if email in users:
            # codeGenandSend()
            self.ids.warningText.text = "We have sent a verification code to your email."
            time.sleep(3)
            self.manager.current = "forgot_password_screen2" 
        else:
            self.ids.warningText.text = "User not found!"            
class ForgotPasswordScreen2(Screen):
    
    def validateCode(self,code):
        trueConfCode = '1234'
        if trueConfCode == code:
           self.manager.current = "forgot_password_screen3"
        else:
            self.ids.warningText.text = "Invalid Code!"  
                      
class ForgotPasswordScreen3(Screen):
    def validateEmail(self,newPass,confirmPass):
       
        if newPass != confirmPass:
            self.ids.warningText.text = "Passwords should match!"
        else:
            
            with open('users.json') as file:
                users = json.load(file)
            
            users[userEmail]['password'] = newPass
            
            with open("users.json",'w') as file:
                json.dump(users,file)
                  
            self.ids.warningText.text = "Password reset successful."
            time.sleep(3)
            self.manager.current = "login_screen"      
                   
                     
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    
    def build(self):
        return RootWidget()


if __name__=="__main__":
    MainApp().run()    