import socket
import json
import csv
import pandas as pd
import numpy as np
import messaging_pb2 as pb2

def main():

    host = '172.31.16.70' #Server ip
    port = 4000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    
    

    print("Server Started")
    while True:
        s.listen(2)
        conn,addr = s.accept()
        data = conn.recv(65536)
        transit_data=pb2.RFW()
        transit_data.ParseFromString(data)
        data_header={
        pb2.RFW.CPUUTILIZATIONAVERAGE:0,
        pb2.RFW.NETWORKINAVERAGE:1,
        pb2.RFW.NETWORKOUTAVERAGE:2,
        pb2.RFW.MEMORYUTILIZATIONAVERAGE:3,
        }
        wms={
        pb2.RFW.CPUUTILIZATIONAVERAGE:'CPUUtilization_Average',
        pb2.RFW.NETWORKINAVERAGE:'NetworkIn_Average',
        pb2.RFW.NETWORKOUTAVERAGE:'NetworkOut_Average',
        pb2.RFW.MEMORYUTILIZATIONAVERAGE:'MemoryUtilization_Average',
        }
        bts={
            pb2.RFW.DVDTESTING:"DVD-testing",
            pb2.RFW.DVDTRAINING:"DVD-training",
            pb2.RFW.NDBENCHTESTING:"NDBench-testing",
            pb2.RFW.NDBENCHTRAINING:"NDBench-training",
        }
        ''' csv query of data '''
        batch_unit=transit_data.Batch_Unit
        batch_ID=transit_data.Batch_ID-1
        batch_size=transit_data.Batch_Size
        metric_h=transit_data.Workload_Metric
        metric=data_header[metric_h]
        filename=bts[transit_data.Benchmark_Type]+'.csv'

        pd_dataframe= pd.read_csv(filename)
        sample_req=pd_dataframe[wms[metric_h]][((batch_unit*batch_ID)):((batch_unit*batch_ID))+(batch_unit*batch_size)]
        sample_req=sample_req.to_numpy().tolist()
        print(sample_req)

        send_data=pb2.RFD()
        send_data.RFW_ID=transit_data.RFW_ID
        send_data.last_Batch_ID=transit_data.Batch_ID+transit_data.Batch_Size
        send_data.datasamples.extend(sample_req)
        conn.sendall(send_data.SerializeToString())
    s.close()

if __name__=='__main__':
    main()
