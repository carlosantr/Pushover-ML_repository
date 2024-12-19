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

from tkinter import filedialog, messagebox, IntVar
from pandas import ExcelWriter, DataFrame
from pandas import read_excel
import joblib
from keras.models import load_model 
from .Requirements_Individual import comprobacion_completo_individual
from .Requirements_Multiple import comprobacion_completo_multiple
from .Draws import resource_path, dibujar_estructura, dibujar_columna, dibujar_viga, resultados_pushover_Individual, mostrar_mensaje_error

#%%Botón de predicción - Individual
def Press_Prediction_Individual(variables, secS_frame, secC_frame, secB_frame, pc_frame, res_frame, models_check):
    resultados = comprobacion_completo_individual(variables)
    if isinstance(resultados, tuple) and len(resultados) > 1:
        cumplimiento, variables_transformadas, nB_C, num_barra_C, nB_V, num_barra_V = resultados
    else:
        cumplimiento=resultados
    if cumplimiento == "SI":
        #Dibujar
        dibujar_estructura(variables_transformadas, secS_frame)
        dibujar_columna(variables_transformadas, secC_frame, nB_C, num_barra_C)
        dibujar_viga(variables_transformadas, secB_frame, nB_V, num_barra_V)
        resultados_pushover_Individual(variables_transformadas, pc_frame, res_frame, models_check)
    else:
        mostrar_mensaje_error("Error in data", cumplimiento)
    

#%%Botón de ayuda
def press_help(key, label):
    rangos ={'Ny':[2,5],
             'Nx':[2,5],
             'Ly':[2.5,4],
             'Lx':[4,8],
             'Fc':[17,35],
             'W':[10,30],
             'B':[0.25,0.5],
             'H':[0.3,0.65],
             'Cuantia_C':[1.12,2.78],
             'Cuantia_V_Sup':[0.51,1.25],
             'Cuantia_V_Inf':[0.34,0.91]}
    meaning ={'Ny':"Number of stories [#]",
              'Nx':"Number of spans [#]",
              'Ly':"Columns height [m]",
              'Lx':"Beams length [m]",
              'Fc':"Compressive strength of concrete [MPa]",
              'W':"Distributed total load on beams, including the beams and columns weight [kN/m]",
              'B':"Base for columns (square) and beams [m]",
              'H':"Beams height [m]",
              'Cuantia_C':"Reinforcement ratio of columns [%]",
              'Cuantia_V_Sup':"Reinforcement ratio for top of beams [%]",
              'Cuantia_V_Inf':"Reinforcement ratio for bottom of beams [%]"}
    if key == "Multiple prediction":
        mensaje = "1. The user must input an excel file (.xlsx) with the data for the prediction.\n2. The excel must contain the information with the next column names:\n'Ny', 'Nx', 'Ly', 'Lx', 'Fc', 'W', 'B', 'Rr_Column' (ρc), 'Rr_Beam_top' (ρb-top), 'Rr_Beam_bot' (ρb-bot)"
        mostrar_mensaje_error(key, mensaje)
    else:
        mensaje = f"{meaning[key]}\n(range: {rangos[key]})"
        mostrar_mensaje_error(label, mensaje)
        
