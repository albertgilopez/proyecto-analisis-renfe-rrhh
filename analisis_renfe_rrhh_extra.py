print("******************")
print("BUSINESS ANALYTICS")
print("******************")

print("**********************************************")
print("ESTRUCTURAS DE DATOS PARA NEGOCIO - EJERCICIOS")
print("**********************************************")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline. Es para decirle cómo tiene que sacar los gráficos.
# En este caso significa que los saque como gráficos estáticos integrados en el propio notebook (de tal forma que se guarde y distribuya más fácilmente).

pd.options.display.min_rows = 6

# Importa el dataset 'Renfe_rrhh.csv'  
# Ten en cuenta que el separador de campos es ; y que el decimal es la coma.
# Guardalo en df y sácalo por pantalla.

# Load the CSV file into a DataFrame considering the provided delimiters

df = pd.read_csv('../../00_DATASETS/Renfe_rrhh.csv', delimiter=';', decimal=',')

print(df)
print(df.head())
print(df.info())

# This table provides various information related to employees in a given organization for the years 2013 to 2019. 
# The information includes the number of employees, number of women in the workforce, average tenure of employees, rotation index, investment in training, total hours of training, and many other factors.

# Limpia los nombres de las variables con janitor y haz un info para ver como quedan

# import janitor

# Clean the column names using janitor's clean_names function
# df = df.clean_names()

# Display the info of the DataFrame
# df.info()

# Otra manera de hacerlo manual es:

# Define a function to clean column names
def clean_column_names(df):
    df.columns = df.columns.str.lower()  # make lower case
    df.columns = df.columns.str.replace(' ', '_')  # replace spaces with underscores
    df.columns = df.columns.str.replace('(', '')  # remove left parenthesis
    df.columns = df.columns.str.replace(')', '')  # remove right parenthesis
    df.columns = df.columns.str.replace('-', '')  # remove hyphen
    df.columns = df.columns.str.replace('á', 'a')  # replace accented a with regular a
    df.columns = df.columns.str.replace('é', 'e')  # replace accented e with regular e
    df.columns = df.columns.str.replace('í', 'i')  # replace accented i with regular i
    df.columns = df.columns.str.replace('ó', 'o')  # replace accented o with regular o
    df.columns = df.columns.str.replace('ú', 'u')  # replace accented u with regular u
    df.columns = df.columns.str.replace('%', 'percent')  # replace % with percent
    df.columns = df.columns.str.replace('–', '')  # replace en dash with nothing
    df.columns = df.columns.str.replace('ó', 'o')  # replace accented o with regular o
    df.columns = df.columns.str.replace('í', 'i')  # replace accented i with regular i
    df.columns = df.columns.str.replace('ó', 'o')  # replace accented o with regular o
    df.columns = df.columns.str.replace('ú', 'u')  # replace accented u with regular u
    return df

# Clean the column names
df = clean_column_names(df)

# Display the info of the DataFrame
df.info()

# Pon el año como index y muestra df por pantalla.

# Set 'año' as the index
df.set_index('año', inplace=True)

# Display the DataFrame
print(df)

# Vamos a quedarnos con una versión reducida del dataframe para hacer estos ejerecicios.
# Concretamente con las variables que diferencian entre hombres y mujeres.

# Crea un nuevo dataframe llamado df2 solo con las variables que incluyo en la lista de abajo:
# Muestra df2 por pantalla

# List of columns to keep
a_dejar = ['numero_de_empleados_a_31_de_diciembre',
           'numero_de_mujeres_en_plantilla',
           'antigüedad_media_de_los_empleados_hombres__años',
           'antigüedad_media_de_los_empleados_mujeres__años',
           'indice_de_rotacion_de_la_plantilla_hombres_percent',
           'indice_de_rotacion_de_la_plantilla_mujeres_percent']

# Create a new DataFrame with only the specified columns
df2 = df[a_dejar]

# Display the new DataFrame
print(df2)

# Crea la variable 'numero_de_hombres_en_plantilla' y elimina 'numero_de_empleados_a_31_de_diciembre'.

# Create the 'numero_de_hombres_en_plantilla' column
df2['numero_de_hombres_en_plantilla'] = df2['numero_de_empleados_a_31_de_diciembre'] - df2['numero_de_mujeres_en_plantilla']

# Drop the 'numero_de_empleados_a_31_de_diciembre' column
df2.drop('numero_de_empleados_a_31_de_diciembre', axis=1, inplace=True)

# Display the updated DataFrame
print(df2)

# Ahora vemos que tenemos 6 variables, pero que en verdad son 3 variables, pero repetidas para hombres y mujeres.
# Esto no es tidy. Corrígelo para incluir una nueva variable que diga si el dato es de hombres o mujeres (llamada sexo) y desduplicar así cada una de las métricas.

# Es decir, el nuevo dataset tendría las variables: año (index), sexo, y las 3 métricas.

