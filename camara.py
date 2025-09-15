import cv2
import mediapipe as mp
import os
from datetime import datetime
import time

# Crear carpeta de alertas si no existe
carpeta_alertas = "alertas"
os.makedirs(carpeta_alertas, exist_ok=True)

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

#Delay de las alertas
ultimo_guardado = 0
delay_segundos = 15

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            # Dibujar detecciones
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)

            # Guardar captura con timestamp
            ahora = time.time()
            if ahora - ultimo_guardado >= delay_segundos:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(carpeta_alertas, f"alerta_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                print(f"[ALERTA] Cara detectada, guardado: {filename}")
                ultimo_guardado = ahora

        cv2.imshow("Camara Seguridad", frame)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or cv2.getWindowProperty("Camara Seguridad", cv2.WND_PROP_VISIBLE) < 1:
            break
        elif tecla == ord('s'): #Guardado imagen manual
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(carpeta_alertas, f"alerta_manual_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[MANUAL] guardado manual: {filename}")
cap.release()
cv2.destroyAllWindows()