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

from tkinter import Tk, Frame, Label, Button, Entry, Checkbutton, StringVar, IntVar
from Helpers.Press_Button import Press_Prediction_Individual, press_help, Press_Input_Multiple, Press_Check_Multiple, Press_Prediction_Multiple

Entradas = {'Ny':'Ny','Nx':'Nx','Ly':'Ly','Lx':'Lx','Fc':'Fc','W':'W','B':'B','H':'H',
           'Cuantia_C':'ρc','Cuantia_V_Sup':'ρb-top','Cuantia_V_Inf':'ρb-bot'}
ML_models = ["ANN", "RF", "GBM", "LASSO"]

#%%Configuración básica
Win = Tk()
#Definiendo tamaño de pantalla
Win.geometry("770x690")#Interface size
Win.resizable(False, False)
#Ícono y fondo
Win.config(bg="#919191")#Color
Win.title("Pushover-ML")

#%% Frame estructura
secS_frame=Frame(Win,width="228",height="242.5")#Creating frame
secS_frame.place(x=190,y=5)#Position
secS_frame.config(bg="#EEEEEE")#Color
secS_frame.config(bd=1)#Border
secS_frame.config(relief="solid")
Label(secS_frame,text="Estructura",fg="#0C0268",font=("Arial Black",15)).place(x=53,y=0)#Title of the frame (text)

#%% Frame columna
secC_frame=Frame(Win,width="228",height="193.5")#Creating frame
secC_frame.place(x=190,y=252.5)#Position
secC_frame.config(bg="#EEEEEE")#Color
secC_frame.config(bd=1)#Border
secC_frame.config(relief="solid")
Label(secC_frame,text="Columnas",fg="#0C0268",font=("Arial Black",15)).place(x=56,y=0)#Title of the frame (text)

#%% Section Column Frame
secB_frame=Frame(Win,width="228",height="193.5")#Creating frame
secB_frame.place(x=190,y=451)#Position
secB_frame.config(bg="#EEEEEE")#Color
secB_frame.config(bd=1)#Border
secB_frame.config(relief="solid")
Label(secB_frame,text="Vigas",fg="#0C0268",font=("Arial Black",15)).place(x=78,y=0)#Title of the frame (text)

#%% Frame curva Pushover predecida
pc_frame=Frame(Win,width="342.5",height="360")#Creating frame
pc_frame.place(x=423,y=5)#Position
pc_frame.config(bg="#EEEEEE")#Color
pc_frame.config(bd=1)#Border
pc_frame.config(relief="solid")
Label(pc_frame,text="Predicción",fg="#0C0268",font=("Arial Black",15)).place(x=110,y=0)#Title of the frame (text)

#%% Frame resultados
res_frame=Frame(Win,width="342.5",height="275")#Creating frame
res_frame.place(x=423,y=370)#Position
res_frame.config(bg="#EEEEEE")#Color
res_frame.config(bd=1)#Border
res_frame.config(relief="solid")
Label(res_frame,text="Resultados",fg="#0C0268",font=("Arial Black",15)).place(x=106.5,y=0)#Title of the frame (text)

#%%Frame entradas
#Pestaña
in_frame=Frame(Win,width="180",height=f"{650-10}")#Creating frame
in_frame.place(x=5,y=5)#Position
in_frame.config(bg="#EEEEEE")#Color
in_frame.config(bd=1)#Border
in_frame.config(relief="solid")
#Titulo
Label(in_frame,text="Entradas",
      fg="#0C0268",font=("Arial Black",15)).place(x=36,y=0) #Title of the frame (text)
#Guardar entradas
variables = {key: StringVar() for key in Entradas.keys()}
models_check = {opcion: IntVar() for opcion in ML_models}
#Generar las entradas y etiquetas
x_in=75
y_in=37.5
for key, label in Entradas.items():
    Entry(in_frame, textvariable=variables[key], justify="center").place(x=x_in-50,y=y_in+22)
    boton_ayuda = Button(in_frame, text="?",command=lambda k=key, l=label: press_help(k, l),width=1,height=1,font=("Arial", 6))
    boton_ayuda.place(x=x_in+78, y=y_in+22.5)
    if label in ["B","H"]:
        x_in=81
    elif label in ['ρb-top','ρb-bot']:
        x_in=65
    else:
        x_in=77.5
    Label(in_frame, text=label).place(x=x_in,y=y_in)
    y_in+=41
    x_in=75
y_in+=15
for idx,opcion in enumerate(ML_models):
    Label(in_frame, text=opcion).place(x=x_in-25,y=y_in)
    Checkbutton(in_frame, variable=models_check[opcion]).place(x=x_in+25,y=y_in)
    y_in+=20
#Botón de predict
button=Button(in_frame,text="Predecir",command=lambda: Press_Prediction_Individual(variables, secS_frame, secC_frame, secB_frame, pc_frame, res_frame, models_check),
                 width=10,bg="#C0C0C0",fg="#0C0268",font=("Arial Black",9)).place(x=x_in-32,y=y_in+15)

#%%Multiple section
mul_frame=Frame(Win,width="760",height="35")#Creating frame
mul_frame.place(x=5,y=650)#Position
mul_frame.config(bg="#EEEEEE")#Color
mul_frame.config(bd=1)#Border
mul_frame.config(relief="solid")
Label(mul_frame,text="Modo múltiple:",fg="#0C0268",font=("Arial Black",13)).place(x=17,y=0)#Title of the frame (text)

button=Button(mul_frame,text="Ingresar datos (.xlsx)",command=lambda: Press_Input_Multiple(),
                 width=20,bg="#C0C0C0",fg="#0C0268",font=("Arial Black",8)).place(x=195,y=2.5)
button=Button(mul_frame,text="Requerimientos",command=lambda: Press_Check_Multiple(),
                 width=20,bg="#C0C0C0",fg="#0C0268",font=("Arial Black",8)).place(x=383,y=2.5)
button=Button(mul_frame,text="Predecir - Multiple",command=lambda: Press_Prediction_Multiple(models_check),
                 width=20,bg="#C0C0C0",fg="#0C0268",font=("Arial Black",8)).place(x=570,y=2.5)
boton_ayuda = Button(mul_frame, text="?",command=lambda: press_help("Multiple prediction", None),width=1,height=1,font=("Arial", 6))
boton_ayuda.place(x=168, y=7)

#%%Bucle principal
Win.mainloop()