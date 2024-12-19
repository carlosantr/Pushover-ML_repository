# Pushover-ML
Pushover-ML is a didactic and user-friendly Graphical User Interface (GUI) to efficiently predict a trilinear approximation of pushover curves for low-rise reinforced concrete (RC) frame buildings, using a Machine Learning (ML) based approach.  This tool is expected to be used by practitioners (e.g. students, research centers and engineering offices) to quickly carry out a Pushover analysis without requiring the construction and implementation of detailed nonlinear models. By simplifying the prediction of seismic performance, Pushover-ML bridges the gap between advanced ML techniques and practical engineering applications.
## Trilinear approximation
The GUI provides insights into the expected seismic capacity by predicting three key points of the Pushover curve: 1) Yielding point (Yield), 2) Maximum capacity point (Max), and 3) Collapse point (Coll). Those points are represented in the Pushover curve through the roof drift ratio (δ) and the base shear (Vs) of the frame building. The scheme for the trilinear prediction is presented below:
![image](https://github.com/user-attachments/assets/d4ba4702-f823-4623-b56e-a3934f5619c1)
## Input data
Pushover-ML receives as input data 11 input variables related to the frame distribution, the section geometry and reinforcement ratios of structural elements (i.e. beams and columns), the material properties, and the applied vertical forces for an acceptable range presented in Figure 2 of [1]:
![image](https://github.com/user-attachments/assets/0776722f-6e24-4024-b772-4eb32d5d3c16)
## ML models
The GUI allows the user to make predictions using different ML techniques such as:
* Artificial Neural Networks.
* Gradient Boosting Machines.
* Random Forest.
* Lasso Regression.

And also provides per default an option called "BEST", which fits the predictions with a combination of the abovementioned ML techniques, selecting the best-performing models (i.e., δ and Vs) for each key point of the pushover curve (i.e., Yield, Max, and Coll), leveraging the strengths of each technique. 
## Repository distribution
This repository provides an update of the GUI presented in previous research [2], including a more user-friendly interface, new ML techniques, different prediction modes (i.e., individual and multiple), and defining the yielding with greater robustness. The content of this repository is presented below:
* Database: Includes the processed data (used for training process of ML techniques) and the raw data (recorded after each Pushover analysis generated in OpenseesPy). The raw data is presented in Pickle format (visualization is available using Python). For further information about the meaning of each variable in the raw dataset, please do not hesitate to reach out at carlosantr@unisabana.edu.co
* GUI: Includes the executable files (.exe) of Pushover-ML for the Spanish and English version. Also presents the Backend structure of the GUI, which can be executed on python environment by the "GUI_main.py" file (the user must accomplish with the compilation requirements, operating environments and dependencies presented in [1]).
* Examples: Includes prediction examples for the individual and multiple mode of prediction. The individual folder provides to the user the output excel file format of the examples presented in Figure 5 of [1]. The multiple folder provides to the user an example of the input and output Excel file ("Example_MultipleMode.xlsx" and "Results_MultipleMode.xlsx", respectively) for multiple mode prediction, and another input Excel files in the folder "Errors" to exemplify typical errors indentified by the GUI.
### Note
This work is also part of MSc. thesis in Applied Analytics. For further information about Pushover-ML, licensing, data availability and collaboration in research related to ML applications, do not hesitate to contact at carlosantr@unisabana.edu.co.

## References
[1] Angarita C., Montes C., Arroyo, O., 2025. Pushover-ML: A Machine Learning approach to predict a trilinear approximation of pushover curves for low-rise reinforced concrete frame buildings. SoftwareX (under review)

[2] Angarita C., Montes C., Arroyo O., 2024. Machine learning – based approach for predicting pushover curves of low-rise reinforced concrete frame buildings. Structures 70, 107694. https://doi.org/10.1016/j.istruc.2024.107694 
