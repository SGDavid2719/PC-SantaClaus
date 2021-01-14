import threading
import time
import random

# PROCESSES

SANTA_CLAUS = 1
REINDEER = 9
ELF = 9

# NUMBER ITERATIONS

TO_ASK = 2
TO_RESPONSE = 6
TO_HOOK = 1

# COUNTERS

nReindeer = 0
nElf = 0

# NAMES

names_Reindeer = ["DANCER","PRANCER","DONCER","BLITZEN","COMET","VIXEN","DASHER","RUDOLPH","CUPID"]
names_Elf = ["Taleasin","Halafarin","Adamar","Galather","Ailduin","Estelar","Lyari","Andrathath","Wyn"]

# BINARI SEMAPHORES

mutex = threading.Lock()

# COUNTER SEMAPHORES

sleeping = threading.Semaphore(0)
waitReindeer = threading.Semaphore(0)
waitTurn = threading.Semaphore(0)
needHelp = threading.Semaphore(3)

# SANTA CLAUS

def SantaClaus():
  
  # 6 PETITIONS AND 1 HOOK
  for i in range(TO_RESPONSE + TO_HOOK):
    print("-------> Santa says: I'm tired")
    print("-------> Santa says: I'm going to sleep")

    # WAITS PETITIONS
    sleeping.acquire()

    print("-------> Santa says: I'm awake ho ho ho!")

    global nReindeer

    mutex.acquire()

    # WITH 9 REINDEERS TO HOOK OR 3 ELF'S PETITIONS
    if nReindeer == 9 :
      
      nReindeer = 0

      mutex.release()

      print("-------> Santa says: Toys are ready!")
      print("-------> Santa loads the toys")
      print("-------> Santa says: Until next Christmas!")

      for m in range(REINDEER):
        waitReindeer.release()

    else :
        
      mutex.release()

      print("-------> Santa says: What is the problem?")

      for j in range(3):
        print("-------> Santa helps the elf "+str(j+1)+" of "+str(3))
        waitTurn.release()

      mutex.acquire()
      global nElf
      nElf = nElf - 3
      mutex.release()

      for m in range(ELF):
        needHelp.release()

    print("-------> Santa Ends turn "+str(i))

  print("-------> Santa Ends")

# REINDEER

def Reindeer(nameR):

  time.sleep(random.randint(6, 10))

  print("       "+"Reindeer "+nameR+" arrives")

  mutex.acquire()
  global nReindeer
  nReindeer = nReindeer + 1

  if nReindeer == 9 :
    sleeping.release()

  mutex.release()

  waitReindeer.acquire()

  print("       "+nameR+" ready and hitched")
  print("       "+"Reindeer "+nameR+" Ends")

# ELF

def Elf(nameE):

  for i in range(TO_ASK):

    print("   "+"Hi I am the elf "+nameE)

    time.sleep(random.randint(2,4))

    needHelp.acquire()

    mutex.acquire()
    global nElf
    nElf = nElf + 1
    t = nElf % 3
    mutex.release()

    if t == 0 :
        
      sleeping.release()
      print("   "+nameE+" says: I have a question, I'm the "+str(3)+" SANTAAAAA!")

    else :
        
      print("   "+nameE+" says: I have a question, I'm the "+str(t)+" waiting")

    waitTurn.acquire()

    print("   "+"The elf "+nameE+" is getting help")
    print("   "+"Elf "+nameE+" Ends")

# MAIN

def main():
  threads = []

  print ("STARTS SIMULATION")

  a = threading.Thread(target=SantaClaus)
  threads.append(a)

  for i in range(REINDEER):
    b = threading.Thread(target=Reindeer, args=(str(names_Reindeer[i]),))
    threads.append(b)

  for i in range(ELF):
    c = threading.Thread(target=Elf, args=(str(names_Elf[i]),))
    threads.append(c)

  for t in threads:
    t.start()

  for t in threads:
    t.join()

if __name__ == "__main__":
  main()