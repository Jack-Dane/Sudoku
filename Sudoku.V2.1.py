from tkinter import * #Libaries used throughout program
import time
import sqlite3
import random ################################# ADD QUOTATIONS!!!!!!!!!!!!!!!!!!!! ############################## ONE SUDOKU DOESNT WORK FIND IT AND DESTROY IT!

conn=sqlite3.connect('SudokuDatabase.db') #Connecting python with the database 'SudokuDatabase.db'
c=conn.cursor() #Telling python where to search

class sudoku():#Done
    def __init__(self):
        self.conn=sqlite3.connect('SudokuDatabase.db')
        self.c=self.conn.cursor()
        self.root=Tk()
        self.root.title(difficultchoice)
        self.root.configure(background=bg1)
        Label(text='Score',font=fonttext,bg=bg2,fg=fg1).grid(row=9,column=0) #Label showing current score
        self.countlabel=Label(text=0,font=fonttext,bg=bg2,fg=fg1)
        self.countlabel.grid(row=9,column=1,columnspan=2)
        if saveglobal==True: #Creating the saved grid and original grid when the user has pressed load
            self.grid=[list(savelistglobal[2][i:i+9]) for i in range(0,81,9)] #savelistglobal[2] = edited version of save
            self.countlabel['text']=savelistglobal[6] #savelistglobal[6] = saved count from when the record was last saved
            self.originalgrid=[list(savelistglobal[1][i:i+9]) for i in range(0,81,9)] #savelistglobal[1] = original sudoku
        else: # Get random sudoku from difficultchoice table when saveglobal==False
            self.x=[]
            for row in self.c.execute('SELECT * FROM '+difficultchoice):
                self.x.append(row)
            self.save=random.randint(0,49)
            self.x=self.x[self.save] #Self.x = random sudoku str
            #self.x=self.x[51]
            self.x=''.join(self.x)
            self.grid=[list(self.x[i:i+9]) for i in range(0,81,9)]
            self.originalgrid=[list(self.x[i:i+9]) for i in range(0,81,9)]
        x,y,num=0,0,0
        for i in range(0,81): #Make 81 buttons for a 9x9 grid
            if x==9:
                y+=1 #Creating row and columns for buttons
                x=0
            self.b='self.b'+str(i)
            if self.originalgrid[x][y]==str(0): #If 0 button click can be changed
                if ((x<3 or x>5) and (y<3 or y>5)) or (2<x<6 and 2<y<6): #Making some boxes bg=bg1
                    exec(self.b+'''=Button(text=int(self.originalgrid[x][y]),command=lambda change=False,i=i,self=self: self.click(change,i),
                                  width=4,font=fonttext,bg=bg1,fg=fg1)''') #Executing button with correct details
                    exec(self.b+'.grid(row=x,column=y)')
                else: #Making some boxes bg=bg2
                    exec(self.b+'''=Button(text=int(self.originalgrid[x][y]),command=lambda change=False,i=i,self=self: self.click(change,i),
                                  width=4,font=fonttext,bg=bg2,fg=fg1)''')
                    exec(self.b+'.grid(row=x,column=y)')
            else: #When !=0 click can't change button text
                if ((x<3 or x>5) and (y<3 or y>5)) or (2<x<6 and 2<y<6):
                    exec(self.b+'''=Button(text=int(self.originalgrid[x][y]),command=lambda change=True,i=i,self=self: self.click(change,i),
                                  width=4,font=fonttext,bg=bg1,fg=fg2)''')
                    exec(self.b+'.grid(row=x,column=y)')
                else:
                    exec(self.b+'''=Button(text=int(self.originalgrid[x][y]),command=lambda change=True,i=i,self=self: self.click(change,i),
                                  width=4,font=fonttext,bg=bg2,fg=fg2)''')
                    exec(self.b+'.grid(row=x,column=y)')
            x+=1
        if saveglobal==True: #Only executed when the user is loading a game
            self.count=0 #Variable used to call on button
            for i in range(0,9):
                for x in range(0,9):
                    if self.grid[x][i]!='0' and self.originalgrid[x][i]=='0':
                        self.b='self.b'+str(self.count) #Original sudoku has 0 and grid doesn't
                        exec(self.b+'[\'text\']=int(self.grid[x][i])') #Changes text of the certain button
                    self.count+=1

        self.menuVar=Menu(self.root) #Adding a Menu for easy and recognisable use
        self.root.config(menu=self.menuVar) #Setting Menu
        self.fileMenu=Menu(self.menuVar,tearoff=False)#Adding sub menu called self.fileMenu
        self.menuVar.add_cascade(label='File',menu=self.fileMenu)
        self.fileMenu.add_command(label='Save',command=self.saves)
        self.fileMenu.add_command(label='Load/Delete',command=self.load)
        self.fileMenu.add_command(label='Check',command=self.check)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Quit',command=self.sudoku_quit)
        self.fileMenu.config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)
        self.newMenu=Menu(self.menuVar,tearoff=False)#Adding sub menu called self.newMenu
        self.menuVar.add_cascade(label='New',menu=self.newMenu)#New sudoku being made
        self.newMenu.add_command(label='New:Easy',command=lambda: self.new_sudoku('Easy'))
        self.newMenu.add_command(label='New:Medium',command=lambda: self.new_sudoku('Medium'))
        self.newMenu.add_command(label='New:Hard',command=lambda: self.new_sudoku('Hard'))
        self.newMenu.config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)
        self.second()
        messagebox.showinfo(title="Info", message="Button with the forground "+fg2+" cannot be changed")
        self.root.mainloop()

    def new_sudoku(self,option):#Creates a new sudoku
        self.root.destroy()#destroying the current window
        global difficultchoice,saveglobal#globalise two variables for Sudoku
        saveglobal=False#not loading a Sudoku
        difficultchoice=option#option= Easy, medium or hard
        sudoku()#run class Sudoku

    def load(self):#Creates the screen Loading
        self.root.destroy()#destroy window
        loading()#open loading class

    def saves(self):#Saves the current sudoku
        def back():#When the back button is clicked
            root.destroy()
        def save():#When the save button is clicked
            user=globalUsername
            rows=list(c.execute('SELECT * FROM SavedSudoku WHERE Username =?',[(user)]))
            grid=''.join([''.join(row) for row in self.grid])#Making the grid a string
            if saveglobal==False:#If True save as
                if len(textvar.get())>4:#Name has to be longer than 4 characters
                    if len(rows)<=5:#If there are less than 5 saves
                        currenttime=(time.strftime('%x')+' '+time.strftime('%X'))#Current time and date
                        originalgrid=(''.join([''.join(row) for row in self.originalgrid]))#Making a grid into string
                        exist=c.execute('SELECT * FROM SavedSudoku WHERE SavedName =?',
                                  [(textvar.get())])
                        exist=False
                        for i in range(0,len(rows)):
                            if rows[i][3]==textvar.get():
                                exist=True#Checking to see if the save name already exists
                        if exist==False:#if the user name doesnt already exist the the user's details are transfered to the database and saved
                            c.execute('INSERT INTO SavedSudoku (Username, OriginalSudoku, SavedSudoku, SavedName, DateSaved, Difficulty, Score) VALUES(?,?,?,?,?,?,?)',
                                        (user,originalgrid,grid,textvar.get(),currenttime,difficultchoice,counter))
                            conn.commit()#saving to the database
                            root.destroy()#destroying the save window
                            self.root.destroy()#destroying the sudoku window
                            menu()#calling the class main
                        else:
                            messagebox.showinfo(title='Save',message='Save name taken')#the save name already exists pop up window infroms user
                    else:#the user has 5 saves already and cant store anouther one
                        root.destroy()
                        menu()
                        messagebox.showinfo(title='Save',message='Too many saves, delete some')
                else:#save name isnt greater than 4 charaters 
                    messagebox.showinfo(title='Save',message='SaveName needs to be 4 characters or longer')
            else:#if the sudoku had been saved before
                c.execute('UPDATE SavedSudoku SET SavedSudoku =? WHERE Username =? AND SavedName=?',
                          (grid,user,savelistglobal[3]))#update the sudoku changes
                c.execute('UPDATE SavedSudoku SET Score =? WHERE Username =? AND SavedName=?',
                          (counter,user,savelistglobal[3]))#update the timer
                currenttime=(time.strftime('%x')+' '+time.strftime('%X'))
                c.execute('UPDATE SavedSudoku SET DateSaved =? WHERE Username =? AND SavedName=?',
                          (currenttime,user,savelistglobal[3]))#update the latest save time
                conn.commit()#save changes to database
                self.root.destroy()#destroy window
                menu()#open up menu
                
            
        counter=self.countlabel['text']
        if saveglobal==False:#Creates a window entry box to enter save name, save as methord
            root=Tk()
            root.configure(background=bg1)
            textvar=StringVar(root)#SaveName variable
            Entry(root,textvariable=textvar,font=fonttext).grid(row=0,column=0,columnspan=2)#textbox for the save name to be placed in
            Button(root,text='Save',command=save,bg=bg2,fg=fg1).grid(row=1,column=0)#save button
            Button(root,text='Back',command=back,bg=bg2,fg=fg1).grid(row=1,column=1)#back button
            root.mainloop()
        else:#If already saved 
            save()

        
    def click(self,change,i):#when one of the sudoku grid buttons is pressed
        if change==False:#if the button has been pressed on the sudoku
            y=i//9#getting x and y value of button in list
            x=i%9
            bname='self.b'+str(i)#the name of the button pressed
            value=eval(bname+'[\'text\']')#text of button pressed
            if value+1==10:#if when button pressed the value is >9
                exec(bname+'[\'text\']=-1')#text==-1
            exec(bname+'[\'text\']+=1')#text+=1
            self.grid[x][y]=str(eval(bname+'[\'text\']'))#setting the value in the grid list
        
    def check(self):#when check button is pressed
        check1=list(map(lambda i: True if len(set(self.grid[i]))==len(self.grid[i]) else False,range(0,9)))#checking for any repeats in the list
        check2lst=[[self.grid[i][x] for i in range(0,9)] for x in range(0,9)]#makes a list of all the columns
        check2=list(map(lambda i: True if len(set(check2lst[i]))==len(check2lst[i]) else False,range(0,9)))#checking for any repeats in the list
        boxes=[]
        for i in range(0,8,3):#creating on the boxes in list format
            boxes.append(self.grid[i][:3]+self.grid[i+1][:3]+self.grid[i+2][:3])
            boxes.append(self.grid[i][3:6]+self.grid[i+1][3:6]+self.grid[i+2][3:6])
            boxes.append(self.grid[i][6:]+self.grid[i+1][6:]+self.grid[i+2][6:])
        check3=list(map(lambda i: True if len(set(boxes[i]))==len(boxes[i]) else False,range(0,9)))#checking for any repeats in the boxes
        if all(check1)==True and all(check2)==True and all(check3)==True:#if all checks are true
            if saveglobal==True:#delete the save if it has been saved before
                c.execute('DELETE FROM SavedSudoku WHERE Username=? AND SavedName=?',
                          (savelistglobal[0],savelistglobal[3]))#deleted
            result=int(self.countlabel['text'])#getting the score on the label
            lst=['Easy','Medium','Hard']
            resultindex=lst.index(difficultchoice)
            tabelcolumnindex=resultindex
            username=globalUsername
            rows=list(c.execute("SELECT * FROM Profiles WHERE Username =?",
                                ([globalUsername])))
            resultindex=rows[0][2+resultindex]#getting the old score
            print(result)
            print(resultindex)
            if resultindex>result or resultindex==0:#if the old score is bigger then the new score or result score hasnt been set yet
                tabelcolumn=['Score1','Score2','Score3']
                c.execute('UPDATE Profiles SET '+tabelcolumn[tabelcolumnindex]+' =? WHERE Username=?',([result,username]))
                messagebox.showinfo(title='NEW HIGH SCORE',message='Well done you got a score '+str(result))#pop up messgae to say well done
            else:#else don't update as didnt beat highscore
                messagebox.showinfo(title='Correct',message='Well done you got a score of '+str(result)+' not beating your high score of '+str(resultindex))
            conn.commit()#save the database
            self.root.destroy()#destroy the window
            menu()#open up the menu
        else:#the sudoku is incorrect
            messagebox.showinfo(title='Incorrect',message='There is a problem with your sudoku')

    def second(self):#when a second passes execute this code bring the score up by one each time
        self.countlabel['text']+=1
        self.root.after(1000,self.second)

    def sudoku_quit(self):#when the back button is pressed
        self.root.destroy()#destoy the window
        menu()#open up the menu

