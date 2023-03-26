import json
from channels.generic.websocket import WebsocketConsumer
import cv2
import base64
import numpy as np 

class VisualizacionTiempoRealConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected'
        }))
        # captura de video 
        url = "ip de video "
        captura = cv2.VideoCapture(url)

        #rango de colores 
        lower_blue = np.array([100, 50, 50]) 
        upper_blue = np.array([130, 255, 255])

        lower_red = np.array([175, 100, 20], np.uint8)
        upper_red = np.array([179, 255, 255], np.uint8)
        
        lower_green = np.array([40, 50, 50]) 
        upper_green = np.array([70, 255, 255])

        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([60, 255, 255])

        while(captura.isOpened()):
            ret, imagen = captura.read()
            if ret == True:
                img_encoded = cv2.imencode('.jpg', imagen)[1]
                # Convertir la imagen codificada en bytes a una cadena base64 que se puede incrustar en la página web
                img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                
                #enviar por el socket la imagen original
                self.send(text_data=json.dumps({
                    'type': 'img',
                    'message': img_base64
                }))
                hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_green, upper_green)
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
                    cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 0, 0), 2)
                    img_encoded = cv2.imencode('.jpg', imagen)[1]
                    # Convertir la imagen codificada en bytes a una cadena base64 que se puede incrustar en la página web
                    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                    self.send(text_data=json.dumps({
                        'type': 'img_procesada',
                        'message': img_base64
                    }))
                    # Mostrar las coordenadas del rectángulo sobre la imagen original
                    #cv2.putText(imagen, f'(VERDE)', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

            
                


