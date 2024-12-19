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

#%%Comprobacion estructura - data
def comprobacion_structure(data):
    cumplimiento = "SI"
    expected_cols = ['Ny', 'Nx', 'Ly', 'Lx', 'Fc', 'W', 'B', 'H', 'Rr_Column', 'Rr_Beam_top', 'Rr_Beam_bot']
    actual_cols = list(data.columns)
    if set(actual_cols) == set(expected_cols):
        data = data[expected_cols]
    else:
        missing_cols = set(expected_cols) - set(actual_cols)
        extra_cols = set(actual_cols) - set(expected_cols)
        cumplimiento = "Incorrect data structure:\n"
        if missing_cols:
            cumplimiento += f"The data has missing columns: ({', '.join(missing_cols)})\n"
        if extra_cols:
            cumplimiento += f"The data has extra columns: ({', '.join(extra_cols)})\n"
    return data, cumplimiento


#%%Formato de entrada
def comprobacion_formato(data):
    cumplimiento = "SI"
    error_message = ""
    #Comprobar si hay filas con información vacía
    filas_vacias = data[data.isnull().any(axis=1)]
    if not filas_vacias.empty:
        indices_vacios = (filas_vacias.index + 1).tolist() # Obtener los índices de las filas vacías
        error_message += f"* Empty data in rows: {', '.join(map(str, indices_vacios))}\n"
    #Comprobar formato de columnas
    for var in data.columns:
        if var in ["Nx", "Ny"]:  # Integer
            # Verificar enteros positivos
            filas_no_enteros_positivos = data[~data[var].apply(lambda x: isinstance(x, (int, float)) and x > 0 and (isinstance(x, int) or (isinstance(x, float) and x.is_integer())))]
            indices_no_enteros_positivos = filas_no_enteros_positivos.index.tolist()
            if not filas_no_enteros_positivos.empty:
                error_message += f"* {var} values must be a positive integer: Check rows {', '.join(map(str, [i + 1 for i in indices_no_enteros_positivos]))}\n"
        else: #Valores no válidos
            filas_no_floats = data[~data[var].apply(lambda x: isinstance(x, (int, float)) and x > 0)]
            indices_no_floats = filas_no_floats.index.tolist()
            if not filas_no_floats.empty:
                error_message += f"* {var} contains non-numeric or negative values: Check rows {', '.join(map(str, [i + 1 for i in indices_no_floats]))}\n"            
    if error_message != "":
        cumplimiento = error_message
    return cumplimiento

#%%RANGOS
def comprobacion_rangos(data, rangos):
    cumplimiento = "SI"
    error_message = ""
    for var in data.columns:
        if var == "Cuantia_C":var_txt='ρc'
        elif var == "Cuantia_V_Sup":var_txt='ρb-top'
        elif var == "Cuantia_V_Inf":var_txt='ρb-bot'
        else: var_txt=var
        filas_fuera_rango = data[(data[var] < rangos[var][0]) | (data[var] > rangos[var][1])]
        indices_fuera_rango = filas_fuera_rango.index.tolist()
        if not filas_fuera_rango.empty:
            error_message += f"* {var_txt} out of range ({rangos[var]}): Check rows {', '.join(map(str, [i + 1 for i in indices_fuera_rango]))}\n"
    if error_message != "":
        cumplimiento = error_message
    return cumplimiento