#%%Botones Multiple
def Press_Input_Multiple():
    try:
        file_path = filedialog.askopenfilename(
            title="Select an Excel file (recommended: .xlsx)",
            filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            messagebox.showinfo("No file selected", "You did not select any file.")
            return
        data = read_excel(file_path)
        messagebox.showinfo("File Loaded", "The Excel file has been loaded successfully.")
        global loaded_data
        loaded_data = data  # Guarda el DataFrame en una variable global para usarlo más tarde
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def Press_Check_Multiple():
    try:
        global loaded_data
        if 'loaded_data' not in globals() or loaded_data is None:
            messagebox.showwarning("Input data is not loaded", "Please load the data first.")
            return
        resultados = comprobacion_completo_multiple(loaded_data.copy())
        #Si no hay errores debería arrojar una tupla con longitud mayor a 1
        if isinstance(resultados, tuple) and len(resultados) > 1:
            cumplimiento_norma, cumplimiento, data_output, data_transformada = resultados
            global loaded_data_transformed #Data transformada al global
            global final_input_data
            loaded_data_transformed = data_transformada
            final_input_data = data_output
        else:
            cumplimiento=resultados
        #Mensajes de salida
        if cumplimiento == "SI":
            if cumplimiento_norma != "SI":
                mostrar_mensaje_error("Warning", f"Seismic design requirements are not satisfied. You can proceed to predict anyway, but it is recommended to perform a review of the pre-design to:\n{cumplimiento_norma}")
            else:
                mostrar_mensaje_error("OK", "The input data is ready for the prediction")
        else:
            mostrar_mensaje_error("Error in data", cumplimiento)
    except Exception as e:
        # Manejo de errores si ocurre un problema
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def Press_Prediction_Multiple(modelos):
    Salidas = {'Plas_Vs':'Vs - Yield','Max_Vs':'Vs - Max','Fin_Vs':'Vs - Coll',
               'Plas_D':'δ - Yield','Max_D':'δ - Max','Fin_D':'δ - Coll'}
    Best_model = {'Plas_Vs':'GBM','Max_Vs':'GBM','Fin_Vs':'GBM',
                  'Plas_D':'ANN','Max_D':'ANN','Fin_D':'GBM'}
    orden_cols_out = list(Salidas.values())
    active_models = []
    for i in Salidas.values():
        if "Vs" in i: orden_cols_out.append(i.replace("Vs", "Vs/Wt"))
        elif "δ" in i: orden_cols_out.append(i.replace("δ", "δ/ht"))
    try:
        global loaded_data_transformed
        if 'loaded_data_transformed' not in globals() or loaded_data_transformed is None:
            messagebox.showwarning("Incorrect input data check", "Please check all the requirements first.")
            return
        global final_input_data
        #Calculando altura y peso
        Wt = (loaded_data_transformed["W"]*loaded_data_transformed["Nx"]*loaded_data_transformed["Lx"]*loaded_data_transformed["Ny"])
        ht = loaded_data_transformed["Ny"]*loaded_data_transformed["Ly"]
        #Definiendo data
        X = loaded_data_transformed
        ruta_scalerX = resource_path("Scalers/scalerX.pkl")
        scalerX = joblib.load(ruta_scalerX)
        X_scaled = DataFrame(scalerX.transform(X), columns=X.columns)
        #Predicciones
        list_df_results = {}
        modelos["BEST"]=1
        for modelo, activo in modelos.items():
            key_model=modelo
            resultados_model = DataFrame(columns=Salidas.keys())
            #Comprobacion de actividad
            active = False
            if (modelo == "BEST"):
                active = True
            elif (activo.get() == 1):  # Verificar si el modelo está activo
                active=True
            if active:
                active_models.append(modelo)
                for variable in Salidas.keys():
                    if key_model=="BEST": 
                        modelo=Best_model[variable]
                    #Cargando modelo
                    if modelo=="ANN":
                        ruta_regressor = resource_path(f'Models/ANN_{variable}.h5')
                        regressor = load_model(ruta_regressor, compile=False)
                    else:
                        ruta_regressor = resource_path(f'Models/{modelo}_{variable}.pkl')
                        regressor = joblib.load(ruta_regressor)
                    #Haciendo predicción
                    y_pred_scaled = regressor.predict(X_scaled)
                    #Desnormalizando
                    ruta_scalerY = resource_path(f'Scalers/scalerY_{variable}.pkl')
                    scalerY = joblib.load(ruta_scalerY)
                    y_pred = scalerY.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
                    #Agregando resultado normalizado y sin normalizar
                    if "_Vs" in variable:
                        resultados_model[Salidas[variable]] = y_pred*Wt#Sin normalizar
                        name_var_norm = Salidas[variable].replace("Vs", "Vs/Wt")
                        resultados_model[name_var_norm] = y_pred#Normalizado
                    elif "_D" in variable: 
                        resultados_model[Salidas[variable]] = y_pred*ht/100#Sin normalizar
                        name_var_norm = Salidas[variable].replace("δ", "δ/ht")
                        resultados_model[name_var_norm] = y_pred#Normalizado
                resultados_model = resultados_model[orden_cols_out]
                list_df_results[key_model] = resultados_model
        #Exportar a excel
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # Extensión por defecto
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            title="Save as")
        if archivo: # Si el usuario selecciona una ubicación
            try:
                # Exportar DataFrame a Excel
                with ExcelWriter(archivo, engine='xlsxwriter') as writer:
                    final_input_data.to_excel(writer, sheet_name="Entradas", index=False)
                    # Exportar las hojas al archivo Excel
                    for modelo, activo in modelos.items():
                        if (modelo == "BEST"):
                            list_df_results[modelo].to_excel(writer, sheet_name=modelo, index=False)
                        elif (activo.get() == 1):
                            list_df_results[modelo].to_excel(writer, sheet_name=modelo, index=False)
                messagebox.showinfo("Successful export", f"File saved in: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file:\n{str(e)}")
        del modelos['BEST']
    except Exception as e:
        # Manejo de errores si ocurre un problema
        messagebox.showerror("Error", f"An error occurred: {str(e)}")    
    
    
    
    
    