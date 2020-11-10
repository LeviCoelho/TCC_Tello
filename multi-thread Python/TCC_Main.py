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

tempo = time.time()
     

date_fmt = '%Y-%m-%d_%H%M%S'

def status_print(text):
    pygame.display.set_caption(text)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if (name in files) or (name in dirs):
            return os.path.join(root, name)
    # Caso nao encontre, recursao para diretorios anteriores
    return find(name, os.path.dirname(path))


class minhaThread (threading.Thread):
    tempo = time.time()
 
    def __init__(self, threadID, nome):
        #my_drone = drone
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.nome = nome

    def run(self):
        tempoTotal = time.time() - tempo
    
        if 30 >= tempoTotal:
            print("takeoff")
            #drone.takeoff()
        if tempoTotal >= 60 and 30 >= tempoTotal:
            print("forward")
            #my_drone.forward(15)
        if tempoTotal >= 90:
            print("land")
            #my_drone.land()
        print("Tempo Thread %d" % (tempoTotal))
        # while True:
        #     time.sleep(1)
        #     tempoTotal = time.time() - tempo
        #     print("Tempo Thread %d" % (tempoTotal))

def processo(nome, contador):
    while contador:
        print ("Thread %s fazendo o processo %d" % (nome, contador))
        contador -= 1



def main():

    drone = tellopy.Tello()
    # Criando as threads
    thread1 = minhaThread(1, "Mover")
    xml_path = '/home/levi/TCC_Tello/haarcascade_frontalface_alt2.xml' 
    
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
        setup = True
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    print('Wait %s/300'%frame)
                    continue
                
                if setup:
                    print("Iniciando thread")
                    time.sleep(10)
                    # Comecando novas Threads
                    thread1.start()
                    
                    threads = []
                    threads.append(thread1)
                    setup = False
                    print("Thread iniciada")
                
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

    
    for t in threads:
        t.join()
    
if __name__ == '__main__':
    main()
    
    