class delete():#Done
    def __init__(self):
        self.fonttext=('Times','12','')#set the font and text size to look nice
        self.root=Tk()#creating the window
        self.root.title('Delete')#setting the title of the window to delete
        self.root.geometry('360x200')#making the size of the window 360 by 200
        self.root.configure(background='gray40')#setting the background colour to gray40
        self.usernamestr=StringVar()#creating a string variable for the username
        Label(text='Username',bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=10)
        #username label which informs the user which text box is used to input the username
        self.e1=Entry(textvariable=self.usernamestr,width=30,font=self.fonttext)
        #username entry box which is where the username is input into
        self.e1.place(x=80,y=10)#placing the entry box in the window at x 80 and y 10
        Button(text='Back',command=self.quits,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=10,y=100)
        #creating back button and then placing it on the window
        Button(text='Submit',command=self.submit,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=80,y=100)
        #creating submit button nad then placing it inside the window
        self.confirm=Label(text='',bg='gray40',fg='yellow',font=self.fonttext)
        self.confirm.place(x=190,y=100)
        #confirm lable which will have the value "Deleted account "+ the account name for 3 seconds
        self.root.mainloop()

    def submit(self):#pressing the submit button
        username=self.usernamestr.get()#getting the username from the username text field
        record=c.execute('SELECT * FROM Profiles WHERE Username =?',[(username)])#selecting all from users profile
        for row in record:
            record=row#getting the users profile
        if len(list(record))!=0:#if the user exists in the database
            self.check()#calling the function called check
            allrecord=c.execute('SELECT * FROM Profiles')#select all from profiles in list
            allrecord=list(allrecord)
            c.execute('DELETE FROM Profiles')#delete everything in the profiles
            allrecord.remove(record)#remove the username from the list
            for letter in allrecord:#for loop
                c.execute('INSERT INTO Profiles (Username, Password, Score1, Score2, Score3, Admin) VALUES(?,?,?,?,?,?)',
                          (letter[0],letter[1],letter[2],letter[3],letter[4],letter[5]))
                #place everything back into the table profiles without the profile which is being deleted
                adminPro=letter[5]#getting admin column
            if(adminPro=="False"):
                allrecord=c.execute('SELECT * FROM Settings')#select all from settings profiles as list
                allrecord=list(allrecord)
                c.execute('DELETE FROM Settings')#delete everything from the settings list
                record=[allrecord[i] for i in range(0,len(allrecord)) if allrecord[i][0]==username]
                #getting the record from the settings profile
                allrecord.remove(record[0])#deleteing the record from the settings table
                for letter in allrecord:
                    c.execute('INSERT INTO Settings (Username, Font, TextSize, Other, BgColour1, BgColour2, BgColour3, FgColour1, FgColour2) VALUES(?,?,?,?,?,?,?,?,?)',
                              (letter[0],letter[1],letter[2],letter[3],letter[4],letter[5],letter[6],letter[7],letter[8]))
                        #insert everything back into the table excluding the record which has been deleted
            conn.commit()#save edits made to the database
            self.e1.delete(0,END)#delete everything from the first entry box
        else:#username doesn't exist
            messagebox.showinfo(title='Existance',message='The Username doesn\'t exist')#error message

    def check(self):
        username=self.usernamestr.get()#get the username which was inputted
        if self.confirm['text']=='':#if the text of the label is equal to nothing
            self.confirm['text']='Deleted acount '+username
            #place the label to deleted account+acount name
            self.root.after(3000,self.check)
            #after 3 seconds call the function again
        else:
            self.confirm['text']=''
            #set the text back to nothing
        

    def quits(self):
        self.root.destroy()#close the current window
        adminMenu()#open up the admin menu

