import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads
     
     #Task2:add semaphores for synchronization
     self.empty_slots =threading.Semaphore(self.NUM_PRINTERS)
     #semaphores ti track availablrs slots
     self.mutex =threading.Semaphore(1)
     #mutex to make sure mutual exclusion when access the queue

    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here
            print("starting simulation and creating threads.")
            for i in range (self.NUM_MACHINES):
                machine=self.machineThread(i,self)
                self.mThreads.append(machine)
                for i in range  (self.NUM_PRINTERS):
                    printer =self.printerThread(i,self)
                    self.pThreads.append(printer)

        # Start all the threads
        # Write code here
    print("Starting all threads")
    for t in self.mThreads + self.pThreads：
    t.start()
        # Let the simulation run for some time
        print(f"Simulation will run for {self.SIMULATION_TIME}seconds.")
        time.sleep(self.SIMULATION_TIME)

        # Finish simulation
        print("\nStopping simulation...")
        self.sim_active = False

        # Wait until all printer threads finish by joining them
        # Write code here
        for printer in self.pThreads：
        printer.join()

        print("Simulation finished.")
     #The program will exit after main thread and printer threads finish 

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                # Write code here
                self.printDox(self.printerID)

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            # Print from the queue
            self.outer.print_list.queuePrint(printerID)

            #Task2:acquire mutex before accessing the shared queue
        self.outer.mutex.acquire()
        try:
            #print from the queue(this also removes the head)
            self.outer.print_list.queuePrint(printerID)
            finally:
                #always release the mutex
                self.outer.mutex.release()
        #Task 2:after printing, one slot in the queue become free.
        #realease the empty_slots semaphore to allow a waiting machine to proceed
        self.outer.mutex.release()

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                # Write code here
                #Task2 :use semaphores to control access
                #check if it is safe
                self.isRequestSafe(self.machineID)
                #send the print request
                self.printRequest(self.machineID)
                self.postRequest(self.machineID)
               #task1 uncommemt the line below and comment  the 4 lines above for task 1
               #self.printRequest(self.machineID)
        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

      #Task:method to  acquire semaphores before inserting
      def isRequestSafe(self,id)
      #print(f"Machine {id} Checking availability") #debug printing
      #wait for  an empty slot in the queue. if queue is full, this will block
      self.outer.empty_slots.acquire()
      #acquire mutex for exclusive access to the queue
      self.outer.mutex.acquire()
     # print(f"Machine{id} will proceed")#debug printing


            def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)

#Task2:method to release semaphores after inserting
def postRequest(self,id)
#print(f"Machine {id} Releasing mutex")#debug printing
self.outer.mutex.release()