# Copyright 2024, Carlos Emilio Angarita Trillos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from numpy import float_, array, zeros, round_, random, abs
from pandas import DataFrame

#%%Diagrama de interacción
def interaction_diagram_kN(b,h,recub,nLineasAcero,nBarras,ABarras,fc,fy):#Este código genera el diagrama de interacción de una columna
    #Encontrando posicion de y área de lineas de acero
    As=[]
    pos=[]#Posicion de lineas de barras de acero definidas en As
    nBarras=float_(nBarras)
    for i in range(0,nLineasAcero):
        pos.append(recub+i*(h-2*recub)/(nLineasAcero-1))
        As.append(nBarras[i]*ABarras[i])    
    Es=210000000; #modulo de elasticidad del acero
    ec=0.003; #del concreto
    es=fy/Es; #del acero
    pos=array(pos)
    As=array(As)
    if (len(pos)!=len(As)):
        print('ERROR: numero de barras no coincide con su ubicacion')    
    else: 
        c=[] #puntos al eje neutro
        for i in range(1,101):
            c.append(h*i/100)
        points = len(c)
        yg = h/2; #posicion del centroide
        arm=yg-array(pos) #brazo de las barras de acero
        Ts = -sum(As)*fy #maxima fuerza de tension sin momento
        Pc = 0.8*(0.85*fc*(b*h-sum(As))+sum(As)*fy) #maxima fuerza de compresion sin momento
        ei=[];fi=[];
        fs=zeros((points,len(pos)));
        Fi=[];Fs=[];Mi=[];Ms=[]
        Fc=[];Mc=[];Pt=[];Pn=[];Mn=[];phi=[]
        for i in range(points):
            ci=c[i]
            ei.append(ec*(1-(pos/ci)))
            fi.append(ei[i]*Es)
            for j in range(len(pos)):
                if (fi[i][j]<-fy):
                    fs[i][j]=-fy
                elif (fi[i][j]>fy):
                    fs[i][j]=fy
                else:
                    fs[i][j]=fi[i][j]
            Fi.append(array(fs[i][:])*As)
            Fs.append(sum(Fi[i][:]))
            Mi.append(Fi[i][:]*arm)
            Ms.append(sum(Mi[i][:]))
            Fc.append(0.85*fc*0.85*ci*b)
            Mc.append(Fc[i]*(yg-0.85*ci/2))
            Pt.append(Fc[i]+Fs[i])
            Pn.append(min(Pt[i],Pc))
            Mn.append(Mc[i]+Ms[i])
            phi.append(0.65+(-ei[i][-1]-es)*250/3)
            if (phi[i]<0.65):
                phi[i]=0.65
            elif(phi[i]>0.9):
                phi[i]=0.9
            else:
                phi[i]=phi[i]
        phi.insert(0,0.9);phi.append(0.65)
        Pn.insert(0,Ts);Pn.append(Pc)
        M1=sum(As*arm*-fy)
        Mn.insert(0,M1);Mn.append(0)
        Pn=array(Pn)
        Mn=array(Mn)
        # plt.plot(Mn,Pn)
        # plt.xlabel('Moment (kN-m)')
        # plt.ylabel('Axial load (kN)')
        # plt.title('Interaction Diagram')
        return Pn[Mn>=0],Mn[Mn>=0]

#%%Asignación de refuerzo        
def DimRefuerzo(Base,Area,Elemento):#Esta función define una distribución de barras común en la sección (barras comerciales) que se asemejen al acero requerido según la cuantía
    n_barras=[];A_barras=[];nT=[];nB=[];nLineasAcero=0;
    n_posibilidad=[]
    A_posibilidad=[]
    nLineas_posibilidad=[]
    nums_barras=[]
    #Tabla de barras de refuerzo
    table=DataFrame([
        [2,3,4,5,6,7,8],#Número de barra
        [0.32,0.71,1.29,1.99,2.84,3.87,5.1],#Área en cm²
        ])
    table=table.transpose()
    table=table.rename(columns={0:'#Barra',1:'Area'})
    table['Area']=table['Area']/10000
    table['Lim4']=table['Area']*4
    table['Lim6']=table['Area']*6
    table['Lim8']=table['Area']*8
    table['Lim10']=table['Area']*10
    table['Lim12']=table['Area']*12
    table['Lim14']=table['Area']*14
    #Encontrando la mejor combinación de barras para COLUMNAS
    if (Elemento=='Columna'):#En cada ciclo se encuentra una combinación diferente, y de manera aleatoria al final se elige una combinación que se ajuste a la cantidad de acero requerido
        if (Base<=0.3):
            for i in range(2,len(table)):#A
                if(Area<=table.loc[i,'Lim4']):#Asigna 4 barras que mejor se ajusten
                    n_posibilidad.append([2,2])
                    A_posibilidad.append([table.loc[i,'Area'],table.loc[i,'Area']])
                    nLineas_posibilidad.append(2)
                    nums_barras.append(table.loc[i,"#Barra"])
                    break
        for p in range(2,len(table)):#C
            if(Area<=table.loc[p,'Lim8']):#Asigna 8 barras que mejor se ajusten
                n_posibilidad.append([3,2,3])
                A_posibilidad.append([table.loc[p,'Area'],table.loc[p,'Area'],table.loc[p,'Area']])
                nLineas_posibilidad.append(3)
                nums_barras.append(table.loc[p,"#Barra"])
                break
        if (Base>=0.35):
            for u in range(2,len(table)):#E
                if(Area<=table.loc[u,'Lim12']):#Asigna 12 barras que mejor se ajusten
                    n_posibilidad.append([4,2,2,4])
                    A_posibilidad.append([table.loc[u,'Area'],table.loc[u,'Area'],table.loc[u,'Area'],table.loc[u,'Area']])
                    nLineas_posibilidad.append(4)
                    nums_barras.append(table.loc[u,"#Barra"])
                    break
        #Selección aleatoria de combinación de barras de acero
        idx=round_(random.uniform(0.5,len(n_posibilidad)+0.5)).astype(int)
        n_barras.append(n_posibilidad[idx-1])
        A_barras.append(A_posibilidad[idx-1])
        nLineasAcero=nLineas_posibilidad[idx-1]
        num_barra = nums_barras[idx-1]
    #Encontrando la mejor combinación de barras para VIGAS                                                  
    if(Elemento=='Viga'):
        #Recorre números de barra y cantidades de barras para encontrar una combinación para el acero superior
        for j in range(2,10):#Asignar máximo 9 barras arriba
            for i in range(1,len(table)):
                if(Area[0]<=j*table.loc[i,'Area']):
                    nT=[j,table.loc[i,'Area']]#Número de barras y área
                    nums_barras.append(table.loc[i,"#Barra"])
                    break
            if (len(nT)>0):
                break  
        #Recorre números de barra y cantidades de barras para encontrar una combinación para el acero inferior
        for j in range(2,9):#Asignar máximo 8 barras abajo
            for i in range(1,len(table)):    
                if(Area[1]<=j*table.loc[i,'Area']):
                    nB=[j,table.loc[i,'Area']]#Número de barras y área
                    nums_barras.append(table.loc[i,"#Barra"])
                    break
            if (len(nB)>0):
                break
        #Almacenando resultados
        n_barras.append([nT[0],0,nB[0]])
        A_barras.append([nT[1],0,nB[1]])
        
        nLineasAcero=2
        num_barra = nums_barras
    #Regresando el número de barras (superior, intermedia e inferior), sus áreas y el número de líneas de acero que tendrá la sección
    return n_barras[0], A_barras[0], nLineasAcero, num_barra

