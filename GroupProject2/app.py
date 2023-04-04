from cgitb import text
from copy import deepcopy
import json
import os
from pydoc import TextRepr
from datetime import date, datetime
from tkinter import *
from PIL import ImageTk, Image


'''Global Data to be used across all functions and Windows'''
window = Tk(className = "- Drink Service -")
window.geometry("800x800")
global_user = {}
images = {}
f = open('db.json')
drink_data = json.load(f)

'''Converting images into a array'''
for i in drink_data:
    if(i["file_name"] != ""):
        temp_path = "./Assets/"+i["file_name"]
    else:
        temp_path = "./Assets/drink.png"
    
    temp = Image.open(temp_path)
    temp = temp.resize((200,200))
    temp_image_tk = ImageTk.PhotoImage(temp)
    images[i["id"]] = temp_image_tk

'''Main window where user chooses what to do'''   
def main_window(t):
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    
    t.destroy()
    welcome = Label(text="Welcome to the Drink Service")
    label = Label(
        text = "CopyRight 2022",
        foreground = "white",
        background = "blue"
    )
    create = Button(window, text="More Options",command=lambda:take_action_on_drink(0,drink_data))
    welcome.grid(column=1, row=1)
    label.grid(column=1, row=2)
    create.grid(column=1, row=3)
    
    button_list = []
    
    for i in range(1,len(images)+1):
        button_list.append(Button(window, image = images[str(i)], command=lambda id=i:take_action_on_drink(id,drink_data)))
    
    r = 4
    c = 0
    
    for i in range(len(button_list)):
        if(c >= 3):
            r += 2
            c = 0
        button_list[i].grid(column = c, row = r, padx = 5, pady = 5)
        Label(text = drink_data[i]["name"]).grid(column = c, row = r+1)
        c+=1
        
'''Allows user to Login, Display Drink Details, Sell a drink, or create a drink.'''
def take_action_on_drink(id, data):    
    top = Toplevel(window)
    top.geometry("400x300")
    top.title("Login")
    top.columnconfigure(0, weight=2)
    Label(top, text= "User Name:", font=('Mistral 18 bold')).grid(column=0, row=0)
    user_name = Entry(top, width=20)
    user_name.grid(column=0, row=1)
    Label(top, text= "Password:", font=('Mistral 18 bold')).grid(column=0, row=2)
    password = Entry(top, width=20)
    password.grid(column=0, row=3)
    login = Button(top,text="Login",font = 'Helvetica', foreground = 'Black', background = 'Grey', command =lambda:server_log_in(user_name.get(),password.get()))
    login.grid(column=0,row=4)
    details = Button(top,text='Drink Details', font = 'Helvetica', foreground = 'Black', background = 'Grey', command =lambda:display_drink_details(data,id))
    details.grid(column=0,row=5)
    sale = Button(top,text='Drink Sale', font = 'Helvetica', foreground = 'Black', background = 'Grey', command =lambda:sell_drink(top,id))
    sale.grid(column=0,row=6)
    new_drink = Button(top,text='Create New Drink', font = 'Helvetica', foreground = 'Black', background = 'Grey', command =lambda:create_drink())
    new_drink.grid(column=0,row=7)

'''Checks if user is logged in or not'''
def login_check():
    if(global_user == {}):
        top = Toplevel(window)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        top.geometry("300x100")
        top.title("Access Denied")
        l = Label(top, text = "You must login to use this feature")
        l.grid(column=1)
        e = Button(top,text="Okay",command=lambda:top.destroy())
        e.grid(column=1)
        return False
    else:
        return True

'''Logs into server returning user information'''
def server_log_in(user_name, password):
    file = open('server.json')
    d = json.load(file)
    temp = {}
    global global_user
    top = Toplevel(window)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)
    top.columnconfigure(2, weight=1)
    top.geometry("200x100")
    if(len(global_user.keys()) == 0):
        for i in range(len(d)):
            if(d[i]["user_name"] == user_name):
                temp = d[i]
        if(len(temp.keys()) == 0):
            top.title("LOGIN FAILURE")
            l = Label(top, text = "Your user name is incorrect!")
            l.grid(column=1)
            e = Button(top,text="Okay",command=lambda:top.destroy())
            e.grid(column=1)
            log_event("User Name Failure",f"Username: {user_name} - Password: {password}")     
        elif(temp["password"] == password):
            global_user = temp
            log_event("Login Success","Username: "+user_name+" - Password: "+password)
            top.title("LOGGED IN")
            l = Label(top, text = user_name+" logged In!")
            l.grid(column=1)
            e = Button(top,text="Okay",command=lambda:top.destroy())
            e.grid(column=1)
        else:
            top = Toplevel(window)
            top.columnconfigure(0, weight=1)
            top.columnconfigure(1, weight=1)
            top.columnconfigure(2, weight=1)
            top.geometry("200x100")
            top.title("LOGIN FAILURE")
            l = Label(top, text = "Your password is incorrect!")
            l.grid(column=1)
            e = Button(top,text="Okay",command=lambda:top.destroy())
            e.grid(column=1)
            log_event("Password Failure","Username: "+user_name+" - Password: "+password)
    

