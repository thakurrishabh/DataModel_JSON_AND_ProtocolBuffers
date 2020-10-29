import json
import socket

def Main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('3.96.144.25', 4000)

    s.connect(server_address)
    try:

        Benchmark_Types=['DVD-testing','DVD-training','NDBench-testing','NDBench-training']
        Workload_Metrics=['CPUUtilization_Average','NetworkIn_Average','NetworkOut_Average','MemoryUtilization_Average']

        RFW_ID=input('Enter RFW ID: ')
        Benchmark_Type=input('Select Benchmark Type 1.DVD-testing 2.DVD-training 3.NDBench-testing 4.NDBench-training: ')
        Workload_Metric=input('Select Workload Metric 1.CPUUtilization_Average 2.NetworkIn_Average 3.NetworkOut_Average 4.MemoryUtilization_Average: ')
        Batch_Unit=input('Enter Batch unit: ')
        Batch_ID=input('Enter Batch ID: ')
        Batch_Size=input('Enter Batch Size: ')

        RFW={
            'RFW_ID':RFW_ID,
            'Benchmark_Type':Benchmark_Types[int(Benchmark_Type)-1],
            'Workload_Metric':Workload_Metrics[int(Workload_Metric)-1],
            'Batch_Unit':Batch_Unit,
            'Batch_ID':Batch_ID,
            'Batch_Size':Batch_Size
        }

        data= json.dumps(RFW)
        s.sendall(data.encode('utf-8'))
        data = s.recv(65536)
        data = data.decode('utf-8')
        print("Received from server: " + data)

    finally:
        s.close()

if __name__=='__main__':
    Main()