class loading():#Done
    def __init__(self):
        self.root=Tk()#Creating the window
        self.root.config(background=bg1)#changing the background colour
        lst=['Save Name','Date Saved','Difficulty','Score','Select']#All of the options needed to save in database
        for i in range(0,len(lst)):#for every coloumn in the table SavedSudoku
            if i==4:#coloumn span is equal to 2
                Label(self.root,text=lst[i],font=fonttext,bg=bg2,fg=fg2,relief='ridge').grid(row=0,column=i+1,sticky='nsew',columnspan=2)
            else:#average label wih a coloumn span of 1
                Label(self.root,text=lst[i],font=fonttext,bg=bg2,fg=fg2,relief='ridge').grid(row=0,column=i+1,sticky='nsew')
        Button(self.root,text='Back',command=self.back,font=fonttext,bg=bg2,fg=fg1,relief='groove').grid(row=1,column=7)
        #adding the back button to the window
        for i in range(1,6):
            Label(self.root,text=str(i),font=fonttext,bg=bg2,fg=fg2,relief='ridge').grid(row=i,column=0,sticky='nsew')
            #adding 1-5 label which shows all of the numbers next to the saves
        self.username=globalUsername#getting the username
        self.saves=list(c.execute('SELECT * FROM SavedSudoku WHERE Username=?',([self.username])))
        #getting all of the saves which the user has
        for i in range(0,len(self.saves)):#for every save that the user has
            Button(self.root,text='Load',command=lambda i=i: self.load(i),bg=bg2,fg=fg1,relief='groove',font=fonttext).grid(row=i+1,column=5)
            Button(self.root,text='Delete',command=lambda i=i: self.delete(i),bg=bg2,fg=fg1,relief='groove',font=fonttext).grid(row=i+1,column=6)
            #adding the load and delete button to every save the user has
            for x in range(0,4):
                Label(self.root,text=self.saves[i][x+3],font=fonttext,bg=bg2,fg=fg2,relief='ridge').grid(row=i+1,column=x+1,sticky='nsew')
                #adding all of the labels which include the save name, time last saved, difficaulty and the current score
        self.root.mainloop()

    def load(self,i):
        global saveglobal,savelistglobal#gobalising two variables which tell if the
        #Sudoku has been saved before and the Sudoku record in the table
        saveglobal=True#the Sudoku has been saved before
        savelistglobal=self.saves[i]#the record sudoku as i is the number in list
        self.root.destroy()#destroy window
        sudoku()#open the Sudoku window

    def back(self):
        self.root.destroy()#destroy current window
        menu()#open the menu window

    def delete(self,i):
        c.execute('DELETE FROM SavedSudoku WHERE Username=? AND SavedName=?',
                  (self.saves[i][0],self.saves[i][3]))#delete the sudoku record selected from table
        conn.commit()#save the edits made to the table
        self.root.destroy()#destroy the current window
        loading()#open loading window

