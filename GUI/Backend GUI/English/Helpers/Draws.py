# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 01:37:30 2024

@author: USUARIO
"""
from tkinter import Canvas, Label, Button, Toplevel, filedialog, messagebox, IntVar
from tkinter.ttk import Style, Treeview
from pandas import ExcelWriter, DataFrame
from matplotlib.pyplot import subplots, yticks, legend, grid
from keras.models import load_model 
import joblib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys, os

#%%Ayuda a encontrar archivos en .exe empaquetado
def resource_path(relative_path):
    """Obtiene la ruta de un archivo empaquetado."""
    try:
        # Ruta en el ejecutable empaquetado
        base_path = sys._MEIPASS
    except AttributeError:
        # Ruta en el entorno de desarrollo
        #base_path = os.path.abspath(__file__)
        base_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
    return os.path.join(base_path, relative_path)

#%%Pintar estructura
def dibujar_estructura(variables, secS_frame):
    Nx=variables["Nx"]
    Ny=variables["Ny"]
    Str=Canvas(secS_frame,width="180",height="180",bg="#EEEEEE",highlightthickness=0)
    Str.place(x=23,y=40)
    spacex=170/Nx
    spacey=170/Ny
    Str.create_line(5,5,5,175);Str.create_line(0,175,10,175)
    Str.create_line(5,5,175,5) 
    for i in range(1,Nx+1):
        Str.create_line(i*spacex+5,5,i*spacex+5,175)
        Str.create_line(i*spacex,175,i*spacex+10,175) 
    for i in range(1,Ny):
        Str.create_line(5,i*spacey+5,175,i*spacey+5) 


#%%Pintar columnas
def dibujar_columna(variables, secC_frame, nB_C, num_barra):
    Bcol = variables["B"]
    Hcol = variables["B"]
    #Creando seccion
    Col=Canvas(secC_frame,width="180",height="165",bg="#EEEEEE",highlightthickness=0)
    Col.place(x=22,y=15)
    xC=1000*Bcol/5
    yC=1000*Hcol/5
    x1C=(180-xC)/2;y1C=(180-yC)/2
    x2C=x1C+xC;y2C=y1C+yC
    Col.create_rectangle(x1C,y1C,x2C,y2C,width=3.5)
    Col.create_text(x2C+8.5,y1C+(yC/2), text = f'H = {Hcol}m', angle = 270,font=("Arial",8))
    Col.create_text(x1C+(xC/2),y1C-8.5, text = f'B = {Bcol}m', font=("Arial",8))
    #Refuerzo
    recub=5
    dim=7
    sepy=(abs(y2C-y1C)-recub*2-dim)/(len(nB_C)-1)
    for i in range(nB_C[0]):#Top
        sep=(abs(x2C-x1C)-recub*2-dim)/(nB_C[0]-1)
        Col.create_oval(x1C+recub+(sep*i),y1C+recub,x1C+recub+dim+(sep*i),y1C+recub+dim,fill='black')
    for i in range(nB_C[-1]):#Bottom
        sep=(abs(x2C-x1C)-recub*2-dim)/(nB_C[-1]-1)
        Col.create_oval(x1C+recub+(sep*i),y2C-recub-dim,x1C+recub+dim+(sep*i),y2C-recub,fill='black')
    if (len(nB_C)>=3):
        for i in range(nB_C[1]):#Fila 3
            sep=(abs(x2C-x1C)-recub*2-dim)/(nB_C[1]-1)
            Col.create_oval(x1C+recub+(sep*i),y1C+recub+sepy,x1C+recub+dim+(sep*i),y1C+recub+sepy+dim,fill='black')
        if (len(nB_C)==4):
            for i in range(nB_C[2]):#Fila 3
                sep=(abs(x2C-x1C)-recub*2-dim)/(nB_C[2]-1)
                Col.create_oval(x1C+recub+(sep*i),y1C+recub+2*sepy,x1C+recub+dim+(sep*i),y1C+recub+2*sepy+dim,fill='black')  
    #Agregar textos de número de barras
    Col.create_text(x1C-15,y1C+recub, text = f'{int(nB_C[0])}#{int(num_barra)}', font=("Arial",8))#Arriba
    Col.create_text(x1C-15,y2C-recub, text = f'{int(nB_C[-1])}#{int(num_barra)}', font=("Arial",8))#Abajo
    
    if len(nB_C)>=3:
        if len(nB_C)==4:
            Col.create_text(x1C-15,y1C+recub+4.5+(y2C-y1C)/4, text = f'{int(nB_C[1])}#{int(num_barra)}', font=("Arial",8))#Fila 2
            Col.create_text(x1C-15,y1C+recub+4.5+2*(y2C-y1C)/4, text = f'{int(nB_C[2])}#{int(num_barra)}', font=("Arial",8))#Fila 3
        else:
            Col.create_text(x1C-15,y1C+(y2C-y1C)/2, text = f'{int(nB_C[1])}#{int(num_barra)}', font=("Arial",8))#Fila del medio
    
    #Asegurar que el titulo quede encima
    Label(secC_frame,text="Columns",fg="#0C0268",font=("Arial Black",15)).place(x=63,y=0)#Title of the frame (text)

#%%Pintar vigas
def dibujar_viga(variables, secB_frame, nB_V, num_barra):
    Bbeam=variables["B"]
    Hbeam=variables["H"]
    recub=5
    dim=7
    Bea=Canvas(secB_frame,width="180",height="175",bg="#EEEEEE",highlightthickness=0)
    Bea.place(x=22,y=15)
    xB=1000*Bbeam/5
    yB=1000*Hbeam/5
    x1B=(180-xB)/2;y1B=(180-yB)/2
    x2B=x1B+xB;y2B=y1B+yB
    Bea.create_rectangle(x1B,y1B,x2B,y2B,width=3.5)
    Bea.create_text(x2B+8.5,y1B+(yB/2), text = f"H = {Hbeam}m", angle = 270,font=("Arial",8))
    Bea.create_text(x1B+(xB/2),y2B+8.5, text = f"B = {Bbeam}m", font=("Arial",8))
    #Reinforcement
    for i in range(nB_V[0]):#Top
        sep=(abs(x2B-x1B)-recub*2-dim)/(nB_V[0]-1)
        Bea.create_oval(x1B+recub+(sep*i),y1B+recub,x1B+recub+dim+(sep*i),y1B+recub+dim,fill='black')
    for i in range(nB_V[-1]):#Bottom
        sep=(abs(x2B-x1B)-recub*2-dim)/(nB_V[-1]-1)
        Bea.create_oval(x1B+recub+(sep*i),y2B-recub-dim,x1B+recub+dim+(sep*i),y2B-recub,fill='black')
    #Agregar textos de número de barras
    Bea.create_text(x1B-15,y1B+recub, text = f'{int(nB_V[0])}#{int(num_barra[0])}', font=("Arial",8))#Arriba
    Bea.create_text(x1B-15,y2B-recub, text = f'{int(nB_V[-1])}#{int(num_barra[1])}', font=("Arial",8))#Abajo
    #Asegurar que el titulo quede encima
    Label(secB_frame,text="Beams",fg="#0C0268",font=("Arial Black",15)).place(x=72.75,y=0)#Title of the frame (text)

#%%Dibujar Pushover
def resultados_pushover_Individual(variables, pc_frame, res_frame, modelos):
    #Calculando valores para desnormalizar
    Wt = (variables["W"]*variables["Nx"]*variables["Lx"]*variables["Ny"])
    ht = variables["Ny"]*variables["Ly"]
    #Variables a predecir
    Salidas = {'Plas_Vs':'Vs - Yield','Max_Vs':'Vs - Max','Fin_Vs':'Vs - Coll',
               'Plas_D':'δ - Yield','Max_D':'δ - Max','Fin_D':'δ - Coll'}
    Best_model = {'Plas_Vs':'GBM','Max_Vs':'GBM','Fin_Vs':'GBM',
                  'Plas_D':'ANN','Max_D':'ANN','Fin_D':'GBM'}
    #Generando X y normalizando
    X = DataFrame([variables])
    ruta_scalerX = resource_path("Scalers/scalerX.pkl")
    scalerX = joblib.load(ruta_scalerX)
    X_scaled = DataFrame(scalerX.transform(X), columns=X.columns)
    #Definiendo figura
    fig,ax=subplots(dpi=65,figsize=(4.85,4.85),facecolor="#EEEEEE")
    yticks(rotation=90)
    grid()
    ax.set_xlabel("δ/ht [%]")
    ax.set_ylabel("Vs/Wt [--]")
    ax.set_facecolor("#EEEEEE")
    #Haciendo predicciones de los modelos seleccionados
    resultados_Vs = {}
    resultados_D = {}
    for modelo, activo in modelos.items():
        if activo.get() == 1:  # Verificar si el modelo está activo
            resultados_Vs[modelo]=[0]
            resultados_D[modelo]=[0]
            for variable in Salidas.keys():
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
                #Agregando resultado
                if "_Vs" in variable:
                    resultados_Vs[modelo].append(y_pred[0])
                elif "_D" in variable:
                    resultados_D[modelo].append(y_pred[0])
            #Ploteando resultado del modelo
            ax.plot(resultados_D[modelo], resultados_Vs[modelo], label=modelo)
            ax.scatter(resultados_D[modelo], resultados_Vs[modelo], color="black")
    #Ploteando el mejor modelo
    resultados_Vs["BEST"]=[0]
    resultados_D["BEST"]=[0]
    for variable, modelo in Best_model.items():
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
        #Agregando resultado
        if "_Vs" in variable:
            resultados_Vs["BEST"].append(y_pred[0])
        elif "_D" in variable:
            resultados_D["BEST"].append(y_pred[0])
    #Ploteando resultado del modelo
    ax.plot(resultados_D["BEST"], resultados_Vs["BEST"], label="BEST")
    ax.scatter(resultados_D["BEST"], resultados_Vs["BEST"], color="black")
    legend(loc='lower right')
    #Insertando al frame
    Model=FigureCanvasTkAgg(fig,master=pc_frame)
    Model.get_tk_widget().place(x=15,y=20)
    Model.draw()
    Label(pc_frame,text="Prediction",fg="#0C0268",font=("Arial Black",15)).place(x=112,y=0)#Title of the frame (text)

    #Apartado de resultados
    dic_resultados = {}
    dic_resultados["BEST"] = [item for sublist in [resultados_Vs["BEST"][1:], resultados_D["BEST"][1:]] for item in sublist]
    for modelo, activo in modelos.items():
        if activo.get() == 1:  # Verificar si el modelo está activo
            dic_resultados[modelo] = [item for sublist in [resultados_Vs[modelo][1:], resultados_D[modelo][1:]] for item in sublist]
    df_resultados = DataFrame(dic_resultados, index=Salidas.values())
    df_resultados_desnorm=df_resultados.copy()
    for variable in df_resultados_desnorm.index:
        if "Vs" in variable:
            df_resultados_desnorm.loc[variable]=df_resultados_desnorm.loc[variable]*Wt
        else:
            df_resultados_desnorm.loc[variable]=df_resultados_desnorm.loc[variable]*ht/100
    #MOSTRAR TABLA
    style = Style()
    style.configure("Treeview",background="#EEEEEE", rowheight=25, borderwidth=1)
    style.configure("Treeview.Heading",font=("Arial", 10, "bold"),background="#DDDDDD",foreground="black",relief="flat")
    style.map("Treeview",background=[("selected", "#cccccc")],foreground=[("selected", "black")],fieldbackground=[("!selected", "#EEEEEE")])
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    tree_width = 328.5
    num_columns = len(df_resultados.columns) + 1
    column_width = int(tree_width // num_columns)
    tree = Treeview(res_frame,columns=["Indice"] + list(df_resultados.columns),show="headings",height=10,style="Treeview")
    tree.heading("Indice", text="Punto")
    tree.column("Indice", anchor="center", width=column_width)
    for col in df_resultados.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=column_width)
    def disable_resize(event):
        return "break"
    tree.bind("<Button-1>", disable_resize)  # Desactiva el redimensionamiento de las columnas
    for item in tree.get_children():
        tree.delete(item)
    for index, row in df_resultados.iterrows():
        rounded_row = [round(value, 3) for value in row]
        tree.insert("", "end", values=[index] + rounded_row)
    tree.place(x=7, y=37, width=tree_width, height=190)
    #Cambiando nombres para normalizados y uniendo en uno solo
    df_resultados_export = df_resultados_desnorm.copy()
    for variable in df_resultados.index:
        if "Vs" in variable:
            name = variable.replace("Vs", "Vs/Wt")
            df_resultados_export.loc[name] = df_resultados.loc[variable]
        elif "δ" in variable: 
            name = variable.replace("δ", "δ/ht")
            df_resultados_export.loc[name] = df_resultados.loc[variable]
    #Botón de exportar excel
    def exportar_a_excel():
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # Extensión por defecto
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            title="Save as")
        if archivo:  # Si el usuario selecciona una ubicación
            try:
                # Exportar DataFrame a Excel
                with ExcelWriter(archivo, engine='xlsxwriter') as writer:
                    # Exportar las hojas al archivo Excel
                    df_resultados_export.to_excel(writer, sheet_name="Summary of predictions", index=True)  # Hoja 1
                    messagebox.showinfo("Successful export", f"File saved in: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file:\n{str(e)}")
    boton_exportar = Button(res_frame,text="Export to Excel",command=exportar_a_excel,
        bg="#C0C0C0",fg="#0C0268",font=("Arial Black", 9))
    boton_exportar.place(x=108.5, y=225)  # Ubicación específica del botón

#%%Mensaje de error
def mostrar_mensaje_error(titulo, mensaje):
    ventana = Toplevel()  # Crear ventana secundaria
    ventana.title(titulo)
    ventana.geometry("300x150")
    # Mensaje
    Label(ventana, text=mensaje, font=("Arial", 10), wraplength=280).pack(pady=20)
    # Botón para cerrar
    Button(ventana, text="OK", command=ventana.destroy, font=("Arial", 10)).pack(pady=10)