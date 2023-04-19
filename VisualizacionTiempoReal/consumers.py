import json
from channels.generic.websocket import WebsocketConsumer
import cv2
import base64
import numpy as np 
from homepage import views
import serial
# timeout = 1 esto significa que el se espera 1 segundo
"""bluetooth = serial.Serial('dev/tty.HC-05-DevB', 9600, timeout=1)"""

class VisualizacionTiempoRealConsumer(WebsocketConsumer):
    """def Listo_Deteccion_Ruta():
        respuesta = "BusquedaRuta"
        response_arduino = bluetooth.readline().decode().rstrip()
        while (response_arduino != respuesta):
            response_arduino = bluetooth.readline().decode().rstrip()
            if response_arduino == respuesta:
                break
    """
    # TYPE IMAGE SEND TO SOCKET 
    TYPE_NORMALLY = "img"
    TYPE_MASK = "img_mascara"
    TYPE_READY = "img_procesada"

    # conexion serial al modulo bluetooth 
    serial_speed = 9600 # frecuencia de transmision
    serial_port = '/dev/rfcomm0' # conectar al puerto serial hc-06

    conexion = serial.Serial(serial_port, serial_speed, timeout=1)
    print ("sending message to turn on PIN 13 ...")
    conexion.write(b'b')

    def compresion_img(self, imagen_comprimida):
        img_encoded = cv2.imencode('.jpg', imagen_comprimida)[1]
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        return img_base64

    def send_img_socked(self, TYPE, imagen):
        imagen_lista = self.compresion_img(imagen)
        self.send(text_data=json.dumps({
                    'type': f'{TYPE}',
                    'message': imagen_lista
                }))
        
    def marcar_objeto(self, contours, imagen, img_morph):
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        centroid_x = x + w//2
        centroid_y = y + h//2
        cv2.circle(imagen, (centroid_x, centroid_y), 10, (0,255,0), -1)
        cv2.line(imagen, (0, centroid_y), (img_morph.shape[1], centroid_y), (0,255,0), 1)
        cv2.line(imagen, (centroid_x, 0), (centroid_x, imagen.shape[0]), (0,255,0), 1)
        cv2.rectangle(imagen, (x, y), (x + w, y + h), (20, 255,0), 2)
        cv2.putText(imagen, f'(Detectado)', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (20, 255, 0), 2)
        return (centroid_x, centroid_y)
    
    def Eliminacion_ruido_img(self, mask):
        img_gaussian = cv2.GaussianBlur(mask, (5,5), 0)
        kernel = np.ones((5,5),np.uint8)
        img_morph = cv2.morphologyEx(img_gaussian, cv2.MORPH_OPEN, kernel)
        return img_morph
    
    def Eleccion_paquete(self, captura, lower_color, upper_color):
        i = 0 
        # cargar dimensiones de la imagen 
        ret, imagen = captura.read()
        print("hyola estoy antes")
        w = imagen.shape[1]
        print(w,"hola estoy aqui")
        # seccionamiento de la imagen 
        IZQUIERDA = [0.0, (w/3)]

        CENTRO = [(IZQUIERDA[1] + 1), ((IZQUIERDA[1] + 1) * 2)]

        DERECHA = [(CENTRO[1] + 1), (w)]

        while(captura.isOpened()):

            ret, imagen = captura.read()
            
            if ret == True:

                # cargar imagen original 

                self.send_img_socked(self.TYPE_NORMALLY, imagen)

                # Cargar imagen a escala de grises 

                hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_color, upper_color)
                
                img_morph = self.Eliminacion_ruido_img(mask)

                #img_morph = cv2.morphologyEx(img_morph, cv2.MORPH_CLOSE, kernel)
                self.send_img_socked(self.TYPE_MASK, img_morph)

                # Encontrar contornos

                contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Dibujar un rectángulo alrededor del contorno de mayor área

                if len(contours) > 0:
                    
                    centroid_x_and_y = self.marcar_objeto(contours, imagen, img_morph)
                    # Identificar posicion del paquete 

                    if((centroid_x_and_y[0]) in range(int(IZQUIERDA[0]), int(IZQUIERDA[1]))):
                        posicion = "Izquierda"
        
                    elif((centroid_x_and_y[0]) in range(int(DERECHA[0]), int(DERECHA[1]))):
                        posicion = "Derecha"

                    elif((centroid_x_and_y[0]) in range(int(CENTRO[0]), int(CENTRO[1]))):
                        posicion = "Centro"
                    
                    self.send_img_socked(self.TYPE_READY, imagen)

                    # por precision al frame numero 20 se enviar la señal al arduino 
                    """if(i == 10):
                        print(f"El paquete se encuentra en {posicion}")
                        # Enviar al serial(ARDUINO) la posicion 
                        bluetooth.write(posicion)
                        # leer confirmacion de arduino 
                        response = bluetooth.readline().decode().rstrip()
                        while (response != "OK"):
                            bluetooth.write(posicion)
                            response = bluetooth.readline().decode().rstrip()
                            if response == "OK":
                                break
                    """    
                    # Mostrar las coordenadas del rectángulo sobre la imagen original
                    #cv2.putText(imagen, f'(VERDE)', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                    i = i + 1
                    if(i == 100):
                        break

        
               
    def Seguimiento_Ruta(self, captura, lower_color, upper_color):
        # AREA DE RECONOCIMIENTO 
        area_pts = np.array([[22,699],[395, 0],[403, 0], [578,699]])
        
        i = 0 
        
        while(captura.isOpened()):

            ret, imagen = captura.read()
            self.send_img_socked(self.TYPE_NORMALLY, imagen)

            mask = np.zeros(imagen.shape[:2], np.uint8)
            # punts para imgen de dimensiones [800x700]
            pts = np.array([[22,699],[395, 0],[403, 0], [578,699]], np.int32)
            cv2.fillPoly(mask, [pts], (255, 255, 255))

            
            # Aplicar la máscara a la imagen original
            masked_img = cv2.bitwise_and(imagen, imagen, mask=mask)
            mask = cv2.inRange(masked_img, lower_color, upper_color)
            self.send_img_socked(self.TYPE_MASK, mask)
            cv2.drawContours(imagen, [pts], -1, (0,255, 0), 2)
           
            img_morph = self.Eliminacion_ruido_img( mask)

            # Encontrar los contornos en la máscara
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0 :
                centroid_x_and_y = self.marcar_objeto(contours, imagen, img_morph)
                self.send_img_socked(self.TYPE_READY, imagen)               
    
    def Ruta_destino(self, ruta_color, captura):
        print("entre")
        print(ruta_color)
        print(type(ruta_color))
        # ruta_color es el numero de la prioridad 
        # es decir que los de prioridad 1 van por la ruta color amarillo...
        if(ruta_color == "1"):
            print("voy amarillo")
            lower_yellow = np.array([20, 50, 50])
            upper_yellow = np.array([60, 255, 255])
            # el carrito debe ir y venir (hay que modificar algo pq esta solo para renocimiento Eleccion_paquete)
            # o crear otra funcion
            self.send(text_data=json.dumps({
                    'type': 'ColorRuta',
                    'message': "A"
                }))
            self.Seguimiento_Ruta(captura, lower_yellow, upper_yellow)
        elif(ruta_color == "2"):
            lower_green = np.array([40, 50, 50]) 
            upper_green = np.array([70, 255, 255])
            self.send(text_data=json.dumps({
                    'type': 'ColorRuta',
                    'message': "V"
                }))
            self.Seguimiento_Ruta(captura, lower_green, upper_green)
        elif(ruta_color == "3"):
            lower_red = np.array([175, 100, 20], np.uint8)
            upper_red = np.array([179, 255, 255], np.uint8) 
            self.send(text_data=json.dumps({
                    'type': 'ColorRuta',
                    'message': "R"
                }))
            self.Seguimiento_Ruta(captura, lower_red, upper_red)
    
    def connect(self):
    
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected'
        }))
        # captura de video 
        # 38 cm de distancia aproximadamente
        url = "http://192.168.105.75:8080/video"
        captura = cv2.VideoCapture(url)
        # amarillo verde rojo 
       
        i = 1
        while(i <= 3):
            if(int(views.prioridad_amarillo) == i):
                print(f"{i} amarillo")
                lower_yellow = np.array([20, 50, 50])
                upper_yellow = np.array([60, 255, 255])
                self.send(text_data=json.dumps({
                    'type': 'color_detectando',
                    'message': "A"
                }))
                # aplicando procesamiento para tomar el paquete 
                self.Eleccion_paquete(captura, lower_yellow, upper_yellow)
                # aplicar el procesamiento para ir a dejar el paquete 
                color_ruta = views.destino_amarillo
                # manda a buscar su ruta 
                # tiene que esperar una señal del arduino que el paquete ya esta listo para llevarse
                # observacion !!!!!!!!!!!!!


                # hasta recibir una respuesta del arduino que se encuentra en poscion para busqueda de ruta

                #self.Listo_Deteccion_Ruta()

                # busqueda de ruta 
                print("voy a buscar ruta")
                self.Ruta_destino(color_ruta, captura)

            elif(int(views.prioridad_verde) == i):
                print(f"{i} verde")        
                lower_green = np.array([40, 50, 50]) 
                upper_green = np.array([70, 255, 255])
                self.send(text_data=json.dumps({
                    'type': 'color_detectando',
                    'message': "V"
                }))
                self.Eleccion_paquete(captura, lower_green, upper_green)

                # soluciones
                # 1- esperar una señal del arduino que ya termino
                # 2- mandar todo los datos directamente (no viable kreo)

            elif(int(views.prioridad_rojo) == i):
                print(f"{i} rojo")
                lower_red = np.array([175, 100, 20], np.uint8)
                upper_red = np.array([179, 255, 255], np.uint8)
                self.send(text_data=json.dumps({
                    'type': 'color_detectando',
                    'message': "R"
                }))
                self.Eleccion_paquete(captura, lower_red, upper_red)
                
            i = i + 1