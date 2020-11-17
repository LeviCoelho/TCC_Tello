import sys
import traceback
import tellopy
import av
import cv2, os  # for avoidance of pylint error
import numpy
import time
import datetime
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font
import threading

date_fmt = '%Y-%m-%d_%H%M%S'

def find(name, path):
    for root, dirs, files in os.walk(path):
        if (name in files) or (name in dirs):
            return os.path.join(root, name)
    # Caso nao encontre, recursao para diretorios anteriores
    return find(name, os.path.dirname(path))

def main():

    drone = tellopy.Tello()
    tempo = time.time()

    # Criando as threads
    xml_path = '/home/levi/TCC_Tello/haarcascade_frontalface_alt_tree.xml' 
    
    # TODO: Inicializar Classificador
    clf = cv2.CascadeClassifier(xml_path)

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        retry = 3
        container = None
        while container is None and 0 < retry:
            retry -= 1
            try:
                container = av.open(drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print('retry...')

        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    print('Wait %s/300'%frame)
                    continue

                tempoTotal = time.time() - tempo
                if tempoTotal >= 20 and tempoTotal <= 21:
                    print("takeoff")
                    drone.takeoff()
                if tempoTotal >= 30 and tempoTotal <= 31:
                    print("forward")
                    drone.forward(15)
                if tempoTotal >= 45 and tempoTotal <= 46:
                    print("counter_clockwise")
                    drone.counter_clockwise(15)
                #if tempoTotal >= 121 and tempoTotal <= 122:
                #    print("forward")
                #    drone.forward(15)
                if tempoTotal >= 50 and tempoTotal <= 51:
                    print("land")
                    drone.land()
                print("Tempo %d" % (tempoTotal))
                
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_BGR2GRAY)

                # TODO: Classificar
                faces = clf.detectMultiScale(image)
             
                # TODO: Desenhar retangulo
                for x, y, w, h in faces:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0))
                    # Create a file in ~/Pictures/ to receive image data from the drone.
                    path = '%s/Pictures/tello-%s.jpeg' % (os.getenv('HOME'),datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
                    cv2.imwrite(path,image)

                 # Visualizar
                cv2.imshow('Faces',image)
                
                cv2.waitKey(1)
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time)/time_base)
                    

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()
    
    
