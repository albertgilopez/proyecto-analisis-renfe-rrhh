# PROYECTO: Proyecto Business Analytics RENFE RRHH
# AUTOR: Albert Gil López
# LINKEDIN: https://www.linkedin.com/in/albertgilopez/

"""
DESCRIPCIÓN: En este proyecto, se realiza un análisis detallado de los datos de la inversión en la comunidad por parte de Renfe de los años 2014 a 2019.
Se utilizan técnicas de análisis de datos y visualización para explorar y entender los datos. Se realiza una limpieza y transformación de los datos, así como la creación de nuevas variables para obtener más información de los datos.
Uno de los hallazgos clave del análisis fue la realización de un análisis de Pareto para examinar la distribución de la inversión en la comunidad.
Se puede observar en el gráfico que un pequeño porcentaje de los años representa una gran proporción de la inversión total en la comunidad. 
En concreto, los años 2014 y 2015 representaron más del 50% de la inversión total en la comunidad.

"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.min_rows = 6

# Importamos el dataset 'Renfe_rrhh.csv'  
# El separador de campos es ; y que el decimal es la ,.
# Lo gardamos en df y lo mostramos por pantalla.

df = pd.read_csv('../00_DATASETS/Renfe_rrhh.csv', delimiter=';', decimal=',')

print(df)
print(df.head())
print(df.info())

# This table provides various information related to employees in a given organization for the years 2013 to 2019. 
# The information includes the number of employees, number of women in the workforce, average tenure of employees, rotation index, investment in training, total hours of training, and many other factors.

# Define a function to clean column names
# También podemos hacerlo con janitor

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

df = clean_column_names(df)
df.info()

# Ponemos el año como index y mostramos df por pantalla.
df.set_index('año', inplace=True)
print(df)

# Las columnas (contratacion_a_centros_especiales_de_empleo_miles_de_euros y contribucion_social_miles_de_euros) se han identificado como object
# Esto indica que pueden contener valores no numéricos. Es posible que necesitemos limpiar estas columnas para poder utilizarlas en análisis numéricos. 
# Revisamos cuáles son los valores únicos en estas columnas para entender qué tipo de limpieza puede ser necesaria.

# Check unique values in the two columns
unique_contratacion = df['contratacion_a_centros_especiales_de_empleo_miles_de_euros'].unique()
unique_contribucion = df['contribucion_social_miles_de_euros'].unique()

# Los valores únicos en la columna contratacion_a_centros_especiales_de_empleo_miles_de_euros son '11754', '3738' y '-'.
# Para la columna contribucion_social_miles_de_euros, los valores únicos son '70554', '69689' y '-'.

# Replace '-' with NaN and convert the columns to numeric
df['contratacion_a_centros_especiales_de_empleo_miles_de_euros'] = pd.to_numeric(df['contratacion_a_centros_especiales_de_empleo_miles_de_euros'].replace('-', float('NaN')))
df['contribucion_social_miles_de_euros'] = pd.to_numeric(df['contribucion_social_miles_de_euros'].replace('-', float('NaN')))

# Display the DataFrame info again to check the changes
df.info()

# Creamos una nueva variable que contenga la diferencia entre la antigüedad media de hombres y mujeres (en valor absoluto). Le llamámos antiguedad_media_dif.

# Create a new column that is the absolute difference between the average tenure of men and women
df['antiguedad_media_dif'] = abs(df['antigüedad_media_de_los_empleados_hombres__años'] - df['antigüedad_media_de_los_empleados_mujeres__años'])
print(df['antiguedad_media_dif'])

# Estos valores indican que, en cada año, los empleados hombres han estado en la empresa en promedio alrededor de 6 a 7 años más que las empleadas mujeres.

# Creamos una nueva variable que contenga el número de hombres que se ha ido de la empresa en cada año. Le llamámos rotación_hombres

# - numero_de_empleados_a_31_de_diciembre
# - numero_de_mujeres_en_plantilla
# - indice_de_rotacion_de_la_plantilla_hombres_%

# Create a new column that represents the number of men who have left the company each year
# This is calculated as the product of the total number of employees, the percentage of those who are men, 
# and the turnover rate for men

df['rotacion_hombres'] = (df['numero_de_empleados_a_31_de_diciembre'] - df['numero_de_mujeres_en_plantilla']) * (df['indice_de_rotacion_de_la_plantilla_hombres_percent'] / 100)
print(df['rotacion_hombres'])

# Eliminamos el registro del año 2013.
df = df.drop(2013)
print(df)

# Vamos a agrupar los datos en dos trienios, de 2014 a 2016 ambos incluídos. Y de 2017 a 2019 ambos incluídos.
# Creamos una nueva variable que se llame trienio, y que contenga T1 en el primer caso y T2 en el segundo.

df['trienio'] = pd.cut(df.index, bins=[2013, 2016, 2019], labels=['T1', 'T2'], include_lowest=True)
print(df)

# Discretizamos la inversion_en_formacion_miles_de_euros, creando una nueva variable que se llame inversion_en_formacion_miles_de_euros_disc y que tenga los valores:

# 01_Menos_de_4001
# 02_Entre_4001_y_6000
# 03_Mas de 6001

df['inversion_en_formacion_miles_de_euros_disc'] = pd.cut(
    df['inversion_en_formacion_miles_de_euros'], 
    bins=[0, 4001, 6001, float('inf')], 
    labels=['01_Menos_de_4001', '02_Entre_4001_y_6000', '03_Mas de 6001'],
    include_lowest=True
)

print(df)

# Calculamos una nueva variable llamada 'horas_totales_de_formacion_dif_media_trienio' que sea la diferencia en absoluto entre el número de horas de formación de cada año menos la media del trienio al que pertenece ese año.

mean_formacion_per_trienio = df.groupby('trienio')['horas_totales_de_formacion'].mean()

# Subtract the mean 'horas_totales_de_formacion' for the corresponding 'trienio' from the 'horas_totales_de_formacion' of each year
df['horas_totales_de_formacion_dif_media_trienio'] = df.apply(lambda row: abs(row['horas_totales_de_formacion'] - mean_formacion_per_trienio[row['trienio']]), axis=1)
print(df)

# Calculamos una nueva variable llamada 'horas_totales_de_formacion_acum_trienio' que sea el acumulado de las horas de formación en cada trienio.

# Sort the DataFrame by the index in ascending order
df = df.sort_index(ascending=True)

# Calculate the cumulative sum of 'horas_totales_de_formacion' within each 'trienio'
df['horas_totales_de_formacion_acum_trienio'] = df.groupby('trienio')['horas_totales_de_formacion'].cumsum()
print(df)

# Pasamos trienio a variables dummy, generando 2 nuevas variables de tipo indicador.

trienio_dummies = pd.get_dummies(df['trienio'], prefix='trienio')

# Concatenate the dummy variables with the original DataFrame
df = pd.concat([df, trienio_dummies], axis=1)
print(df)

# ¿La inversion_en_la_comunidad_miles_de_euros ha sido equitativa todos los años? 

# Step 1: Create a new DataFrame 'pareto' with only the index 'año' and the variable 'inversion_en_la_comunidad_miles_de_euros'
pareto = df[['inversion_en_la_comunidad_miles_de_euros']].copy()

# Display the new DataFrame
print(pareto)

# Step 2: Sort the data in descending order
pareto = pareto.sort_values(by='inversion_en_la_comunidad_miles_de_euros', ascending=False)

# Display the sorted DataFrame
print(pareto)

# Step 3: Crea la variable posicion con la posición (en absoluto)
pareto['position'] = range(1, len(pareto) + 1)

# Display the updated DataFrame
print(pareto)

# Step 4: Crea la variable posicion_porc con la posición (en porcentaje)
pareto['position_porc'] = pareto['position'] / len(pareto) * 100

# Display the updated DataFrame
print(pareto)

# Como se puede ver, los dos primeros años (2014 y 2015) representan más del 50% de la inversión total en la comunidad.

# Step 5: Create an 'acum' variable that indicates the cumulative 'inversion_en_la_comunidad_miles_de_euros'
pareto['acum'] = pareto['inversion_en_la_comunidad_miles_de_euros'].cumsum()

# Display the updated DataFrame
print(pareto)

# Step 6: Create an 'acum_porc' variable that indicates the cumulative percentage of 'inversion_en_la_comunidad_miles_de_euros'

# Calculate the total 'inversion_en_la_comunidad_miles_de_euros'
total_inversion = pareto['inversion_en_la_comunidad_miles_de_euros'].sum()

pareto['acum_porc'] = pareto['acum'] / total_inversion * 100

# Display the updated DataFrame
print(pareto)

# Modify 'pareto' to only include the index and the variables 'position_porc' and 'acum_porc'

pareto.reset_index(inplace=True)
pareto = pareto[['año', 'position_porc', 'acum_porc']].set_index('año')

# Display the updated DataFrame
print(pareto)

# #Haz el gráfico de pareto (recuerda resetear el índice antes de nada)

# Reset the index so that 'año' becomes a column
pareto.reset_index(inplace=True)

# Create a Pareto chart with 'position_porc' and 'acum_porc'
fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(x='position_porc', y='acum_porc', data=pareto, color='red', sort=False, marker="o")

# Set the labels and title
ax.set_xlabel('Posición (%)')
ax.set_ylabel('Acumulado (%)')
ax.set_ylim(0, 100)  # Set the y-axis scale to be from 0 to 100
plt.title('Análisis de Pareto de la Inversión en la Comunidad')

# Y con la función proporcionada en el curso:

# Import the necessary library
import numpy as np

def pareto_ds4b(variable, salida='tabla'):
    # Sort in descending order and convert to dataframe
    pareto = variable.sort_values(ascending=False).to_frame()

    # Rename the variable
    pareto.columns = ['Valor']

    # Create the position
    pareto['Posicion'] = np.arange(start=1, stop=len(pareto) + 1)
    pareto['Posicion_Porc'] = pareto.Posicion.transform(lambda x: x / pareto.shape[0] * 100)

    # Create the cumulative
    pareto['Acum'] = pareto['Valor'].cumsum()
    max_pareto_acum = max(pareto.Acum)
    pareto['Acum_Porc'] = pareto.Acum.transform(lambda x: x / max_pareto_acum * 100)

    # Simplify
    pareto = pareto[['Posicion_Porc', 'Acum_Porc']]

    # Set the style to 'fivethirtyeight'
    plt.style.use('fivethirtyeight')

    # Create the plot
    f, ax = plt.subplots(figsize=(16, 8))
    ax.plot(pareto.Posicion_Porc, pareto.Acum_Porc)
    ax.plot(pareto.Posicion_Porc, pareto.Posicion_Porc)
    ax.tick_params(axis='x', labelsize=12, labelrotation=90)

    # Add labels and title
    ax.set_xlabel('Posición (%)')
    ax.set_ylabel('Acumulado (%)')
    ax.set_title('Análisis de Pareto de la Inversión en la Comunidad')

    plt.show()

# Use the function to perform a Pareto analysis on 'inversion_en_la_comunidad_miles_de_euros' and display the graph
inversion = df['inversion_en_la_comunidad_miles_de_euros']
pareto_ds4b(inversion, salida = 'grafico')

plt.style.use('fivethirtyeight')

# Como puedes ver en el gráfico, los dos primeros años (2014 y 2015) representan más del 50% de la inversión total en la comunidad.
# Esto está en línea con el principio de Pareto (también conocido como la regla del 80/20), que establece que, para muchos eventos, aproximadamente el 80% de los efectos provienen del 20% de las causas.
# En este caso, una gran proporción de la inversión total en la comunidad se realiza en un pequeño número de años.

# Algunos gráficos más:

# We need to calculate the 'rotacion_mujeres' first
df['rotacion_mujeres'] = df['numero_de_mujeres_en_plantilla'] * (df['indice_de_rotacion_de_la_plantilla_mujeres_percent'] / 100)
# Create a new column for the number of men in the company
df['numero_de_hombres_en_plantilla'] = df['numero_de_empleados_a_31_de_diciembre'] - df['numero_de_mujeres_en_plantilla']

# Set the style to 'fivethirtyeight'
plt.style.use('fivethirtyeight')

# Create the first set of plots (Antigüedad analysis and Number of employees)
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 8))

# Antigüedad analysis plot
antiguedad_plot = df[['antigüedad_media_de_los_empleados_hombres__años', 'antigüedad_media_de_los_empleados_mujeres__años']].plot(kind='bar', ax=ax1)
ax1.set_title('Análisis de Antigüedad')
ax1.set_xlabel('Año')
ax1.set_ylabel('Antigüedad media')
ax1.tick_params(axis='x', labelrotation=45)  # Rotate x-axis labels for better readability

# Modify the legend labels
antiguedad_plot.legend(["Hombres", "Mujeres"])

# Number of employees plot
plantilla_plot = df[['numero_de_hombres_en_plantilla', 'numero_de_mujeres_en_plantilla']].plot(kind='bar', ax=ax2)
ax2.set_title('Número de empleados en la empresa')
ax2.set_xlabel('Año')
ax2.set_ylabel('Número de empleados')
ax2.tick_params(axis='x', labelrotation=45)  # Rotate x-axis labels for better readability

# Modify the legend labels
plantilla_plot.legend(["Hombres", "Mujeres"])

# Adjust spacing between subplots in the first figure
plt.subplots_adjust(wspace=0.3, hspace=0.6)

# Create the second set of plots (Employee turnover and Investment in training)
fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(16, 8))

# Employee turnover plot
rotacion_plot = df[['rotacion_hombres', 'rotacion_mujeres']].plot(kind='bar', ax=ax3)
ax3.set_title('Rotación de empleados e Inversión en formación (Horas)')
ax3.set_xlabel('Año')
ax3.set_ylabel('Número de empleados que se van')
ax3.tick_params(axis='x', labelrotation=45)  # Rotate x-axis labels for better readability

# Modify the legend labels
rotacion_plot.legend(["Hombres", "Mujeres"])

# Add line plot for investment in training over the years
df['horas_totales_de_formacion_acum_trienio'].plot(kind='line', ax=ax4, secondary_y=True, color='orange')
ax4.right_ax.set_ylabel('Inversión en formación (Horas acumuladas)')
ax4.right_ax.tick_params(axis='y', labelcolor='orange')

# Adjust spacing between subplots in the second figure
plt.subplots_adjust(wspace=0.3, hspace=0.6)

plt.tight_layout()
plt.show()