class setting():#Done
    def __init__(self):
        self.root=Tk()#Creating the window
        self.root.title('Settings')#Changing the title window to Settings
        self.root.configure(background=bg1)#changing background colour
        self.colours=['red','blue','green','brown','gray']#colour schemes that the user is able to choose from
        self.colourscheme=[['indian red','light salmon','tomato','black','blue'],['deep sky blue','royal blue','midnight blue','white','yellow'],
                           ['spring green','lawn green','lime green','black','blue'],['wheat','tan','salmon','black','green'],
                           ['grey40','gray56','gray80','white','yellow']]
        self.textlst=['bold','','italic','','underline','']#list of radio buttons that the user can select from
        self.labeltext=['Font:','Text Size:','Colour:','Bold or not:','Italic or not','Underlined or not:']#labels
        for i in range(1,7):#creating the 7 labels and griding the them to the screen
            self.x='self.l'+str(i)#label name
            exec(self.x+'=Label(text=\''+self.labeltext[i-1]+'\',relief=\'ridge\',font=fonttext,bg=bg2,fg=fg2)')
            exec(self.x+'.grid(row=%d,column=0,sticky=\'nsew\')'%(i-1))#placig the button on the screen
        self.var1=StringVar()#setting string variable for first drop down list
        self.var1.set('Times')#the title for the drop down list, the first one to be selected
        self.var2=StringVar()#same process but for 3 different drop down menus
        self.var2.set('8')
        self.var3=StringVar()
        self.var3.set('red')
        self.textfont=OptionMenu(self.root,self.var1,'Times','Courier New','Comic Sans MS','Fixedsys',
                                 'Ms Sans Serif','Ms Serif','Symbol','System','Times New Roman','Verdana')#drop down list of fonts
        self.textfont.grid(row=0,column=1,columnspan=2)#adding drop down list to the screen
        self.textfont.config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)#configuring the settings on drop down menu
        self.textfont['menu'].config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)#configuring the settings in drop down menu
        self.textsize=OptionMenu(self.root,self.var2,'8','10','12','14','16')
        self.textsize.grid(row=1,column=1,columnspan=2)
        self.textsize.config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)
        self.textsize['menu'].config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)
        self.textcolour=OptionMenu(self.root,self.var3,'red','blue','green','brown','gray')
        self.textcolour.grid(row=2,column=1,columnspan=2)
        self.textcolour.config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)
        self.textcolour['menu'].config(font=fonttext,bg=bg2,fg=fg1,activebackground=bg1)
        self.ivar=IntVar()#creating int variable for radio button
        self.bvar=IntVar()
        self.uvar=IntVar()
        self.radiobold1=Radiobutton(text='Bold',font=fonttext,variable=self.bvar,value=0,relief='ridge',bg=bg2).grid(row=3,column=1,sticky='nsew')
        self.radiobold2=Radiobutton(text='Not bold',font=fonttext,variable=self.bvar,value=1,relief='ridge',bg=bg2).grid(row=3,column=2,sticky='nsew')
        self.radioitalic1=Radiobutton(text='Italic',font=fonttext,variable=self.ivar,value=2,relief='ridge',bg=bg2).grid(row=4,column=1,sticky='nsew')
        self.radioitalic2=Radiobutton(text='Not Italic',font=fonttext,variable=self.ivar,value=3,relief='ridge',bg=bg2).grid(row=4,column=2,sticky='nsew')
        self.radiounder1=Radiobutton(text='Underline',font=fonttext,variable=self.uvar,value=4,relief='ridge',bg=bg2).grid(row=5,column=1,sticky='nsew')
        self.radiounder2=Radiobutton(text='Not Underlined',font=fonttext,variable=self.uvar,value=5,relief='ridge',bg=bg2).grid(row=5,column=2,sticky='nsew')
        #radio buttons have been created which have been grouped to make sure that you can only select one, and then adding them to the screen
        self.buttonreset=Button(text='Reset',font=fonttext,command=self.update,relief='groove',bg=bg2,fg=fg1).grid(row=6,column=0,sticky='nsew')
        #add button reset which allows the user to reset the setting meaning that the changes can be made
        self.buttonback=Button(text='Back',font=fonttext,command=self.back,relief='groove',bg=bg2,fg=fg1).grid(row=6,column=1,sticky='nsew')
        #add button back which allows the user to go back to the main menu
        self.labelupdate=Label(text='',font=fonttext,bg=bg1,fg=fg1)#label which will provide count down when the user presses reset
        self.labelupdate.grid(row=6,column=2,sticky='nsew')
        self.root.mainloop()

    def update(self):#command for the reset button
        if self.labelupdate['text']=='':#setting the timer
            self.labelupdate['text']='Restarting in: 5'
            self.root.after(100,self.update2)#calling the function every second until the timer reaches 0
        username=globalUsername#getting the user name of the current user
        temp=self.colours.index(self.var3.get())#getting the colour scheme that the user has choosen
        lst=['Font','TextSize','Other','BgColour1','BgColour2','BgColour3','FgColour1','FgColour2']#list of all the options
        lst2=[self.var1.get(),self.var2.get(),self.textlst[self.bvar.get()]+' '+self.textlst[self.ivar.get()]+' '+self.textlst[self.uvar.get()],
                self.colourscheme[temp][0],self.colourscheme[temp][1],self.colourscheme[temp][2],self.colourscheme[temp][3],
                self.colourscheme[temp][4]]#list of all the selections that the user made
        for i in range(0,len(lst)):#going through all of the selections by the user
            c.execute('UPDATE Settings SET '+lst[i]+' =? WHERE Username =?',(lst2[i],username))#updating the table
        conn.commit()#saving the table from any updates

    def update2(self):#This is the function that is called every second when the function update is initiated
        temp=str(int(self.labelupdate['text'][-1:])-1)#getting the last letter in the label which is the number
        self.labelupdate['text']=self.labelupdate['text'][:-1]+temp#increment the last number
        if self.labelupdate['text'][-1:]!='0':#if the countdown hasn't finished
            self.root.after(1000,self.update2)#carry out the function out again after a second
        else:
            self.root.destroy()#destroy windo
            colours()#load up the colours function to initiate the new changes

    def back(self):
        self.root.destroy()#destroy window
        menu()#open main menu

