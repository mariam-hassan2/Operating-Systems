
import random 
from collections import deque
import numpy as np 

#setting the maximum number of customers/ processes
Max_Customers = 50

id = 0

# priorities for processes/ customers are as the following:
# priority for high is 2 
# priority for medium is 1
# priority for low is 0



class Customer:
    # data members for the customer include the arrival time, service time, premmative priority, end time, duration_time
    def __init__(self,id):
        self.id = id
        self.arrival_time = np.random.randint(1,30)
        self.service_time = np.random.randint(1,10)
        self.prem_prio = np.random.randint(0,3)
        self.end_time = 0
        self.duration_time = self.service_time
        
# method for adding elements to the queue
# this method returns an index which helps knowing where to add the customer in the queue based on it's priority
def PQ_insert(queue_list,element):
    # for loop that iterates and compares the priorities to sort the elements in queue based on that
    for i in range(len(queue_list)):
        if queue_list[i].prem_prio > element.prem_prio:
            return i
        if queue_list[i].prem_prio == element.prem_prio:
            if(queue_list[i].arrival_time < element.arrival_time):
                return i 

    return  len(queue_list)    
    

if __name__ == "__main__": 
    Customers_list = [] 
    #
    served_list = []

    #adding customers/ processes to a list    
    for i in range(Max_Customers):
        Customers_list.append(Customer(i))
        
          
    #initializing time
    t = 0 
    priority_queue = []
    #initializing a running customer to be false
    running_customer = False
    rem_list= []

    # a while loop that iterates with these conditions :
    #  length of the customers list bigger than 0 or length of priority queue eot be bigger than 0 or existing of a running customer
    while len(Customers_list) > 0 or len(priority_queue)> 0 or running_customer: 
        # checking if any process has arrived
        for i,cus in enumerate(Customers_list): 
            if cus.arrival_time == t:
                #adding a process to the the remaining list
                rem_list.append(i)
                
                #finding the right index for the order of the process/ customer in the queue based on it's priority
                index = PQ_insert(priority_queue,cus)
                #inserting the process/customer into the priority queue
                priority_queue.insert(index,cus)

        #for loop for popping customers  out of the customers list
        for  val in reversed(rem_list): 
            
            Customers_list.pop(val)
        rem_list= []
        #print(t, len(Customers_list), len(priority_queue), len(Customers_list)+ len(priority_queue))  
        

        # checking if there is no running customer and there are other customers in the priority queue
        if (running_customer == False) & (len(priority_queue) > 0):
            #popping a customer out of the queue
            current_customer = priority_queue.pop(-1)
            running_customer = True
            #decrementing the duration time left for processing the customer
            current_customer.duration_time -=1
            # checking if the duration time left is 0
            if current_customer.duration_time == 0: 

                #saving the end time of the customer 
                current_customer.end_time = t + 1 
                # adding the customer to the list of customer that have ben served
                served_list.append(current_customer)

                #checking if there are other customers in the queue 
                if len(priority_queue) > 0: 
                    current_customer = priority_queue.pop(-1)
                else: 
                    running_customer = False 
                            
         # checking if there is already a running customer    
        elif running_customer == True:
                if len(priority_queue) > 0:
                    if current_customer.prem_prio < priority_queue[-1].prem_prio:
                        priority_queue.insert(PQ_insert(priority_queue,current_customer),current_customer)
                        current_customer = priority_queue.pop(-1)



                current_customer.duration_time -=1
                #checking if the duration time is 0
                if current_customer.duration_time == 0:  
                    current_customer.end_time = t + 1
                    #adding the customer to the list of served customers
                    served_list.append(current_customer)
                    #checking if there is other customers in the priority queue
                    if len(priority_queue) > 0: 
                        current_customer = priority_queue.pop(-1)
                    else: 
                        running_customer = False
        
        
        t+=1 



    

    # a list for wait times for processes/ customers of low priority
    low_wait_time = []
    # a list for wait times for processes/ customers of medium priority
    medium_wait_time = []
    # a list for wait times for processes/ customers of high priority
    high_wait_time = []

    # a list for processes/ customers of low priority
    low_served_list = []
    # a list for processes/ customers of medium priority
    medium_served_list = [] 
    # a list for processes/ customers of high priority
    high_served_list = []
    #iterating over the served list and and adding each item to the list of it's priority
    for i in served_list: 
        if i.prem_prio == 0:
            low_served_list.append(i)
        if i.prem_prio == 1:
            medium_served_list.append(i)
        if i.prem_prio == 2:
            high_served_list.append(i)  

    # calculating total time for each priority         
    low_total_time = low_served_list[-1].end_time - low_served_list[0].arrival_time
    medium_total_time = medium_served_list[-1].end_time - medium_served_list[0].arrival_time
    high_total_time = high_served_list[-1].end_time - high_served_list[0].arrival_time


    #Variable for calculating total wait time for low priority
    low_total_wait_time = 0
    # a for loop that iterates over the list of processes/customers of low priority
    # calculating wait time for each process/customer in the list
    for j in low_served_list:  
        temp_low = j.end_time - j.arrival_time - j.service_time 
        
        low_wait_time.append(temp_low)
        low_total_wait_time = low_total_wait_time + temp_low

    #Variable for calculating total wait time for medium priority
    medium_total_wait_time = 0   
    #for loop that iterates over the list of processes/customers of medium priority
    # calculating wait time for each process/customer in the list 
    for m in medium_served_list: 
        temp_medium = m.end_time - m.arrival_time - m.service_time 
        medium_wait_time.append(temp_medium)
        medium_total_wait_time = medium_total_wait_time + temp_medium

    #Variable for calculating total wait time for high priority
    high_total_wait_time = 0    
    #for loop that iterates over the list of processes/customers of high priority
    # calculating wait time for each process/customer in the list     
    for k in high_served_list: 
        temp_high = k.end_time - k.arrival_time - k.service_time 
        high_wait_time.append(temp_high)
        high_total_wait_time = high_total_wait_time + temp_high

    #printing throughput for each class
    #printing throughput for low priority class
    print("throughput for low priority class ", len(low_served_list)/low_total_time)
    #printing throughput for medium priority class
    print("throughput for medium priority class ", len(medium_served_list)/medium_total_time)   
    #printing throughput for high priority class
    print("throughput for high priority class ", len(high_served_list)/high_total_time) 


    #printing latency stats for each class
    #printing latency stats for low priority class
    #average wait time for low priority
    print("average wait time for low priority", low_total_wait_time/len(low_served_list))
    #minimum wait time for low priority
    print("minimum wait time for low priority", min(low_wait_time))
    #maximum wait time for low priority
    print("maximum wait time for low priority", max(low_wait_time))
    #25%ile for low priority
    print("25 percentile wait time for low priority", np.percentile(low_wait_time,25))
    #75%ile for low priority
    print("75 percentile wait time for low priority", np.percentile(low_wait_time,75))    




    #printing latency stats for medium priority class
    #average wait time for medium priority
    print("average wait time for medium priority", medium_total_wait_time/len(medium_served_list))
    #minimum wait time for medium priority
    print("minimum wait time for medium priority", min(medium_wait_time))
    #maximum wait time for medium priority
    print("maximum wait time for medium priority", max(medium_wait_time))
    #25%ile for medium priority
    print("25 percentile wait time for medium priority", np.percentile(medium_wait_time,25))
    #75%ile for medium priority
    print("75 percentile wait time for medium priority", np.percentile(medium_wait_time,75))      

    #printing latency stats for high priority class
    #average wait time for medium priority
    print("average wait time for high priority", high_total_wait_time/len(high_served_list))
    #minimum wait time for high priority
    print("minimum wait time for high priority", min(high_wait_time))
    #maximum wait time for high priority
    print("maximum wait time for high priority", max(high_wait_time))
    #25%ile for high priority
    print("25 percentile wait time for high priority", np.percentile(high_wait_time,25))
    #75%ile for high priority
    print("75 percentile wait time for high priority", np.percentile(high_wait_time,75)) 
    
