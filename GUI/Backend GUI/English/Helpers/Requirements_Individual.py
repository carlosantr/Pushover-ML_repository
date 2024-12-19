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

from .SCWB_requirement import comprobacion_norma
from numpy import round

#%%Formato de entrada
def comprobacion_formato(variables):
    variables_transformadas = {}
    cumplimiento = "SI"
    for var in variables.keys():
        if variables[var] != "":#Verificar si contiene algo
            if var in ["Nx", "Ny"]:
                if (variables[var].get()).isdigit():#Verificar que sea un número entero positivo
                    variables_transformadas[var]=int(variables[var].get())
                else:
                    cumplimiento = f"{var} must be a positive integer"
                    break
            else:
                try:
                    variables_transformadas[var]=float(variables[var].get())
                except:
                    cumplimiento = f"{var} must be a valid number"  
                    break
            if variables_transformadas[var]<=0:
                cumplimiento = f"{var} must be a number greater than 0"  
                break
        else:
            cumplimiento = f"There is not input value for {var}" 
            break
    return variables_transformadas, cumplimiento

#%%RANGOS
def comprobacion_rangos(variables):
    rangos ={'Ny':[2,5],
             'Nx':[2,5],
             'Ly':[2.5,4],
             'Lx':[4,8],
             'Fc':[17,35],
             'W':[10,30],
             'B':[0.25,0.5],
             'H':[0.3,0.65],
             'Cuantia_C':[1,2.8],
             'Cuantia_V_Sup':[0.5,1.3],
             'Cuantia_V_Inf':[0.33,1]}
    cumplimiento = "SI"
    for var in variables.keys():
        if (variables[var] < rangos[var][0])|(variables[var] > rangos[var][1]):
            if var == "Cuantia_C":var_txt='ρc'
            elif var == "Cuantia_V_Sup":var_txt='ρb-top'
            elif var == "Cuantia_V_Inf":var_txt='ρb-bot'
            else: var_txt=var
            cumplimiento = f"Out of range for input variable {var_txt} ({rangos[var]})"
            break
    return cumplimiento

#%%Comprobacion norma
def comprobacion_norma_general(variables):
    LimH1=round(float(0.05*round((variables["Lx"]/16)/0.05)),2)#Beam height limit 1
    LimH2=round(float(0.05*round((variables["Lx"]/12)/0.05)),2)#Beam height limit 2
    LimB1=round(float(0.05*round((variables["H"]/1.4)/0.05)),2)#Beam base limit 1
    LimB2=round(float(0.05*round((variables["H"]/1.2)/0.05)),2)#Beam base limit 2
    cumplimiento = "SI"
    #C.21.3.5.1
    if variables["B"]<0.25:
        cumplimiento = "Does not comply with the requirement C.21.3.5.1 (NSR-10)\n(B >= 0.25m)"
    #C.9.5.2.1
    if (variables["H"]<LimH1)|(variables["H"]>LimH2):
        cumplimiento = "Does not comply with the requirement C.9.5.2.1 (NSR-10)\n(Lx/12 >= H >= Lx/16)"
    #C.10.4.1
    if variables["Lx"]/variables["B"]>50:
        cumplimiento = "Does not comply with the requirement C.10.4.1 (NSR-10)\n(Lx/B > 50)"
    #Altura/Base
    if (variables["B"]<LimB1)|(variables["B"]>LimB2):
        cumplimiento = "It does not comply with the relationship between the height and base of beams\n(H/1.4 >= B >= H/1.2)"
    #C.3.21.3.6.2.2
    OK, n_barras_C, num_barra_C, n_barras_V, num_barra_V = comprobacion_norma(variables, "Individual")
    if OK == 0:
        cumplimiento = "Does not comply with the requirement C.3.21.3.6.2.2 [SCWB]\n(Mnc >= 1.2Mnb)"
    return cumplimiento, n_barras_C, num_barra_C, n_barras_V, num_barra_V

#%%Comprobacion
def comprobacion_completo_individual(variables):
    variables_transformadas, cumplimiento = comprobacion_formato(variables)
    if cumplimiento=="SI":#Comprobación de formato
        cumplimiento = comprobacion_rangos(variables_transformadas)
        if cumplimiento=="SI":#Comprobación rango
            variables_transformadas["Fc"]=variables_transformadas["Fc"]*1000
            variables_transformadas["Cuantia_C"]=variables_transformadas["Cuantia_C"]/100
            variables_transformadas["Cuantia_V_Sup"]=variables_transformadas["Cuantia_V_Sup"]/100
            variables_transformadas["Cuantia_V_Inf"]=variables_transformadas["Cuantia_V_Inf"]/100
            cumplimiento, n_barras_C, num_barra_C, n_barras_V, num_barra_V = comprobacion_norma_general(variables_transformadas)
            if cumplimiento=="SI":#Comprobación de norma
                return (cumplimiento, variables_transformadas, n_barras_C, num_barra_C, n_barras_V, num_barra_V)
            else:
                return (cumplimiento)
        else:
            return (cumplimiento)
    else:
        return (cumplimiento)