#%%Comprobacion norma
def comprobacion_norma_general(data):
    cumplimiento = "SI"
    error_message = ""
    Rr_Real_C_list, Rr_Real_B_Top_list, Rr_Real_B_Bot_list = [], [], []
    for i in range(len(data)):
        msg_i=""
        LimH1=round(float(0.05*round((data.loc[i,"Lx"]/16)/0.05)),2)#Beam height limit 1
        LimH2=round(float(0.05*round((data.loc[i,"Lx"]/12)/0.05)),2)#Beam height limit 2
        LimB1=round(float(0.05*round((data.loc[i,"H"]/1.4)/0.05)),2)#Beam base limit 1
        LimB2=round(float(0.05*round((data.loc[i,"H"]/1.2)/0.05)),2)#Beam base limit 2
        #C.21.3.5.1
        if data.loc[i,"B"]<0.25:
            msg_i += "Does not comply with the requirement C.21.3.5.1 (NSR-10)\n(B >= 0.25m)\n"
        #C.9.5.2.1
        if (data.loc[i,"H"]<LimH1)|(data.loc[i,"H"]>LimH2):
            msg_i += "Does not comply with the requirement C.9.5.2.1 (NSR-10)\n(Lx/12 >= H >= Lx/16)\n"
        #C.10.4.1
        if data.loc[i,"Lx"]/data.loc[i,"B"]>50:
            msg_i += "Does not comply with the requirement C.10.4.1 (NSR-10)\n(Lx/B > 50)\n"
        #Altura/Base
        if (data.loc[i,"B"]<LimB1)|(data.loc[i,"B"]>LimB2):
            msg_i += "It does not comply with the relationship between the height and base of beams\n(H/1.4 >= B >= H/1.2)\n"
        #C.3.21.3.6.2.2
        OK, Rr_Real_C, Rr_Real_B_Top, Rr_Real_B_Bot = comprobacion_norma(data.loc[i].to_dict(), "Multiple")
        Rr_Real_C_list.append(Rr_Real_C)
        Rr_Real_B_Top_list.append(Rr_Real_B_Top)
        Rr_Real_B_Bot_list.append(Rr_Real_B_Bot)
        if OK == 0:
            msg_i += "Does not comply with the requirement C.3.21.3.6.2.2 [SCWB]\n(Mnc >= 1.2Mnb)\n"
        if msg_i != "":  # Verificar si msg_i no está vacío
            msg_i = f"* row {i+1}:\n" + msg_i
        error_message += msg_i
    if error_message != "":
        cumplimiento = error_message
    #Sacar data_output
    data_output = data.copy()
    data_output["ρc_Assigned"] = Rr_Real_C_list
    data_output["ρb-top_Assigned"] = Rr_Real_B_Top_list
    data_output["ρb-bot_Assigned"] = Rr_Real_B_Bot_list
    data_output = data_output.rename(columns={"Cuantia_C":'ρc',
                                               "Cuantia_V_Sup":'ρb-top',
                                               "Cuantia_V_Inf":'ρb-bot'})
    return cumplimiento, data_output

#%%Comprobacion
def comprobacion_completo_multiple(data):
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
    data_transformada, cumplimiento = comprobacion_structure(data)
    if cumplimiento=="SI":#Comprobación de la estructura del dataframe
        cumplimiento = comprobacion_formato(data_transformada)
        if cumplimiento=="SI":#Comprobación de formatos
            data_transformada = data_transformada.rename(columns={'Rr_Column':'Cuantia_C',
                                                                  'Rr_Beam_top':'Cuantia_V_Sup',
                                                                  'Rr_Beam_bot':'Cuantia_V_Inf'})
            cumplimiento = comprobacion_rangos(data_transformada, rangos)
            if cumplimiento=="SI":#Comprobación de rangos
                data_transformada["Fc"]=data_transformada["Fc"]*1000
                data_transformada["Cuantia_C"]=data_transformada["Cuantia_C"]/100
                data_transformada["Cuantia_V_Sup"]=data_transformada["Cuantia_V_Sup"]/100
                data_transformada["Cuantia_V_Inf"]=data_transformada["Cuantia_V_Inf"]/100
                cumplimiento_norma, data_output = comprobacion_norma_general(data_transformada)
                return (cumplimiento_norma, cumplimiento, data_output, data_transformada)
            else:
                return (cumplimiento)
        else:
            return (cumplimiento)
    else:
        return (cumplimiento)
