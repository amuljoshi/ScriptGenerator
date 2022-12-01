import pandas as pd

def main():
 
    #READ datas from Google and MML
    df = pd.read_csv('Google.csv')
    
    df_temp = pd.read_excel('MML.xlsx')
    df_xlsx = pd.read_excel('MML.xlsx')

    # print(df_temp)
    # print(df_xlsx)
    
    updater = 0
    generator = 0

    for i in range(0,df_temp.shape[0]):
        generator = generator + 1        
        filtername = "f_youtube_"f"{generator:03}"
        # print("GF:"+filtername) 
        # print("DF:"+df_temp.loc[i,"Filtername"])
        if(filtername == df_temp.loc[i,'Filtername']):
            df_xlsx.loc[updater] = df_temp.loc[i]
            updater = updater + 1

        else:
            while filtername != df_temp.loc[i,'Filtername']:
                # print(updater)
                # print(df_xlsx.loc[updater], df_temp.loc[i])
                df_xlsx.loc[updater] = df_temp.loc[i]
                # print(df_xlsx.loc[updater,["Filtername","SVRENDPORT"]])
                df_xlsx.loc[updater,["Filtername","Ip Address","Subnet","SVRENDPORT"]] = [ filtername ,"Blank","Blank","Blank"]
                # print(df_xlsx.loc[updater])
                updater = updater + 1
                generator = generator + 1
                filtername = "f_youtube_"f"{generator:03}"
                if (filtername == df_temp.loc[i,'Filtername']):
                    df_xlsx.loc[updater] = df_temp.loc[i]
                    updater = updater + 1
                    break
    
    # print(df_xlsx)            

    current = 0 
    latest = 0
    
    # Check to see the Ips to be removed and save in dataframe df_xlsx
    for i in range(df_xlsx.shape[0]):
        # print(df_xlsx.loc[i,"Ip Prefix"])
        df_xlsx.loc[i,'Ip Prefix'] = df_xlsx.loc[i,'Ip Address']+"/"+str(df_xlsx.loc[i,'Subnet'])
        # print(df_xlsx.loc[i,"Ip Prefix"])
        count = 0
        for j in range(df.shape[0]):
            if(df_xlsx.loc[i,'Ip Prefix'] == df.loc[j,'IP Prefix']):
                # print(j, count,"this is break")
                break
            count = count + 1
        if(count == df.shape[0] and df_xlsx.loc[i,"SVRENDPORT"] != "Blank"):
            df_xlsx.loc[i,"SVRENDPORT"] = "Remove"  
            current = current + 1
            print(df_xlsx.loc[i,"SVRENDPORT"],df_xlsx.loc[i,"Ip Prefix"]) 
    # print(df_xlsx)
    # print(df)

    # Check to see the Ips to be added and save in dataframe df
    for i in range(df.shape[0]):
        count = 0
        for j in range(df_xlsx.shape[0]):
            if(df.loc[i,'IP Prefix'] == df_xlsx.loc[j,'Ip Prefix']):
                # print(j, count,"this is break")
                break
            count = count + 1
        if(count == df_xlsx.shape[0]):
            df.loc[i,"Services"] = "New" 
            latest = latest + 1 
            print(df.loc[i,"Services"],df.loc[i,"IP Prefix"]) 

    # print(df)
    # print(current, latest)

    blank = 0
    for i in range(df_xlsx.shape[0]):
        if(df_xlsx.loc[i,"SVRENDPORT"] == "Blank"):
            blank = blank + 1
    # print(blank)
    counter = 0

    # print(df_xlsx)
    if(current + blank > 0):
        for k in range(df_xlsx.shape[0]):
            # print(df_xlsx.loc[k,"SVRENDPORT"])
            if(df_xlsx.loc[k,"SVRENDPORT"] == "Blank" or df_xlsx.loc[k,"SVRENDPORT"] == "Remove"):
                for l in range(df.shape[0]):
                    if(df.loc[l,"Services"] == "New"):
                        if(df_xlsx.loc[k,"SVRENDPORT"] == "Remove"):
                            df_xlsx.loc[k,"SVRENDPORT"] = "Assigned"
                        else:
                            df_xlsx.loc[k,"SVRENDPORT"] = "New"
                        df.loc[l,"Services"] = "Assigned"
                        df_xlsx.loc[k,['Ip Address', 'Subnet']] = df.loc[l,'IP Prefix'].split('/')
                        break
    
    # print(df_xlsx)
    # print(df)

    counter = 0
    l = df_xlsx.shape[0]
    while latest - current - blank - counter > 0:
        for i in range(df.shape[0]):
            if(df.loc[i,"Services"] == "New"):
                l = l + 1
                df.loc[i,"Services"] = "Assigned"
                df_xlsx.loc[l,['Ip Address', 'Subnet']] = df.loc[i,'IP Prefix'].split('/')
                df_xlsx.loc[l,'SVRENDPORT'] = "New"
                # print(l)
                df_xlsx.loc[l,'Filtername'] = "f_youtube_{:03d}".format(l)
                # print(df_xlsx.loc[l,'Ip Address'], df_xlsx.loc[l,'Subnet'])
                counter =  counter + 1
                break
                
    # print(df_xlsx.shape[0], df.shape[0])

    df_xlsx.to_csv ('Output.csv', index = False, header=True) 
    output = pd.read_csv('Output.csv')

    # print(output)
    # print(output.shape[0])

    with open("output.txt","w") as file:
        file.write('*****************\nSCRIPT: \n*****************\n\n')
        print('\n*****************\nSCRIPT: \n*****************\n')
        file.close()
    with open("output.txt","a") as file:
        for i in range(output.shape[0]):
            # print(counter)
            if(output.loc[i,"SVRENDPORT"] == "Assigned"):
                print('MOD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';')
                file.write('MOD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';\n') 
            elif(output.loc[i,"SVRENDPORT"] == "New"):
                print('ADD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';')
                print('ADD FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+output.loc[i,'Filtername']+'";')
                file.write('ADD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';\n')
                file.write('ADD FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
            elif(output.loc[i,"SVRENDPORT"] == "Remove"):
                print('RMV FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+output.loc[i,'Filtername']+'";')
                print('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+output.loc[i,'Filtername']+'";')
                file.write('RMV FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
                file.write('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
        rollback = output
        file.write('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n\n*****************\nROLLBACK SCRIPT: \n*****************\n\n')
        print('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n\n*****************\nROLLBACK SCRIPT: \n*****************\n')
        for i in range(rollback.shape[0]):
            if(rollback.loc[i,"SVRENDPORT"] == "Assigned"):
                rollback.loc[i,['Ip Address', 'Subnet']] = rollback.loc[i,'Ip Prefix'].split('/')
                print('MOD FILTER: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+rollback.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(rollback.loc[i,'Subnet'])+';')
                file.write('MOD FILTER: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+rollback.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(rollback.loc[i,'Subnet'])+';\n') 
            elif(rollback.loc[i,"SVRENDPORT"] == "New"):
                print('RMV FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                print('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                file.write('RMV FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')
                file.write('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')                
            elif(rollback.loc[i,"SVRENDPORT"] == "Remove"):
                print('ADD FILTER: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+rollback.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(rollback.loc[i,'Subnet'])+';')
                print('ADD FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                file.write('ADD FILTER: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+rollback.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(rollback.loc[i,'Subnet'])+';\n')
                file.write('ADD FLTBINDFLOWF: FLOWFILTERNAME="fg_youtube", FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')
        file.write('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n')
        print('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n')
        
        # cwd = os.getcwd()
        # print("Result saved in \nDirectory: "+cwd+"\nFilename: output.txt")
    file.close()

if __name__ == "__main__":
    main()