#%%Comprobación de norma
def comprobacion_norma(variables, mode):#Esta función se encarga de definir si la combinación de parámetros del edificio creado, cumple o no con el criterio de columna fuerte - viga débil
    #Definiendo variables
    B_vig=variables["B"]
    H_vig=variables["H"]
    recub=0.05
    Fy=420000
    Fc=variables["Fc"]
    w=variables["W"]
    Lx=variables["Lx"]
    Cuantia_Vig_Sup=variables["Cuantia_V_Sup"]
    Cuantia_Vig_Inf=variables["Cuantia_V_Inf"]
    Cuantia_Col=variables["Cuantia_C"]
    #Variables de cumplimiento
    OK=0 #General
    OKV=0 #Viga
    OKC=0 #Columna
    #CRITERIO 1
    As_V=Cuantia_Vig_Sup*B_vig*(H_vig-recub)#Área de acero arriba y abajo
    Mn_V = As_V*Fy*((H_vig-recub)-(As_V*Fy/(Fc*B_vig)))#Momento de la viga
    if(Mn_V>=(w*(Lx**2)/12)):#Comprobacion del momento nominal de la viga con WL²/11
        OKV=1
    #CRITERIO 2 
    B_col=B_vig;H_col=B_col  
    As_C=Cuantia_Col*B_col*H_col#Área de acero de columna
    n_barras_C,A_barras_C,nLineasAcero_C,num_barra_C=DimRefuerzo(B_col,As_C,'Columna')#Número de barras y áreas de columnas
    Point_Diagrama=0.15*Fc*(B_col*H_col)#Aproximación para el momento del diagrama de interacción para comprobar SCWB
    Pd,Md=interaction_diagram_kN(B_col, H_col, recub, nLineasAcero_C, n_barras_C, A_barras_C, Fc, Fy)
    index_near=(abs(Point_Diagrama-Pd)).argmin()
    #Interpolando entre puntos del diagrama de interacción, para encontrar el momento nominal exacto
    if (Pd[index_near]<Point_Diagrama):
        m=(Md[index_near+1]-Md[index_near])/(Pd[index_near+1]-Pd[index_near])
        Mn_C = Md[index_near]+((Point_Diagrama-Pd[index_near])*m)#Momento nominal de columna
    else:
        m=(Md[index_near]-Md[index_near-1])/(Pd[index_near]-Pd[index_near-1])
        Mn_C = Md[index_near]+((Pd[index_near]-Point_Diagrama)*m)#Momento nominal de columna
    #Comprobacion de SCWB
    if(Mn_C>1.2*Mn_V):
        OKC=1
    #¿CUMPLE?
    if(OKV==OKC==1):
        OK=1
    #Sacar diseño de vigas
    As_V_both=[Cuantia_Vig_Sup*B_vig*(H_vig-recub),Cuantia_Vig_Inf*B_vig*(H_vig-recub)] #Acero necesario en la parte superior e inferior de la viga
    n_barras_V,A_barras_V,nLineasAcero_V,num_barra_V=DimRefuerzo(B_col,As_V_both,'Viga')#Número de barras y áreas de columnas
    if mode=="Individual":
        return OK, n_barras_C, num_barra_C, n_barras_V, num_barra_V
    elif mode=="Multiple":
        Cuantia_Real_C = (sum(n_barras_C)*A_barras_C[0])/(B_col*H_col)
        Cuantia_Real_B_Top = (n_barras_V[0]*A_barras_V[0])/(B_vig*(H_vig-recub))
        Cuantia_Real_B_Bot = (n_barras_V[-1]*A_barras_V[-1])/(B_vig*(H_vig-recub))
        return OK, Cuantia_Real_C, Cuantia_Real_B_Top, Cuantia_Real_B_Bot

