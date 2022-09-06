import DamageCalculator as dc
# REHACER TODAS LAS COSAS CON PYQT
from tkinter import *
root= Tk()

root.title('BDO Damage Comparer')
leftframe=Frame(root)
leftframe.grid(row=0,column=0,sticky='n')
rightframe=Frame(root)
rightframe.grid(row=0,column=1,rowspan=2)
optionframe=Frame(root)
optionframe.grid(row=1,column=0,sticky='s')

class AttackerList:
    #attacker list. it stores created attackers
    attackers=[]
    attackernames=[]
    leftradbut=[]
    rightradbut=[]
    

    
    @property
    def get_attlist(self):
        return self.attackers
    
    def att_creator(self):
        newrow=[]
        name=nameentry.get()
        data= [stat.get() for stat in entries]
        self.attackernames.append(name)
        Radlist.makebuttons(self.attackernames) #attacker is added to attacker list and button maker is reexecuted to create that attackers button
        Label(leftframe,text=name,font=('Helvetica 10')).grid(row=3+len(self.attackers),column=2)
        for index, name in enumerate(data):
            newrow.append(Label(leftframe,text=name,font=('Helvetica 10')))
            newrow[index].grid(row=3+len(self.attackers),column=3+index)
        self.attackers.append(data)
        
    

class ButtonList(AttackerList):
    #this class adds buttons for attackers whever they are added 
    x=IntVar()
    y=IntVar()
    
    @property
    def xval(self):
        return self.x.get()
    @property
    def yval(self):
        return self.y.get()
    #x and y are class variables to store which attackers are selected
    def makebuttons(self,names):
        for index in range(len(names)):
            radiobutton=Radiobutton(leftframe,variable=self.x,value=index)
            radiobutton.grid(row=3+index,column=0)
        for index in range(len(names)):
            radiobutton=Radiobutton(leftframe,variable=self.y,value=index)
            radiobutton.grid(row=3+index,column=1)
            

class AttackButton(ButtonList):
    def attack_command(self):
        if self.xval!=self.yval:
            att1=dc.Atacante(self.attackers[self.xval])
            att2=dc.Atacante(self.attackers[self.yval])
            chart= dc.ComparOf.Multicompara(att2,att1)
            chart()
            
        else:
            att1=dc.Atacante(self.attackers[self.xval])
            dc.ComparOf.Calcular(att1)
            
def SettingButton():
    global ComparOf
    ComparOf=dc.ComparacionOfensiva(int(settentries[0].get()),int(settentries[1].get()),1,int(settentries[2].get()),int(settentries[3].get()),int(settentries[4].get()),1,int(settentries[5].get()))
    Attbutt.attack_command()
    
def ResetButton():
    #resets chart settings
    defaults={settentries[0]:'300',settentries[1]:'500',settentries[2]:'10',settentries[3]:'800',settentries[4]:'1300',settentries[5]:'20'}
    for k,v in defaults.items():
        k.delete(0,END)
        k.insert(0,str(v))
    SettingButton()
 
    
names=['AP','Human AP','Accuracy','Acc. Rate', 'Skill +Acc%']
labels=[]
entries=[]
List=AttackerList()
Radlist=ButtonList()
Attbutt=AttackButton()

Label(leftframe,text='Name',font=('Helvetica 10')).grid(row=0,column=2)
nameentry=Entry(leftframe,width=20,borderwidth=5,font=('Helvetica 18'),justify='center')
nameentry.grid(row=1,column=2)

Label(leftframe,text='    ').grid(row=0,column=0) #this label makes space for the vertical radio buttons

# Titles and text boxes for each stat
for index, name in enumerate(names):
    labels.append(Label(leftframe,text=name,font=('Helvetica 10')))
    labels[index].grid(row=0,column=3+index)
    entries.append(Entry(leftframe,width=5,borderwidth=5,font=('Helvetica 18'),justify='center'))
    entries[index].grid(row=1,column=3+index)

Label(leftframe,text='1',font=('Helvetica 10'),padx=10).grid(row=0,column=0)
Label(leftframe,text='2',font=('Helvetica 10'),padx=10).grid(row=0,column=1)

#attack button instantiation
Button(leftframe,text='Create Attacker',width=30,borderwidth=5,font=('Helvetica 18'),justify='center',command=List.att_creator).grid(row=2,column=2,columnspan=3)
Button(leftframe,text='Attack',width=15,borderwidth=5,font=('Helvetica 18'),justify='center',command=Attbutt.attack_command).grid(row=2,column=5,columnspan=3)

titulo=Label(rightframe,text='Chart',font=('Helvetica 10'))
titulo.grid(row=0,column=0)
base=Canvas(rightframe,height=800,width=1000)
base.grid(row=1,column=0)

Label(optionframe,text='Chart Settings',font=('Helvetica 16')).grid(row=0,column=0,columnspan=4)

#chart options resetting
settings=['Min DR','Max DR','DR Ticks','Min Eva','Max Eva','EVA Ticks']
defaults=['300','500','10','800','1300','20']
settentries=[]
for index,value in enumerate(settings):
    Label(optionframe,text=settings[index]).grid(row=1+2*(index//3),column=index%3)
    settentries.append(Entry(optionframe,width=10,borderwidth=5,font=('Helvetica 14'),justify='center'))
    settentries[index].grid(row=2+2*(index//3),column=index%3)
    settentries[index].insert(0,defaults[index])

#setting buttons
Button(optionframe,text='Apply',width=10,borderwidth=5,font=('Helvetica 14'),justify='center',command=SettingButton).grid(row=1,column=3,rowspan=3)
Button(optionframe,text='Reset',width=10,borderwidth=5,font=('Helvetica 14'),justify='center',command=ResetButton).grid(row=3,column=3,rowspan=2)

#gui main loop
root.mainloop()