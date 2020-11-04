import socket
import json
import csv
import pandas as pd
import numpy as np

def main():

    host = '172.31.17.67' #Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    data_header={
        'CPUUtilization_Average':0,
        'NetworkIn_Average':1,
        'NetworkOut_Average':2,
        'MemoryUtilization_Average':3,
        'Final_Target':4
    }


    print("Server Started")
    while True:
        s.listen(2)
        conn,addr = s.accept()
        data = conn.recv(1024).decode('utf-8')
        print("From connected user: " + data)
        transit_data=json.loads(data)

        ''' csv query of data '''
        batch_unit=int(transit_data['Batch_Unit'])
        batch_ID=int(transit_data['Batch_ID'])-1
        batch_size=int(transit_data['Batch_Size'])
        metric_h=transit_data['Workload_Metric']
        metric=data_header[metric_h]
        filename=transit_data['Benchmark_Type']+'.csv'

        pd_dataframe= pd.read_csv(filename)
        sample_req=pd_dataframe[metric_h][((batch_unit*batch_ID)):((batch_unit*batch_ID))+(batch_unit*batch_size)]
        sample_req=sample_req.to_numpy().tolist()
        print(sample_req)

        send_data={}
        send_data['RFW_ID']=transit_data['RFW_ID']
        send_data['last_Batch_ID']=int(transit_data['Batch_ID'])+int(transit_data['Batch_Size'])
        send_data['samples_requested']=sample_req
        send=json.dumps(send_data)
        print(send_data)
        conn.sendall(send.encode('utf-8'))
    s.close()

if __name__=='__main__':
    main()