# PASO 1: resetea el índice para que año pase a ser una columna más
# PASO 2: pasa todo a transaccional excepto el año
# PASO 3: crea una nueva columna llamada sexo que sea 'H' si en 'variable' aparece 'hombres', 'M' si aparece 'mujeres', o 'ERROR' si no aparece ninguno de esos términos.
# PASO 4: crea una nueva columna llamada metrica que sea:

# - 'numero_de_empleados' si en 'variable' aparece 'numero_de'
# - 'antiguedad_media' si en 'variable' aparece 'antiguedad'
# - 'indice_de_rotacion' si en 'variable' aparece 'indice'

# PASO 5: elimina la columna 'variable'

# Step 1: Reset the index
df2.reset_index(inplace=True)

# Step 2: Melt the DataFrame to a long format
df2_melt = df2.melt(id_vars='año', var_name='variable', value_name='value')

# Step 3: Create 'sexo' column
df2_melt['sexo'] = df2_melt['variable'].apply(lambda x: 'H' if 'hombres' in x else ('M' if 'mujeres' in x else 'ERROR'))

# Step 4: Create 'metrica' column
conditions = [
    df2_melt['variable'].str.contains('numero_de'),
    df2_melt['variable'].str.contains('antigüedad'),
    df2_melt['variable'].str.contains('indice')
]
choices = ['numero_de_empleados', 'antiguedad_media', 'indice_de_rotacion']
df2_melt['metrica'] = np.select(conditions, choices, default='ERROR')

# Step 5: Drop the 'variable' column
df2_melt.drop('variable', axis=1, inplace=True)

# Display the DataFrame
print(df2_melt) 

# Pivota finalmente el dataset a tabular de tal forma que año y sexo se queden como el índice (multiíndice), las métricas se queden como variables, y los datos que están en value se queden como las celdillas

# Pivot the DataFrame to a tabular format
df2_tabular = df2_melt.pivot_table(index=['año', 'sexo'], columns='metrica', values='value')

# Display the DataFrame
print(df2_tabular)

# GRÁFICOS

# ANÁLISIS ANTIGÜEDAD. Muestra la antigüedad media de los empleados hombres y mujeres a lo largo de los años. 
# La antigüedad media de ambos, hombres y mujeres, ha ido disminuyendo con el tiempo. 
# Esto podría indicar que la empresa está contratando a más empleados jóvenes o que los empleados más antiguos están dejando la empresa.

# Set the style
plt.style.use('fivethirtyeight')

# Create a DataFrame for 'antiguedad_media'
df_antiguedad = df2_tabular['antiguedad_media'].unstack()

# Create a line plot
df_antiguedad.plot(kind='line', figsize=(10, 6))

# Set the title and labels
plt.title('Análisis de Antigüedad')
plt.ylabel('Antigüedad Media (años)')

# Show the legend
plt.legend(title='Sexo', labels=['Hombres', 'Mujeres'])

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()

# ROTACIÓN EMPLEADOS. Muestra el índice de rotación de los empleados hombres y mujeres a lo largo de los años.
# La rotación de los empleados ha ido aumentando con el tiempo para ambos sexos. 
# Este aumento en el índice de rotación podría indicar una disminución en la satisfacción de los empleados o un cambio en las políticas de contratación de la empresa.

# Create a DataFrame for 'indice_de_rotacion'
df_rotacion = df2_tabular['indice_de_rotacion'].unstack()

# Create a bar plot
df_rotacion.plot(kind='bar', figsize=(16, 9))

# Set the title and labels
plt.title('Rotación de Empleados')
plt.ylabel('Índice de Rotación (%)')

# Show the legend
plt.legend(title='Sexo', labels=['Hombres', 'Mujeres'])

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()

# EVOLUCIÓN NÚMERO EMPLEADOS. Muestra cómo ha cambiado el número de empleados hombres y mujeres en la empresa a lo largo de los años.
# El número de hombres ha disminuido ligeramente con el tiempo, mientras que el número de empleados mujeres ha aumentado.

# Create a DataFrame for 'numero_de_empleados'
df_empleados = df2_tabular['numero_de_empleados'].unstack()

# Create a line plot
df_empleados.plot(kind='line', figsize=(10, 6))

# Set the title and labels
plt.title('Evolución del Número de Empleados')
plt.ylabel('Número de Empleados')

# Show the legend
plt.legend(title='Sexo', labels=['Hombres', 'Mujeres'])

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()

# PROPORCIÓN HOMBRES / MUJERES. Muestra cómo ha cambiado la proporción de empleados hombres y mujeres en la empresa a lo largo de los años. 
# En consecuencia, como se puede ver, a pesar de que el número total de empleados ha disminuido ligeramente, la proporción de empleados mujeres ha aumentado. 

# Create a stacked bar plot
df_empleados.plot(kind='bar', stacked=True, figsize=(10, 6))

# Set the title and labels
plt.title('Proporción de Hombres y Mujeres en la Plantilla')
plt.ylabel('Número de Empleados')

# Show the legend
plt.legend(title='Sexo', labels=['Hombres', 'Mujeres'])

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()
