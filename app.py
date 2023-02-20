import requests
import streamlit as st
from datetime import date
import time

# Define the API endpoint and request payload
API_ENDPOINT_USUARIO = 'http://python-docx.valladolid.tecnm.mx:8443/usuario'
API_ENDPOINT_JUSTIFICACION = 'http://python-docx.valladolid.tecnm.mx:8443/justificacion'

# Definicion funciones
def pagina_carga_en_seg(seg):
    user_registrado = st.success("Usuario Registrado")
    with st.spinner():
        time.sleep(seg)  # Simulamos una tarea que tarda 5 segundos
        user_registrado.empty()
        st.success('Carga completa')

def si_hay_reposicion():

    print("funciona")

# Define the form fields
form_fields = {
    'fecha': {'label': 'Fecha:', 'value': ''},
    'nombre': {'label': 'Nombre:', 'value': ''},
    'puesto': {'label': 'Puesto:', 'value': ''},
    ###   Informa que se ausento de sus labores:
    'horario_inasistencia_inicio': {'label': 'horario_inasistencia_inicio', 'value': ''},
    'horario_inasistencia_final': {'label': 'horario_inasistencia_final', 'value': ''},
    'fecha_inasistencia': {'label': 'fecha_inasistencia', 'value': ''},
    'reposicion': {'label': 'Reposicion:', 'value': ''},
    'horario_reposicion_inicio': {'label': 'horario_reposicion_inicio', 'value': ''},
    'horario_reposicion_final': {'label': 'horario_reposicion_final', 'value': ''},
    'fecha_reposicion': {'label': 'fecha_reposicion', 'value': ''},
    'motivo': {'label': 'Motivo:', 'value': ''},
    'nombre_jefe': {'label': 'Nombre Jefe:', 'value': ''},
    'puesto_jefe': {'label': 'Puesto Jefe:', 'value': ''},
    'tipo': {'label': 'Tipo de Justificacion', 'value':''}
}

# Página 1: ingreso del texto
titulo_pagina_1 = st.title("Sistema de Formatos Justificacion")
encabezado_pagina_1 = st.header("Ingresa tu nombre de usuario ")
text_input_username = st.empty()
username = text_input_username.text_input("Usuario:")

if username != "":
    # Make a POST request to the API
    payload = {'username': username}
    response = requests.post(API_ENDPOINT_USUARIO, data=payload)

    # If the request is successful, parse the JSON response and fill the form fields
    if response.status_code == 200:
        data = response.json().get('user')
        if data and username != "":
            
            # Ocultamos la pagina principal
            titulo_pagina_1.empty()
            encabezado_pagina_1.empty()
            text_input_username.empty()

            #pagina_carga_en_seg(3)
            form_fields['nombre']['value'] = data.get('fname') + " " + data.get('lname')
            form_fields['puesto']['value'] = data.get('position')
            
            st.write('# Formato Justificacion')
            # Render the form

            for field_name, field_data in form_fields.items():
                match field_name:
                    case "fecha":
                        field_data['value'] = st.date_input(field_data['label'], value=date.today(), key='fecha_formato')
                    
                    # Columnas Fecha inasistencia
                    case "horario_inasistencia_inicio":
                        st.write("Informa que se ausento de sus labores en el horario:")
                        col1, col2, col3, col4, col5, col6 = st.columns([1,5,1,5,3,3])
                        with col1:
                            st.write("De")
                        with col2:
                            field_data['value'] = st.slider(field_data['label'], 0, 23, 9, 1, key='time_range_1',label_visibility="collapsed")
                        with col3:
                            st.write("a")
                    case "horario_inasistencia_final":
                        with col4:
                            field_data['value'] = st.slider(field_data['label'], 0, 23, 17, 1, key='time_range_2', label_visibility="collapsed")
                    case "fecha_inasistencia":
                        with col5:
                            st.write("DE FECHA:")
                        with col6:
                            field_data['value'] = st.date_input(field_data['label'],key='fecha_inasistencia', label_visibility="collapsed")
                    
                    # Columnas fecha Reposicion
                    case "reposicion":
                        col1, col2, col3, col4, col5, col6, col7 =st.columns([4,1,3,1,3,3,3])
                        with col1:
                            field_data['value'] = st.checkbox(field_data['label'])
                            reposicion = field_data['value']
                    case "horario_reposicion_inicio":
                        with col2:
                            if reposicion:
                                st.write("De")
                        with col3:
                            if reposicion:
                                field_data['value'] = st.slider(field_data['label'], 0, 23, 9, 1, key='time_range_3', label_visibility="collapsed")
                    case "horario_reposicion_final":
                        with col4:
                            if reposicion:
                                st.write("a")
                        with col5:
                            if reposicion:
                                field_data['value'] = st.slider(field_data['label'], 0, 23, 17, 1, key='time_range_4', label_visibility="collapsed")
                    case "fecha_reposicion":    
                        with col6:
                            if reposicion:
                                st.write("DE FECHA:")
                        with col7:
                            if reposicion:
                                field_data['value'] = st.date_input(field_data['label'],key='fecha_reposicion', label_visibility="collapsed")
                    
                    case "tipo":
                        field_data['value'] = st.radio(field_data['label'],('Personal', 'Medica'))

                    case _:
                        field_data['value']  = st.text_input(field_data['label'], value=field_data['value'])

            # Agrega un botón para enviar los datos al servidor
            if st.button('Enviar'):
                # Obtiene los valores de los inputs
                form_values = {field_name: field_data['value'] for field_name, field_data in form_fields.items()}

                # Envía los datos al servidor
                response = requests.post(API_ENDPOINT_JUSTIFICACION, data=form_values)

                # Verifica si la solicitud fue exitosa
                if response.status_code == 200:
                    st.success('Los datos han sido enviados.')
                else:
                    st.error('Ha ocurrido un error al enviar los datos.')
        else:
            st.warning("El usuario no existe.")
    else:
        st.error("El servicio no esta disponible.")