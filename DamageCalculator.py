import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap, Normalize
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as colors


spectral= cm.get_cmap('Spectral')

plt.style.use('ggplot')

Atacantes=[]
Defensores=[]

class Atacante():
    '''Class for each attacker. Their stats are created only once and can only be accessed, not modified'''
    def __init__(self,stats):
        Atacantes.append(self)
        self.AP=int(stats[0])
        self.HumanDamage=int(stats[1])
        self.Acc=int(stats[2])
        self.SkillAcc=int(stats[3])
        self.BonusAcc=int(stats[4])
    
        
    @property
    def EffectiveAP(self):
        return self.AP + self.HumanDamage*0.85
    
    @property
    def EffectiveAcc(self):
        return self.Acc + (self.SkillAcc + self.BonusAcc)*4
             
        
class Defensor:
    '''Not yet implemented in GUI'''
    def __init__(self,dr,eva,bonuseva):
        Defensores.append(self)
        self.DR=dr
        self.Eva=eva
        self.BonusEva=bonuseva
        
    @property
    def EffectiveEva(self):
        return self.Eva + self.BonusEva*5      

class ComparacionUnica:
    '''Class with basic calculations'''
    
    def HitRate(self,acc,eva):
        hitrate =  (1200+5*acc-4*eva)/2000
        if hitrate <0.1:
            return 0.1
        if hitrate >1:
            return 1
        else:
            return hitrate
        
    def RawDamage(self, ap, dr):
        raw=7.919-(0.6214*dr)+(0.272*ap)+(0.005165*(dr**2))-(0.00003649*(ap*dr))-(0.0000258*(dr**3))+(0.000001725*((dr**2)*ap))+(0.00000005595*(dr**4))-(0.00000001078*(dr**3)*ap)-((4.314e-11)*(dr**5))+(1.365e-11*(dr**4)*ap)
        return raw
    
    def VectorDamage(self,apef,accef,evaef,dr):
        ap=apef
        acc= accef
        dr=dr
        eva= evaef
        hr= self.HitRate(acc,eva)
        raw= self.RawDamage(ap,dr)
        return raw*hr

class ComparacionOfensiva(ComparacionUnica):
    '''Class that creates the actual comparation for offensive comparation'''
    def __init__(self,mindr,maxdr,stepdr,tickdr,mineva,maxeva,stepeva,tickeva):
        self.mindr , self.maxdr = mindr, maxdr
        self.mineva, self.maxeva = mineva, maxeva
        self.numejedr , self.numejeeva =int(((maxdr-mindr)/stepdr))+1 , int(((maxeva-mineva)/stepeva))+1
        self.ejedr , self.ejeeva =np.linspace(mindr,maxdr,self.numejedr) , np.linspace(mineva,maxeva,self.numejeeva)
        self.tickdr=tickdr
        self.tickeva=tickeva

    def Comparar(self,atacante):
        '''Creates a new comparation, but no charting'''
        ap=atacante.EffectiveAP
        acc=atacante.EffectiveAcc
        DamageVectorized= np.vectorize(self.VectorDamage)
        return DamageVectorized(ap,acc,self.ejeeva[:,np.newaxis],self.ejedr)
        
    def Calcular(self,atacante):
        '''Compares and charts damage'''
        resultado= self.Comparar(atacante)
        self.Pintar(resultado)
        
    def Multicompara(self,atacante1,atacante2):
        '''Used to compare between two attackers'''
        a1=self.Comparar(atacante1)
        a2=self.Comparar(atacante2)
        resultado=a1/a2
        self.Pintar(resultado)
        
    def Pintar(self,resultado):
        fig, ax = plt.subplots()
        fig.set_figheight(8)
        fig.set_figwidth(10)
        plt.colorbar(ax.contourf(self.ejedr, self.ejeeva,resultado,cmap=spectral,levels=16))
        ax.set_xticks(np.arange(self.mindr,self.maxdr+1,self.tickdr))
        ax.set_yticks(np.arange(self.mineva,self.maxeva+1,self.tickeva))
        plt.ylabel('Eva Total')
        plt.xlabel('DR')
        chart=FigureCanvasTkAgg(fig,rightframe)
        chart.get_tk_widget().grid(column=0,row=1)
        
        
class ComparacionDefensiva(ComparacionUnica):
    '''Not yet implemented in GUI. Works the same as Offensive Comparing but using defensive stats'''
    def __init__(self,minap,maxap,stepap,minacc,maxacc,stepacc):
        self.minap , self.maxap= minap,maxap
        self.minacc , self.maxacc = minacc , maxacc
        self.numejeap, self.numejeacc= int(((maxap-minap)/stepap))+1 , int(((maxacc-minacc)/stepacc))+1
        self.ejeap , self.ejeacc =np.linspace(minap,maxap,self.numejeap) , np.linspace(minacc,maxacc,self.numejeacc)
        
    def Comparar(self,defensor):
        dr=defensor.DR
        eva=defensor.EffectiveEva
        DamageVectorized=np.vectorize(self.VectorDamage)
        return DamageVectorized(self.ejeap,self.ejeacc[:,np.newaxis],eva,dr)
    
    def Multicompara(self,defensor1,defensor2):
        a1=self.Comparar(defensor1)
        a2=self.Comparar(defensor2)
        resultado=a1/a2
        self.Pintar(resultado)
    
    def Calcular(self,defensor):
        resultado= self.Comparar(defensor)
        self.Pintar(resultado)

    def Pintar(self,resultado):
        fig, ax = plt.subplots()
        plt.colorbar(ax.contourf(self.ejeap, self.ejeacc,resultado,cmap=spectral,levels=16))
        plt.ylabel('Acc Total')
        plt.xlabel('AP')
        ax.set_xticks(np.arange(self.minap,self.maxap+1,10))
        ax.set_yticks(np.arange(self.minacc,self.maxacc+1,20))
        ax.plot(417,795,marker='.')
        plt.show() 
            
  
  
#Chart default settings
ComparOf=ComparacionOfensiva(300,500,1,10,800,1300,1,20)
ComparDef=ComparacionDefensiva(300,500,1,700,900,1)



#GUI

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
            dc.ComparOf.Multicompara(att2,att1)
            
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