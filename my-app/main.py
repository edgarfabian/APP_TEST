import flet as ft
import paho.mqtt.client as mqtt
import json
import threading
numero1=0

# Llamada a la función
mensaje = {"LED": 1}
# Callback que se ejecuta cuando se recibe un mensaje
def on_message(cliente, userdata, mensaje):
    global numero1
    try:
        # Convertir el mensaje recibido a un diccionario usando json.loads
        data = json.loads(mensaje.payload.decode())

        # Extraer el valor de la clave "NUMER1" si existe
        if "NUMER1" in data:
            valor = data["NUMER1"]
            print(f"Valor de NUMER1: {valor}")
            valor_texto.value = f"Valor de NUMER1: {valor}"
            valor_texto.update()
        else:
            print("La clave 'NUMER1' no se encuentra en el mensaje recibido.")
    except json.JSONDecodeError:
        print("Error al decodificar el mensaje JSON.")

def enviar_mensaje_mqtt(broker, puerto, usuario, contraseña, topico, mensaje):
    # Creación del cliente MQTT
    cliente = mqtt.Client()

    # Configuración de usuario y contraseña para el broker
    cliente.username_pw_set(usuario, contraseña)

    # Conexión al broker
    cliente.connect(broker, puerto)
    # Convertir el mensaje a formato JSON
    mensaje_json = json.dumps(mensaje)

    # Publicar un mensaje
    cliente.publish(topico, mensaje_json)

    # Cerrar la conexión
    cliente.disconnect()

# Callback que se ejecuta cuando se recibe un mensaje
#def on_message1(cliente, userdata, mensaje):
    #print(f"Mensaje recibido: {mensaje.payload.decode()} en el tópico: {mensaje.topic}")

# Función que se ejecuta en un hilo separado para suscribirse al broker MQTT
def suscribirse_mqtt(broker, puerto, usuario, contraseña, topico):
    try:
        # Creación del cliente MQTT
        cliente = mqtt.Client()

        # Configuración de usuario y contraseña para el broker
        cliente.username_pw_set(usuario, contraseña)

        # Configurar el callback para recibir mensajes
        cliente.on_message = on_message

        # Conexión al broker
        cliente.connect(broker, puerto)

        # Suscribirse al tópico
        cliente.subscribe(topico)

        # Mantener la conexión activa en un hilo de fondo
        cliente.loop_start()

        print("Conexión al broker MQTT exitosa y suscripción al tópico realizada")
    except Exception as e:
        print(f"Error al conectarse al broker MQTT: {e}")



def main(page:ft.Page):
    global valor_texto
    page.title="PRUEBA APP"
        # Función para manejar el evento de clic en el botón
    def on_start_click(e):
        # Crear un hilo para ejecutar la función de suscripción MQTT
        threading.Thread(
            target=suscribirse_mqtt,
            args=(
                "f7476b46.ala.dedicated.aws.emqxcloud.com",
                1883,
                "FABIAN",
                "Elektronik32",
                "ROUTER/SALIDA",
            ),
            daemon=True
        ).start()
            # Crear un componente de texto para mostrar el valor de NUMER1
    valor_texto = ft.Text("Valor de NUMER1: ", size=20)
    page.add(
        ft.CupertinoFilledButton(
            content=ft.Text("START"),
            opacity_on_click=0.3,
            on_click=lambda e: enviar_mensaje_mqtt(broker="f7476b46.ala.dedicated.aws.emqxcloud.com", puerto=1883, usuario="FABIAN", contraseña="Elektronik32", topico="ROUTER/SALIDA", mensaje=mensaje),
        ),ft.CupertinoFilledButton(
            content=ft.Text("ACTUALIZAR"),
            opacity_on_click=0.3,
            on_click=on_start_click,
        ),valor_texto
    )

ft.app(main)