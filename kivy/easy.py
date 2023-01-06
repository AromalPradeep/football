
# gui using kivy
# DBMS project

# GUI : kivy
import kivy
from kivy.app import App
from kivy.core.window import Window

from kivy.properties import ObjectProperty,StringProperty,NumericProperty,BooleanProperty,ListProperty

# UIX
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.config import Config
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button

# MYSQL Connectivity
import mysql.connector

# Creating connection object
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "root",
    database="football"
)

mycursor = mydb.cursor()

# Profiling
import cProfile

# other modules
import hashlib
import random

## functions

## screens

# Screen_0 : Loading
class ScreenZero(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    key_down = StringProperty() # perform button state
    
    def on_pre_enter(self, *args):
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        return
    
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.manager.current = 'screen19' #'screen19' 
        return
    
    def on_pre_leave(self, *args):
        #self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        return
    
 # Screen_1 : Menu  
class ScreenOne(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def function(self, *args):
        return

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text
        self.obj.selected = True

class DeletePopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(DeletePopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = "delete row containing "+str(obj.text)

class Delete2Popup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(Delete2Popup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = "Row deleted"
        
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt

class EButton(RecycleDataViewBehavior, Button):

    def on_press(self):
        
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt

class MTButton(RecycleDataViewBehavior, Button):

    def on_press(self):
        
        #self.manager.current = 'screen19'
        
        text = self.text
        
        sql = "SELECT Team_id,Team_name FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for i in k:
            if text in i:
                print(i[1])
        
        

class MKButton(RecycleDataViewBehavior, Button):

    def on_press(self):
        popup = DeletePopup(self)
        popup.open()

    def update_changes(self):
        
        try:
            
            text = self.text
            
            sql = "SELECT Team_id,Team_name FROM teams"
            mycursor.execute(sql)
            k = mycursor.fetchall()
            
            for i in k:
                print(i)
                if text in i:
                    kf = i[0]
                    print(kf)
                    sql = "DELETE FROM teams WHERE Team_id = %d"%kf      
                    mycursor.execute(sql)        
                    mydb.commit()
                    
                    popup = Delete2Popup(self)
                    popup.open()            
            
        except Exception as e:
            print(e)
            pass
        
        

# Screen_2 : Teams
class ScreenTwo(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

# players
class ScreenThree(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM players"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

# games
class ScreenFour(Screen):
    
        
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT Team_1,Team_2 FROM games" # add goals
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

# manage
class ScreenFive(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def function(self, *args):
        return

class ScreenSix(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def add(self, *args):
        sql = "INSERT INTO players VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.ids.Team_id.text,
        self.ids.Team_name.text,
        self.ids.Manager.text,
        self.ids.Captain.text,
        self.ids.Matches_Played.text,
        self.ids.Wins.text,
        self.ids.Draws.text,
        self.ids.Loses.text,
        self.ids.Goal_Difference.text)
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.ids.info.text = str(val)+" Row Added"
            self.ids.Team_id.text = ""
            self.ids.Team_name.text = ""
            self.ids.Manager.text = ""
            self.ids.Captain.text = ""
            self.ids.Matches_Played.text = ""
            self.ids.Wins.text = ""
            self.ids.Draws.text = ""
            self.ids.Loses.text = ""
            self.ids.Goal_Difference.text = ""            
            
        except Exception as e:
            k = str(e)
            k = k[k.find(":")+1:]
            self.ids.info.text = "Error : "+k
            
        return
    
    def clear(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return
    
    def on_pre_leave(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return

class ScreenSeven(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM Argentina"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def f(self, *args):
        self.manager.current = 'screen11' 
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []
        

class ScreenEight(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM Argentina"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

class ScreenNine(Screen):
   
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM Argentina"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

# teams add
class ScreenTen(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def add(self, *args):
        sql = "INSERT INTO teams VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.ids.Team_id.text,
        self.ids.Team_name.text,
        self.ids.Manager.text,
        self.ids.Captain.text,
        self.ids.Matches_Played.text,
        self.ids.Wins.text,
        self.ids.Draws.text,
        self.ids.Loses.text,
        self.ids.Goal_Difference.text)
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.ids.info.text = str(val)+" Row Added"
            self.ids.Team_id.text = ""
            self.ids.Team_name.text = ""
            self.ids.Manager.text = ""
            self.ids.Captain.text = ""
            self.ids.Matches_Played.text = ""
            self.ids.Wins.text = ""
            self.ids.Draws.text = ""
            self.ids.Loses.text = ""
            self.ids.Goal_Difference.text = ""            
            
        except Exception as e:
            k = str(e)
            k = k[k.find(":")+1:]
            self.ids.info.text = "Error : "+k
            
        return
    
    def clear(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return
    
    def on_pre_leave(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return

# teams delete
class ScreenEleven(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def f(self, *args):
        self.manager.current = 'screen11' 
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []
        

# teams view
class ScreenTwelve(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

# teams edit
class ScreenThirteen(Screen):
     
    serror = StringProperty()
    shint = StringProperty()
    
    def add(self, *args):
        
        try:
            
            text = self.ids.Team_id.text
            sql = "DELETE FROM teams WHERE Team_id = %s"%text 
            mycursor.execute(sql)
            mydb.commit()
            
            print("deleted")
            
        except Exception as e:
            print(e)
            pass
        
        sql = "INSERT INTO teams VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.ids.Team_id.text,
        self.ids.Team_name.text,
        self.ids.Manager.text,
        self.ids.Captain.text,
        self.ids.Matches_Played.text,
        self.ids.Wins.text,
        self.ids.Draws.text,
        self.ids.Loses.text,
        self.ids.Goal_Difference.text)
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.ids.info.text = str(val)+" Row Updated"
            self.ids.Team_id.text = ""
            self.ids.Team_name.text = ""
            self.ids.Manager.text = ""
            self.ids.Captain.text = ""
            self.ids.Matches_Played.text = ""
            self.ids.Wins.text = ""
            self.ids.Draws.text = ""
            self.ids.Loses.text = ""
            self.ids.Goal_Difference.text = ""            
            
        except Exception as e:
            k = str(e)
            k = k[k.find(":")+1:]
            self.ids.info.text = "Error : "+k
            
        return
    
    def edit(self, country,*args):
        
        try :
            sql = "SELECT * FROM teams WHERE Team_name = '%s'"%country
            mycursor.execute(sql)
            k = mycursor.fetchall()
            k = k[0]
            
            
            
            self.ids.Team_id.text = str(k[0])
            self.ids.Team_name.text = str(k[1])
            self.ids.Manager.text = str(k[2])
            self.ids.Captain.text = str(k[3])
            self.ids.Matches_Played.text = str(k[4])
            self.ids.Wins.text = str(k[5])
            self.ids.Draws.text = str(k[6])
            self.ids.Loses.text = str(k[7])
            self.ids.Goal_Difference.text = str(k[8])
            
            
        
        except Exception as e:
            k = str(e)
            k = k[k.find(":")+1:]
            self.ids.info.text = "Error : "+k
        
        
        
        return
    
    def clear(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return
    
    def on_pre_enter(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return
    
    def on_pre_leave(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return

class ScreenFourteen(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def add(self, *args):
        
        
        try:
            
            text = self.ids.Team_id.text
            sql = "DELETE FROM teams WHERE Team_id = %d"%text 
            mycursor.execute(sql)
            mydb.commit()
            
        except Exception as e:
            print(e)
            pass
        
        sql = "INSERT INTO teams VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.ids.Team_id.text,
        self.ids.Team_name.text,
        self.ids.Manager.text,
        self.ids.Captain.text,
        self.ids.Matches_Played.text,
        self.ids.Wins.text,
        self.ids.Draws.text,
        self.ids.Loses.text,
        self.ids.Goal_Difference.text)
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.ids.info.text = str(val)+" Row Added"
            self.ids.Team_id.text = ""
            self.ids.Team_name.text = ""
            self.ids.Manager.text = ""
            self.ids.Captain.text = ""
            self.ids.Matches_Played.text = ""
            self.ids.Wins.text = ""
            self.ids.Draws.text = ""
            self.ids.Loses.text = ""
            self.ids.Goal_Difference.text = ""            
            
        except Exception as e:
            k = str(e)
            k = k[k.find(":")+1:]
            self.ids.info.text = "Error : "+k
            
        return
    
    def clear(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return
    
    def on_pre_leave(self, *args):
        self.ids.Team_id.text = ""
        self.ids.Team_name.text = ""
        self.ids.Manager.text = ""
        self.ids.Captain.text = ""
        self.ids.Matches_Played.text = ""
        self.ids.Wins.text = ""
        self.ids.Draws.text = ""
        self.ids.Loses.text = ""
        self.ids.Goal_Difference.text = ""
        self.ids.info.text = ""
        return

class ScreenFifteen(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def f(self, *args):
        self.manager.current = 'screen11' 
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []
        

class ScreenSixteen(Screen):
    
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

class ScreenSeventeen(Screen):
      
    serror = StringProperty()
    shint = StringProperty() 
    data_items = ListProperty([])

    def on_pre_enter(self, *args):
        sql = "SELECT * FROM teams"
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for row in k:
            for col in row:
                self.data_items.append(col)
        
        return
    
    def on_pre_leave(self, *args):
        self.data_items = []

class ScreenEighteen(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def function(self, *args):
        return

# Screen_19 : Login
class ScreenNineteen(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def password(self, *args):
        #print(self.ids.username.text)
        #print(self.ids.password.text)
        
        if self.ids.username.text.lower() == 'admin' and self.ids.password.text.lower() == 'admin':
            self.manager.current = 'screen5' 
            return
        
        username,pword = self.ids.username.text,self.ids.password.text
        username= hashlib.md5(username.encode()).hexdigest()
        pword = hashlib.md5(pword.encode()).hexdigest()
        
        sql = "SELECT password,username FROM users where password = '%s' or username = '%s'"%(pword,username)
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for i in k:
            if username == i[0] and pword != i[0]:
                self.ids.info.text = "Invalid Credentials"
                return
        
        self.manager.current = 'screen1' 
        
        return
    
    def on_pre_leave(self, *args):
        
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.info.text = ""
        
        return

# Screen_20 : Sign up
class ScreenTwenty(Screen):
    
    serror = StringProperty()
    shint = StringProperty()
    
    def password(self, *args):
        #print(self.ids.username.text)
        #print(self.ids.password.password)
        
        if self.ids.password.text != self.ids.cpassword.text:
            self.ids.info.text = "Passwords do not match"
            return
        
        email,username,pword = self.ids.email.text,self.ids.username.text,self.ids.password.text
        email = hashlib.md5(email.encode()).hexdigest()
        username= hashlib.md5(username.encode()).hexdigest()
        pword = hashlib.md5(pword.encode()).hexdigest()
        
        sql = "SELECT email,username FROM users where email = '%s' or username = '%s'"%(email,username)
        mycursor.execute(sql)
        k = mycursor.fetchall()
        
        for i in k:
            if email == i[0]:
                self.ids.info.text = "Existing Email"
                return
            elif username == i[1]:
                self.ids.info.text = "Existing Username"
                return
        
        sql = "INSERT INTO users VALUES (%s, %s, %s)"
        val = (email,username,pword)
        mycursor.execute(sql, val)
        
        mydb.commit()
        
        self.manager.current = 'screen1' 
        
        return
    
    def on_pre_leave(self, *args):
        
        self.ids.email.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.cpassword.text = ""
        self.ids.info.text = ""
        
        return


# screen manager
class Manager(ScreenManager):
    
    screen_zero = ObjectProperty(None)

class easyApp(App):
        
    def build(self):
        
        # Window
        self.title = 'Football Management System'
        #self.icon = 'static/icon.png'
        
        height = 1080   
        width = 1920
        bias = 1.5
        
        Window.size = (width/bias,height/bias)
        
        return Manager()
    
    def on_start(self):

        # Profile
        self.profile = cProfile.Profile()
        self.profile.enable()

        return
    
    def stop(self):
        
        # Profile
        self.profile.disable()
        self.profile.dump_stats('data/profile/lastrun.profile')
        
        # kivy
        Window.close()
        
        return

if __name__ == "__main__":
    
    temp = ''
    
    # App start
    main = easyApp()
    main.run()

