import Client_message_pb2
import socket

def Main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('3.96.144.25', 4000)

    s.connect(server_address)
    try:
        rfw= Client_message_pb2.RFW()
        Benchmark_Types=[Client_message_pb2.RFW.DVDTESTING ,Client_message_pb2.RFW.DVDTRAINING ,Client_message_pb2.RFW.NDBENCHTESTING ,Client_message_pb2.RFW.NDBENCHTRAINING ]
        Workload_Metrics=[Client_message_pb2.RFW.CPUUTILIZATIONAVERAGE ,Client_message_pb2.RFW.NETWORKINAVERAGE,Client_message_pb2.RFW.NETWORKOUTAVERAGE ,Client_message_pb2.RFW.MEMORYUTILIZATIONAVERAGE]

        rfw.RFW_ID =input('Enter RFW ID: ')
        rfw.Benchmark_Type=input('Select Benchmark Type 1.DVD-testing 2.DVD-training 3.NDBench-testing 4.NDBench-training: ')
        rfw.Workload_Metric=input('Select Workload Metric 1.CPUUtilization_Average 2.NetworkIn_Average 3.NetworkOut_Average 4.MemoryUtilization_Average: ')
        rfw.Batch_Unit=input('Enter Batch unit: ')
        rfw.Batch_ID=input('Enter Batch ID: ')
        rfw.Batch_Size=input('Enter Batch Size: ')

        RFW={
            'RFW_ID':RFW_ID,
            'Benchmark_Type':Benchmark_Types[int(Benchmark_Type)-1],
            'Workload_Metric':Workload_Metrics[int(Workload_Metric)-1],
            'Batch_Unit':Batch_Unit,
            'Batch_ID':Batch_ID,
            'Batch_Size':Batch_Size
        }

        data= rfw.SerializeToString()
        s.sendall(data.encode('utf-8'))
        data = s.recv(65536)
        data = data.decode('utf-8')
        print("Received from server: " + data)

    finally:
        s.close()

if __name__=='__main__':
    Main()
