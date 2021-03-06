import sys
import traceback
import tellopy
import av
#import cv2.cv2 as cv2  # for avoidance of pylint error
import cv2, os  # for avoidance of pylint error
import numpy
import time

def find(name, path):
    for root, dirs, files in os.walk(path):
        if (name in files) or (name in dirs):
            return os.path.join(root, name)
    # Caso nao encontre, recursao para diretorios anteriores
    return find(name, os.path.dirname(path))

def main():
    drone = tellopy.Tello()

    #cv2path = os.path.dirname(cv2.__file__)
    #haar_path = find('haarcascades', cv2path)
    #xml_name = 'haarcascade_frontalface_alt2.xml'
    xml_path = '/home/levi/TCC_Tello/haarcascade_frontalface_alt2.xml' #os.path.join(haar_path, xml_name)
    
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
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_BGR2GRAY)
                cv2.imshow('Original', image)
                
                #cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                 
                # TODO: Converter para tons de cinza
                
                # TODO: Classificar
                faces = clf.detectMultiScale(image)
             
                 # TODO: Desenhar retangulo
                for x, y, w, h in faces:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0))
             
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