class leaderboard():#Done
    def __init__(self):
        self.root=Tk()#creating the window
        self.root.title('Leaderboard: Easy')#setting the title
        self.root.configure(background=bg1)#setting background colour from global variable
        self.rvar=IntVar()#setting the int variable of the difficaulty selction
        Radiobutton(text='Easy',font=fonttext,bg=bg2,fg='black',variable=self.rvar,relief='ridge',value=0).grid(row=0,column=0,sticky='nsew')
        #radio button for easy difficaulty setting grid postion to 0,0
        Radiobutton(text='Medium',font=fonttext,bg=bg2,fg='black',variable=self.rvar,relief='ridge',value=1).grid(row=0,column=1,sticky='nsew')
        #radio button for medium difficaulty setting grid postion to 0,1
        Radiobutton(text='Hard',font=fonttext,bg=bg2,fg='black',variable=self.rvar,relief='ridge',value=2).grid(row=0,column=2,sticky='nsew')
        #radio button for hard difficaultly setting grid postion to 0,2
        Button(text='Refresh',font=fonttext,bg=bg2,fg=fg1,command=self.refresh,relief='groove').grid(row=0,column=3,sticky='nsew')
        #button for refresh with the command self.refresh
        Button(text='Back',font=fonttext,bg=bg2,fg=fg1,command=self.back,relief='groove').grid(row=1,column=3,sticky='nsew')
        #back button which leads back to main menu
        self.labelnames=['Postion','Username','Score']#labels needed in the window
        for i in range(0,3):#for loop places the labels on the window
            Label(text=self.labelnames[i],font=fonttext,bg=bg2,fg=fg2,relief='ridge').grid(row=1,column=i,sticky='nsew')
            #places the labels with the label names from lists and places it in a different coloum each time
        self.rows=list(c.execute('SELECT Username,Score1 FROM Profiles WHERE Score1!=? AND Admin=? ORDER BY Score1',(0,"False")))
        #select all of the usernames and scores of score1 as this is what it is pre set as, ordering by score
        self.rows=self.rows[:5]#get only the best 5 scores
        while len(self.rows)<5:#while there is less than 5 scores
            self.rows.append(('',''))#place empty tuples into the list
        self.count=0#setting variable to 0
        for i in range(0,5):#for a loop going through each of the 5 scores
            Label(text=i+1,font=fonttext,bg=bg2,fg=fg2,relief='ridge').grid(row=i+2,column=0,sticky='nsew')
            #placing the postion in each row of the grid 
            for x in range(0,2):#for lopping going through each score
                self.labelname='self.l'+str(self.count)#making the label name for each i in for loop
                exec(self.labelname+'=Label(text=self.rows[i][x],font=fonttext,bg=bg2,fg=fg2,relief=\'ridge\')')
                exec(self.labelname+'.grid(row=i+2,column=x+1,sticky=\'nsew\')')
                #creating the label and placing it in the window
                self.count+=1#incrmenting the count variable
        self.root.mainloop()

    def refresh(self):
        lst=['Score1','Score2','Score3']#the three difficuties name in the database
        lst2=['Easy','Medium','Hard']#the three difficulties in the game
        choice=lst[self.rvar.get()]#getting the score of the difficault the user selected
        self.root.title('Leaderboard: '+lst2[self.rvar.get()])#setting the title to leaderboard and then the difficulty
        rows=list(c.execute('SELECT Username,'+str(choice)+' FROM Profiles WHERE '+str(choice)+'!=? AND Admin=? ORDER BY '+str(choice),([0,"False"])))
        #getting all of the highest scores from the current difficulty the user choose
        count=0
        rows=rows[:5]#getting the top 5 scores
        while len(rows)<5:#when there isn't 5 top scores
            rows.append(("",""))#append the tuple to the list so clears any left over before
        for i in range(0,len(rows)):#for every index in the list rows
            for x in range(0,2):#get the username and score
                labeltext='self.l'+str(count)
                exec(labeltext+'[\'text\']=rows[i][x]')
                #setting the label texts to everything that has been extracted from the database
                count+=1

    def back(self):
        self.root.destroy()#destroy window
        menu()#open up the main menu
        
