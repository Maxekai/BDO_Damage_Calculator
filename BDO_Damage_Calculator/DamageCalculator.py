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
