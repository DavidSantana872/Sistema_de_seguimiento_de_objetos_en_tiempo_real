import json
from channels.generic.websocket import WebsocketConsumer
import cv2
import base64
import numpy as np 
from homepage import views
class VisualizacionTiempoRealConsumer(WebsocketConsumer):
    def Procesamiento_img(self, captura, lower_color, upper_color):
        while(captura.isOpened()):
            ret, imagen = captura.read()
            if ret == True:
                img_encoded = cv2.imencode('.jpg', imagen)[1]
                # Convertir la imagen codificada en bytes a una cadena base64 que se puede incrustar en la página web
                img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                
                # Enviar por el socket la imagen original
                self.send(text_data=json.dumps({
                    'type': 'img',
                    'message': img_base64
                }))
                hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_color, upper_color)
                # quitar ruido 
                kernel = np.ones((15,15),np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                # enviar imagen en mascara de grises 
                img_encoded = cv2.imencode('.jpg', mask)[1]
                # Convertir la imagen codificada en bytes a una cadena base64 que se puede incrustar en la página web
                img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                self.send(text_data=json.dumps({
                    'type': 'img_mascara',
                    'message': img_base64
                }))
                # Encontrar contornos
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # Dibujar un rectángulo alrededor del contorno de mayor área
                if len(contours) > 0:
                    cnt = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(cnt)
                   #print(w,h)
                    cv2.rectangle(imagen, (x, y), (x + w, y + h), (20, 255,0), 2)
                    cv2.putText(imagen, f'(Detectado)', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (20, 255, 0), 2)
                    img_encoded = cv2.imencode('.jpg', imagen)[1]
                    # Convertir la imagen codificada en bytes a una cadena base64 que se puede incrustar en la página web
                    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                    self.send(text_data=json.dumps({
                        'type': 'img_procesada',
                        'color' : upper_color
                    }))
                    # Mostrar las coordenadas del rectángulo sobre la imagen original
                    #cv2.putText(imagen, f'(VERDE)', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
    def Ruta_destino(self, ruta_color, captura):
        # ruta_color es el numero de la prioridad 
        # es decir que los de prioridad 1 van por la ruta color amarillo...
        if(ruta_color == 1):
            lower_yellow = np.array([20, 50, 50])
            upper_yellow = np.array([60, 255, 255])
            # el carrito debe ir y venir (hay que modificar algo pq esta solo para renocimiento procesamiento_img)
            # o crear otra funcion
            self.Procesamiento_img(captura, lower_yellow, upper_yellow)
            self.send(text_data=json.dumps({
                    'type': 'ColorRuta',
                    'message': "A"
                }))

        elif(ruta_color == 2):
            lower_green = np.array([40, 50, 50]) 
            upper_green = np.array([70, 255, 255])
            self.Procesamiento_img(captura, lower_green, upper_green)
            self.send(text_data=json.dumps({
                    'type': 'ColorRuta',
                    'message': "V"
                }))

        elif(ruta_color == 3):
            lower_red = np.array([175, 100, 20], np.uint8)
            upper_red = np.array([179, 255, 255], np.uint8)
            self.Procesamiento_img(captura, lower_red, upper_red)
            self.send(text_data=json.dumps({
                    'type': 'ColorRuta',
                    'message': "R"
                }))
            

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected'
        }))
        # captura de video 
        url = "http://192.168.1.135:8080/video"
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
                self.Procesamiento_img(captura, lower_yellow, upper_yellow)
                # aplicar el procesamiento para ir a dejar el paquete 
                color_ruta = views.destino_amarillo
                # manda a buscar su ruta 
                self.Ruta_destino(color_ruta, captura)

            elif(int(views.prioridad_verde) == i):
                print(f"{i} verde")        
                lower_green = np.array([40, 50, 50]) 
                upper_green = np.array([70, 255, 255])
                self.send(text_data=json.dumps({
                    'type': 'color_detectando',
                    'message': "V"
                }))
                self.Procesamiento_img(captura, lower_green, upper_green)

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
                self.Procesamiento_img(captura, lower_red, upper_red)
                
            i = i + 1
        

        
        
        
        

        
            
                