class menu():#Done
    def __init__(self):
        self.root=Tk()#creating the window
        self.root.title('Menu')#setting the window title to Menu
        self.root.configure(background=bg1)#setting the background colour to the global variable bg1
        self.play=Button(text='Play',width=30,command=self.createboard,bg=bg2,relief='groove',fg=fg1,font=fonttext,pady=4,padx=40).grid(columnspan=3,row=0,column=0)
        self.v=IntVar()#creating an integer variable for the radio buttons
        Radiobutton(text='Easy',variable=self.v,value=0,bg=bg2,relief='ridge',fg='black',font=fonttext,height=1).grid(row=1,column=0)#Easy radio button
        Radiobutton(text='Medium',variable=self.v,value=1,bg=bg2,relief='ridge',fg='black',font=fonttext,height=1).grid(row=1,column=1)#Medium radio button
        Radiobutton(text='Hard',variable=self.v,value=2,bg=bg2,relief='ridge',fg='black',font=fonttext,height=1).grid(row=1,column=2)#Hard radio button
        self.leader=Button(text='Leaderboard',width=30,command=self.leaderboard,bg=bg2,relief='groove',fg=fg1,font=fonttext,pady=4,padx=40).grid(columnspan=3,row=2,column=0)
        self.twoplay=Button(text='Settings',width=30,command=self.settings,bg=bg2,relief='groove',fg=fg1,font=fonttext,pady=4,padx=40).grid(columnspan=3,row=3,column=0)
        self.quitb=Button(text='Quit',width=30,command=self.quits,bg=bg2,relief='groove',fg=fg1,font=fonttext,pady=4,padx=40).grid(columnspan=3,row=4,column=0)
        self.root.mainloop()#main loop for the window

    def createboard(self):#command for when the play button is pressed
        lst=['Easy','Medium','Hard']#list of easy medium and hard, the names of the Sudoku tables
        global difficultchoice,saveglobal#globalising two variables
        saveglobal=False#if Sudoku has been saved before and started up it is false
        difficultchoice=lst[self.v.get()]#difficaulty choice is Easy, Medium or Hard
        self.root.destroy()#destroy the window
        sudoku()#open the Sudoku class

    def leaderboard(self):#when the lederboard button is pressed
        self.root.destroy()#destroy current window
        leaderboard()#open leaderboard

    def settings(self):#when the settings button is pressed
        self.root.destroy()#destroy the current window
        setting()#open settings window

    def quits(self):#when the back button is pressed
        self.root.destroy()#destroy the current window
        login()#open login window as that is the nct window that was last opened