'''Logs multiple types of events around the application'''
def log_event(event_category: str = "General", event: str = "LOG", user:str = "None", id: str = "None"):
    l = {}
    l["category"] = event_category
    l["event"] = event
    l["user"] = user
    l["date_time"] = str(datetime.now())
    l["drink_id"] = id
    file = open('logs.json')
    d = json.load(file)    
    d.append(l)
    
    with open('logs.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(d))

'''Displays drink details into a concise window'''
def display_drink_details(data, id):
    if(id!=0):
        top = Toplevel(window)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)

        top.geometry("500x250")
        top.title(data[int(id)-1]["name"])
        Label(top, image = images[str(id)]).grid(column=0, rowspan=len(data[int(id)-1]["ingredients"]))
        Label(top, text="Ingredient:",font=('Helvetica 18 bold')).grid(column=1, row=0)
        Label(top, text="Quantity:",font=('Helvetica 18 bold')).grid(column=2,row=0)
        row = 0
        for i in data[int(id)-1]["ingredients"]:
            row+=1
            Label(top, text=i["ingredient"]).grid(column=1, row=row)
            Label(top, text=i["oz"]).grid(column=2, row=row)

'''Checks if we have all ingredents to sell drinks and sells them if we do updating our inventory'''
def sell_drink(t,id):
    if(login_check() and id != 0):
        t.destroy()
        data = drink_data
        display_drink_details(data, id)
        
        ing = open('ingredients.json')
        ingredients = json.load(ing)
        
        flag = False
        ingredient_owned = False
        for i in data[int(id)-1]["ingredients"]:
            for j in ingredients:
                if(i["ingredient"] == j["Ingredient"]):
                    ingredient_owned = True
                    q = float(j["OZ_Available"]) - float(i["oz"])
                    if(q >= 0):
                        j["OZ_Available"] = str(q)
                    else:
                        flag = True
                        top = Toplevel(window)
                        top.columnconfigure(0, weight=1)
                        top.columnconfigure(1, weight=1)
                        top.columnconfigure(2, weight=1)
                        top.geometry("400x100")
                        top.title("Quantities Exceeded")
                        l = Label(top, text = "There is not enough "+i["ingredient"]+"to make this drink!")
                        l.grid(column=1)
            if(not ingredient_owned):
                flag = True
                top = Toplevel(window)
                top.columnconfigure(0, weight=1)
                top.columnconfigure(1, weight=1)
                top.columnconfigure(2, weight=1)
                top.geometry("400x100")
                top.title("Quantities Exceeded")
                l = Label(top, text = "There is not enough "+i["ingredient"]+"to make this drink!")
                l.grid(column=1)
            else:
                ingredient_owned = False
                
        if(not flag):
            with open('ingredients.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json.dumps(ingredients))

'''User Created Drinks that are validated'''    
def create_drink():
    if(login_check()):
        top = Toplevel(window)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        
        top.geometry("400x500")
        top.title("New Drink")
        Label(top, text= "Drink Creator", font=('Mistral 18 bold')).grid(column=1)
        Label(top, text= "No special Characters", font=('Mistral 12 bold')).grid(column=1)
        Label(top, text= "Name of Drink", font=('Mistral 18 bold')).grid(column=1)
        name = Entry(top, width=20)
        name.grid(column=1)
        Label(top, text= "Ingredients in a Comma Seperated List", font=('Mistral 18 bold')).grid(column=1)
        Label(top, text= "Comma Seperated List", font=('Mistral 12 bold')).grid(column=1)
        ingredients = Entry(top, width=20)
        ingredients.grid(column=1)
        Label(top, text= "Ingredients measurements", font=('Mistral 18 bold')).grid(column=1)
        Label(top, text= "Comma Seperated List", font=('Mistral 18 bold')).grid(column=1)
        measurements = Entry(top, width=20)
        measurements.grid(column=1)
        Label(top, text= "Instructions", font=('Mistral 18 bold')).grid(column=1)
        instructions = Entry(top, width=20)
        instructions.grid(column=1)
        Label(top, text= "Description", font=('Mistral 18 bold')).grid(column=1)
        description = Entry(top, width=20)
        description.grid(column=1)
        Label(top, text= "Exact File Path", font=('Mistral 18 bold')).grid(column=1)
        file = Entry(top, width=20)
        file.grid(column=1)
        
        submit = Button(top,text="Submit",command=lambda:validate(top,name.get(),ingredients.get(),measurements.get(),instructions.get(),description.get(),file.get()))
        submit.grid(column=1)
    
'''Validates user created drinks'''
def validate(t, name, ingredients, measurements, instructions, description, file):
    errors = []
    if(not name.isalpha()):
        errors.append("Name must be Alphabetic.")
    if(len(ingredients) == 0):
        errors.append("Double check ingredients and measurements.")
    if(len(file) > 0):
        try:
            open(file)
        except:
            errors.append("File doesnt exist.\nLeave blank for default.")
    if(len(errors) != 0):
        top = Toplevel(window)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        top.geometry("300x100")
        top.title("Errors in Drink Creation")
        for i in errors:
            Label(top, text = errors).grid(column=1)
    else:
        send_drink(t, name, create_ingredient_list(ingredients,measurements), instructions, description, file)
       
'''Once drink is validated this sends it to the server''' 
def send_drink(t, name, ingredients, instructions, description, file):
    global drink_data
    drink = {}
    drink["id"] = str(len(drink_data)+1)
    drink["name"] = name
    drink["ingredients"] = ingredients
    drink["instructions"] = instructions
    drink["description"] = description
    if(len(file) > 0): 
        drink["file_name"] = file
    else:
        drink["file_name"] = "drink.png"
    
    drink_data.append(drink)
    with open('db.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(drink_data))
    restart(t)
    
'''Updates current windows'''
def restart(t):
    global window
    top = Toplevel(window)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)
    top.columnconfigure(2, weight=1)
    top.columnconfigure(3, weight=1)
    top.geometry("300x100")
    top.title("Changes Successful")
    Label(top, text="Please restart to see changes").grid(column=0,row=0)
    e = Button(top,text="Quit Program",command=lambda:quit_program())
    e.grid(column=1,row=1)
    e2 = Button(top,text="Okay",command=lambda:(t.destroy(),top.destroy()))
    e2.grid(column=2,row=1)

'''Creates ingredient object from two arrays'''
def create_ingredient_list(ingredients,measurements):
    i_list = ingredients.split(",")
    m_list = measurements.split(",")
    l = []
    
    if(len(i_list) == len(m_list)):
        for i in range(len(i_list)):
            if(i_list[i].isalpha() and m_list[i].isnumeric()):
                l.append({"oz": m_list[i], "ingredient": i_list[i]})
    return l

    
'''Closes and quits program'''
def quit_program():
    os._exit(0)

def open_popup(window: Tk):
    top = Toplevel(window)
    top.geometry("350x300")
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)
    top.columnconfigure(2, weight=1)
    top.title("Agreement")
    Label(top, text= 
          "If you press agree, you give consent\n" 
          "to the use of data you provide to be\n"+
          "used in any way the company sees fit.\n"+
          "If you have any questions are conecerns\n"+
          "please contact HR. Any data that is given\n"+
          "is at will and we are not responsible for\n"+
          "security breaches. user may not sell or\n"+
          "distribute data without the express consent\n"+
          "of umbrella company. This program goes through\n"+
          "routine data penetration tests but unaitherized\n"+
          "tests or uses is prohibited. These requirements\n"+
          "are elastic and may change over time as needed.",
          font=('Mistral 14'), justify=LEFT).grid()
    Button(top, text='Agree', font = 'Helvetica', foreground = 'Black', background = 'green', command = lambda:main_window(top)).grid()
    Button(top, text = "Deny", font = 'Helvetica', foreground= 'Black', background = 'red', command = quit_program).grid()
    
open_popup(window)

window.mainloop()
    
