import messaging_pb2
import socket

def Main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('35.183.148.239', 4000)

    s.connect(server_address)
    try:
        rfw= messaging_pb2.RFW()
        Benchmark_Types=[messaging_pb2.RFW.DVDTESTING ,messaging_pb2.RFW.DVDTRAINING ,messaging_pb2.RFW.NDBENCHTESTING ,messaging_pb2.RFW.NDBENCHTRAINING ]
        Workload_Metrics=[messaging_pb2.RFW.CPUUTILIZATIONAVERAGE ,messaging_pb2.RFW.NETWORKINAVERAGE,messaging_pb2.RFW.NETWORKOUTAVERAGE ,messaging_pb2.RFW.MEMORYUTILIZATIONAVERAGE]

        rfw.RFW_ID =int(input('Enter RFW ID: '))
        rfw.Benchmark_Type=Benchmark_Types[int(input('Select Benchmark Type 1.DVD-testing 2.DVD-training 3.NDBench-testing 4.NDBench-training: '))-1]
        rfw.Workload_Metric=Workload_Metrics[int(input('Select Workload Metric 1.CPUUtilization_Average 2.NetworkIn_Average 3.NetworkOut_Average 4.MemoryUtilization_Average: '))-1]
        rfw.Batch_Unit=int(input('Enter Batch unit: '))
        rfw.Batch_ID=int(input('Enter Batch ID: '))
        rfw.Batch_Size=int(input('Enter Batch Size: '))

        data= rfw.SerializeToString()

        s.sendall(data)
        rec_data = s.recv(65536)

        rec_rfd= messaging_pb2.RFD()
        rec_rfd.ParseFromString(rec_data)

        print("Received from server: ")
        print("RFW_ID: "+str(rec_rfd.RFW_ID))
        print("last_Batch_ID: "+str(rec_rfd.last_Batch_ID))
        print("datasamples: "+str(rec_rfd.datasamples))


    finally:
        s.close()

if __name__=='__main__':
    Main()