class create():#Done
    def __init__(self):
        self.fonttext=('Times','12','')#the font which is choosen for admins
        self.root=Tk()#creating the window
        self.root.title('Create Account')#setting the the title to create account
        self.root.geometry('330x200')#setting the size of the window
        self.root.configure(background='gray40')#setting the background colour
        self.usernamestr=StringVar()#string variable for the username input
        self.password1str=StringVar()#seting variable for the password1 input
        self.password2str=StringVar()#settig variable for the password2 input
        Label(text='Username',bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=10)
        #label which shows what entry box is for the username 
        Entry(textvariable=self.usernamestr,width=30,font=self.fonttext).place(x=80,y=10)
        #entry box for the username
        Label(text='Password',bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=40)
        #label which shows what entry box is for the password1
        Entry(textvariable=self.password1str,width=30,show='*',font=self.fonttext).place(x=80,y=40)
        #entry box for the password1 shows "*" so no one can see the input
        Label(text='Password',bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=70)
        #label which shows what entry box is for the password2
        Entry(textvariable=self.password2str,width=30,show='*',font=self.fonttext).place(x=80,y=70)
        #entry box for the password2 shows "*" so no one can see the input
        self.radioVar=IntVar()#radio button value for the admin or not
        Label(text="ADMIN",bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=100)
        #showing where the admin radio buttons are
        Radiobutton(text="True",relief='ridge',variable=self.radioVar,value=0,bg='gray56',font=self.fonttext).place(x=80,y=100)
        #first radio button for when the new account is an admin account
        Radiobutton(text="False",relief='ridge',variable=self.radioVar,value=1,bg='gray56',font=self.fonttext).place(x=150,y=100)
        #second radio button for when the new account isn't an admin account
        Button(text='Back',command=self.quits,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=10,y=140)
        #back button for the window
        Button(text='Sign Up',command=self.signup,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=80,y=140)
        #sign up button to create the account with the details inputted by the admin 
        self.root.mainloop()

    def quits(self):
        self.root.destroy()#detroy the current window
        adminMenu()#open up the admin menu window

    def signup(self):#make it so that it checks to see that if the object is true or false to admin.
        password1=self.password1str.get()#getting the text from the password1 text box
        password2=self.password2str.get()#getting the text from the password2 text box
        username=self.usernamestr.get()#getting the text from the username text box
        if password1==password2:#if both of the passwords match
            if len(username)>4 and len(password1)>4:#if both the password and the username are loger than 4 characters
                user=list(c.execute('SELECT * FROM Profiles WHERE Username =?', [(username)]))#getting all from username inputted
                if len(user)!=0:#checking to see if name already exists in the database
                    messagebox.showinfo(title='Username',message='Username already exsits')#error message
                else:
                    adminLst=["True","False"]
                    if self.radioVar.get()==1:#if the admin is equal to false
                        default=['Times','10','','grey40','gray56','gray80','white','yellow']#default values which will be put into settings
                        c.execute('INSERT INTO Settings (Username, Font, TextSize, Other, BgColour1, BgColour2, BgColour3, FgColour1, FgColour2) VALUES(?,?,?,?,?,?,?,?,?)',
                                  (username, default[0], default[1], default[2], default[3], default[4], default[5], default[6], default[7]))
                        #inserting into database the settings
                    c.execute('INSERT INTO Profiles (Username, Password, Score1, Score2, Score3,Admin) VALUES(?,?,?,?,?,?)',
                                (username,password1,0,0,0,adminLst[self.radioVar.get()]))
                    #insert a profile with all of the correct values
                    conn.commit()#save the database edits
                    self.root.destroy()#destroying the window 
                    adminMenu()#open the admin menu
            else:
                messagebox.showinfo(title='Username/Password',message='Username or password is shorter than 4 characters')
                #error message box saying that the username or password is shorter than 4 characters
        else:
            messagebox.showinfo(title='Passwords',message='The two passwords don\'t match')
            #error message box saying that the two passwords don't match
        conn.commit()#save the database edits 

