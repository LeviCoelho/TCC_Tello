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
     

class minhaThread (threading.Thread):
    tempo = time.time()
 
    def __init__(self, threadID, nome, contador):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.nome = nome
        self.contador = contador
        tempo = time.time()
 
    def run(self):
        while True:
            time.sleep(1)
            tempoTotal = time.time() - tempo
            print("Tempo Thread %d" % (tempoTotal))

def processo(nome, contador):
    while contador:
        print ("Thread %s fazendo o processo %d" % (nome, contador))
        contador -= 1



def main():

    # Criando as threads
    thread1 = minhaThread(1, "Mover", 8)
    # Comecando novas Threads
    thread1.start()
    
    
    threads = []
    threads.append(thread1)

    #while True:
    #    time.sleep(1)
    #    tempoTotal = tempo - time.time()
    #    print("Tempo Main %d" % (tempoTotal))

    
    for t in threads:
        t.join()
    
    print ("Saindo da main")
    
if __name__ == '__main__':
    main()
    
    