class adminMenu():#Done

    def __init__(self):
        self.fonttext=('Times','12','')#font text as admin can't change settings
        self.root=Tk()#creating the screen
        self.root.configure(background='grey40')#setting the background colour
        self.root.geometry("200x200")#creating the size of the window
        self.root.title("ADMIN MENU")#setting the window title to ADMIN MENU
        self.createBt=Button(text="Create Account",command=self.createAccount,bg='gray56',relief='groove',fg='white',font=self.fonttext,width=19)
        self.createBt.place(x=10,y=20)
        #creating the button called create account and then placing it on the screen
        self.deleteBt=Button(text="Delete Account",command=self.deleteAccount,bg='gray56',relief='groove',fg='white',font=self.fonttext,width=19)
        self.deleteBt.place(x=10,y=80)
        #creating the button called delete account and then placing it on the screen
        self.backBt=Button(text="Back",command=self.back,bg='gray56',relief='groove',fg='white',font=self.fonttext,width=19).place(x=10,y=140)
        #placing a back button on the screen
        self.root.mainloop()

    def back(self):
        self.root.destroy()#destroy the current window
        login()#open up the login window

    def createAccount(self):
        self.root.destroy()#destroy the current window
        create()#open up the create window

    def deleteAccount(self):
        self.root.destroy()#destroy the current window
        delete()#open up the delete window

class login():#Done

    def __init__(self):
        self.fonttext=('Times','12','')
        self.root=Tk()
        self.root.configure(background='grey40')
        self.root.title('Sudoku')
        self.root.geometry('280x240+0+0')
        self.usernamestr=StringVar()
        self.passwordstr=StringVar()
        Label(text='Username: ',bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=10)
        Entry(textvariable=self.usernamestr,font=self.fonttext).place(x=100,y=10)
        Label(text='Password: ',bg='gray56',relief='ridge',fg='yellow',font=self.fonttext).place(x=10,y=50)
        Entry(textvariable=self.passwordstr,show='*',font=self.fonttext).place(x=100,y=50)
        Button(text='Login',command=self.loginb,width=26,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=10,y=90)
        #Button(text='Create account',width=13,command=self.createaccount,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=140,y=90)
        Button(text='Quit',command=self.quits,width=26,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=10,y=130)
        #Button(text='Delete Account',command=self.delete,width=26,bg='gray56',relief='groove',fg='white',font=self.fonttext).place(x=10,y=170)
        self.root.mainloop()

    def loginb(self):
        username=self.usernamestr.get()
        password=self.passwordstr.get()
        user=list(c.execute('SELECT * FROM Profiles WHERE Username =?', [(username)]))
        if len(user)==0:
            messagebox.showinfo(title='Existance',message='The username doens\'t exist')
        else:
            if user[0][1]==password:
                global globalUsername
                globalUsername=username
                self.root.destroy()
                if user[0][5]=="True":
                    adminMenu()
                else:
                    colours()
            else:
                messagebox.showinfo(title='Password/Username',message='The username or password is inccorect')
        conn.commit()

    def quits(self):
        self.root.destroy()

class colours():#Done
    def __init__(self):
        username=globalUsername#get the username of the currenr user
        record=list(c.execute('SELECT * FROM Settings WHERE Username =?',[(username)]))#get all of the users colour settings
        record=record[0]
        global fonttext,bg1,bg2,bg3,fg1,fg2#globalise the colour vairbales to be used in other classes
        fonttext=(record[1],record[2],record[3])#setting font variable
        bg1,bg2,bg3=record[4],record[5],record[6]#all 3 background colours
        fg1,fg2=record[7],record[8]#both the forground variables set
        menu()#open up the menu

class startup():#Done
    def __init__(self):
        lst=['Profiles','Easy','Medium','Hard','Settings','SavedSudoku']
        for i in range(0,len(lst)):
            if i<1:
                default='(Username TEXT, Password TEXT, Score1 INT, Score2 INT, Score3 INT, Admin BOOL)'
            elif i<4:
                default='(Grid TEXT)'
            elif i==4:
                default='(Username TEXT, Font TEXT, TextSize TEXT, Other TEXT, BgColour1 TEXT, BgColour2 TEXT, BgColour3 TEXT, FgColour1 TEXT, FgColour2 TEXT)'
            else:
                default='(Username TEXT, OriginalSudoku TEXT, SavedSudoku TEXT, SavedName TEXT, DateSaved TEXT, Difficulty TEXT, Score INT)'
            try:
                c.execute('CREATE TABLE '+lst[i]+default)
            except sqlite3.OperationalError:
                pass
            else:
                pass
        conn.commit()
        login()

startup()
