import re
import pandas as pd
import os


def find_lines_with_keywords(filename, keyword1, keyword2):
    lines_with_keywords = []

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if str(keyword1) in line and str(keyword2) not in line:
                lines_with_keywords.append(line)

    return lines_with_keywords


def main():
 
    #READ datas from Google and MML
    df = pd.read_csv('LatestIp.csv')
    df['IP Prefix'] = df['IP Prefix'].str.upper()
    # df_temp = pd.read_excel('MML.xlsx')
    # df_xlsx = pd.read_excel('MML.xlsx')

    # print(df_temp)
    # print(df_xlsx)

    # Initialise a tabular data to incorporate different traffic types, their filter, digits used and filtergroup. This can be taken from file in future
    Application =   { 
                    'Name':         ['Google',     'Facebook',       'Instagram',    'Tiktok',      'Google-IPV6',    'Facebook-IPV6',    'Instagram-IPV6'],
                    'Filtername':   ['f_youtube_', 'f_fbspecialip',  'f_instagram_', 'f_tiktokip_', 'f_youtubeipv6_', 'f_fbspecialipv6_', 'f_instagramipv6_'],
                    'GEN':          ['03',         '04',             '04',           '03',          '03',             '04',               '04'],
                    'Filtergroup':  ['fg_youtube', 'fg_fbspecialip', 'fg_instagram', 'fg_tiktokip', 'fg_youtube',     'fg_fbspecialip',   'fg_instagram']
                    }
    # print(Application)

    appdf = pd.DataFrame(Application)

    # Take input from user for the traffic type the script is being generated for. Since user input is disabled in for Debug Console in VISUDO, use direct userinput from script for testing.
    # userinput = 3
    print("\nPlease type the option number for the Application(Choose 0,1,2,3,etc):")
    print(appdf['Name'])
    userinput = int(input("\nYourInput: "))
    print("\n"+appdf.loc[userinput,'Name']+" selected !!\n")

    # if (userinput == '1'):
    #     print('\nGoogle selected\n')
    #     userinput = 0
    # elif (userinput == '2'):
    #     print('\nFacebook selected\n')
    #     userinput = 1
    # elif (userinput == '3'):
    #     print('\nInstagram selected\n')
    #     userinput = 2
    # else :
    #     print('\nTiktok selected\n')
    #     userinput = 3

    # initialise the necessary for filling up dataframe directly from mml configuration file
    filename = 'mmlconf.txt'
    keyword1 = appdf.loc[userinput,'Filtername']
    keyword2 = appdf.loc[userinput,'Filtergroup']
    # print(keyword1+":"+keyword2)
    lines = find_lines_with_keywords(filename, keyword1, keyword2)

    # Create DataFrame df_result with delimited values "=" and ","
    data = []
    for line in lines:
        parts = [part.strip().strip('"') for part in re.split('=|,', line)]

        data.append(parts)
    headers = ['From MML', 'Filtername', 'L34PROTTYPE', 'STRING', 'L34PROTOCOL', 'ANY', 'SVRIPMODE', 'IP', 'SVRIP', 'Ip Address', 'SVRIPMASKTYPE', 'LENGTHTYPE', 'SVRIPMASKLEN', 'Subnet', 'MSSTARTPORT', '0', 'MSENDPORT', '65535', 'SVRSTARTPORT', '0', 'SVRENDPORT', 'Ip Prefix']  # Specify the header field names here
    df_result = pd.DataFrame(data, columns=headers)

    # print(df_result)

    # Output DataFrame to Excel file MML_gen.xlsx
    output_file = 'MML_gen.xlsx'  # Specify the desired output file name
    df_result.to_excel(output_file, index=False)
    print("Generated MML saved to "+os.getcwd()+f"\{output_file}")

    # Assign the output generated MML to two data frames for comparing as well as generating output.
    df_xlsx = pd.read_excel(output_file)
    df_temp = pd.read_excel(output_file)


    print("Processing...\n")

    updater = 0
    generator = 0
    
    #Check for three 000 or four 0000 before comparing two datas
    if(appdf.loc[userinput,'GEN'] == '03'):
        for i in range(0,df_temp.shape[0]):
            generator = generator + 1        
            filtername = appdf.loc[userinput,'Filtername']+f"{generator:03}"
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
                    filtername = appdf.loc[userinput,'Filtername']+f"{generator:03}"
                    if (filtername == df_temp.loc[i,'Filtername']):
                        df_xlsx.loc[updater] = df_temp.loc[i]
                        updater = updater + 1
                        break
    
    else: 
        for i in range(0,df_temp.shape[0]):
            generator = generator + 1        
            filtername = appdf.loc[userinput,'Filtername']+f"{generator:04}"
            # print(filtername)
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
                    filtername = appdf.loc[userinput,'Filtername']+f"{generator:04}"
                    # print("else"+filtername)
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

    if(appdf.loc[userinput,'GEN'] == '03'):
        while latest - current - blank - counter > 0:
            for i in range(df.shape[0]):
                if(df.loc[i,"Services"] == "New"):
                    l = l + 1
                    df.loc[i,"Services"] = "Assigned"
                    df_xlsx.loc[l,['Ip Address', 'Subnet']] = df.loc[i,'IP Prefix'].split('/')
                    df_xlsx.loc[l,'SVRENDPORT'] = "New"
                    # print(l)
                    df_xlsx.loc[l,'Filtername'] = appdf.loc[userinput,'Filtername']+"{:03d}".format(l)
                    # print(df_xlsx.loc[l,'Ip Address'], df_xlsx.loc[l,'Subnet'])
                    counter =  counter + 1
                    break

    else: 
         while latest - current - blank - counter > 0:
            for i in range(df.shape[0]):
                if(df.loc[i,"Services"] == "New"):
                    l = l + 1
                    df.loc[i,"Services"] = "Assigned"
                    df_xlsx.loc[l,['Ip Address', 'Subnet']] = df.loc[i,'IP Prefix'].split('/')
                    df_xlsx.loc[l,'SVRENDPORT'] = "New"
                    # print(l)
                    df_xlsx.loc[l,'Filtername'] = appdf.loc[userinput,'Filtername']+"{:04d}".format(l)
                    # print(df_xlsx.loc[l,'Ip Address'], df_xlsx.loc[l,'Subnet'])
                    counter =  counter + 1
                    break
                  
    # print(df_xlsx.shape[0], df.shape[0])

    df_xlsx.to_csv ('Output.csv', index = False, header=True) 
    output = pd.read_csv('Output.csv')

    # print(output)
    # print(output.shape[0])

    #Check for ipv4 or ipv6 before printing out outputs
    if(appdf.loc[userinput,'Name'].find('-IPV6')!=-1):
        with open("outputipv6.txt","w") as file:
            file.write('*****************\nSCRIPT: \n*****************\n\n')
            print('\n*****************\nSCRIPT: \n*****************\n')
            for i in range(output.shape[0]):
                # print(counter)
                if(output.loc[i,"SVRENDPORT"] == "Assigned"):
                    print('MOD FILTERIPV6: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+output.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(int(output.loc[i,'Subnet']))+';')
                    file.write('MOD FILTERIPV6: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+output.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(int(output.loc[i,'Subnet']))+';\n') 
                elif(output.loc[i,"SVRENDPORT"] == "New"):
                    print('ADD FILTERIPV6: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+output.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(int(output.loc[i,'Subnet']))+';')
                    print('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";')
                    file.write('ADD FILTERIPV6: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+output.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(int(output.loc[i,'Subnet']))+';\n')
                    file.write('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
                elif(output.loc[i,"SVRENDPORT"] == "Remove"):
                    print('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";')
                    print('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+output.loc[i,'Filtername']+'";')
                    file.write('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
                    file.write('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
            rollback = output
            file.write('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n\n*****************\nROLLBACK SCRIPT: \n*****************\n\n')
            print('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n\n*****************\nROLLBACK SCRIPT: \n*****************\n')
            for i in range(rollback.shape[0]):
                if(rollback.loc[i,"SVRENDPORT"] == "Assigned"):
                    rollback.loc[i,['Ip Address', 'Subnet']] = rollback.loc[i,'Ip Prefix'].split('/')
                    print('MOD FILTERIPV6: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+rollback.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(rollback.loc[i,'Subnet'])+';')
                    file.write('MOD FILTERIPV6: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+rollback.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(rollback.loc[i,'Subnet'])+';\n') 
                elif(rollback.loc[i,"SVRENDPORT"] == "New"):
                    print('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                    print('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                    file.write('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')
                    file.write('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')                
                elif(rollback.loc[i,"SVRENDPORT"] == "Remove"):
                    print('ADD FILTERIPV6: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+rollback.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(rollback.loc[i,'Subnet'])+';')
                    print('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                    file.write('ADD FILTERIPV6: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPEV6=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIPV6="'+rollback.loc[i,'Ip Address']+'", SVRIPV6MASKTYPE=LENGTHTYPE, SVRIPV6MASKLEN='+str(rollback.loc[i,'Subnet'])+';\n')
                    file.write('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')
            file.write('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n')
            print('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n')

            cwd = os.getcwd()
            print("Result saved in \nDirectory: "+cwd+"\nFilename: outputipv6.txt")
        file.close()        
    else:
        with open("output.txt","w") as file:
            file.write('*****************\nSCRIPT: \n*****************\n\n')
            print('\n*****************\nSCRIPT: \n*****************\n')
            for i in range(output.shape[0]):
                # print(counter)
                if(output.loc[i,"SVRENDPORT"] == "Assigned"):
                    print('MOD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';')
                    file.write('MOD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';\n') 
                elif(output.loc[i,"SVRENDPORT"] == "New"):
                    print('ADD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';')
                    print('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";')
                    file.write('ADD FILTER: FILTERNAME="'+output.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+output.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(int(output.loc[i,'Subnet']))+';\n')
                    file.write('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
                elif(output.loc[i,"SVRENDPORT"] == "Remove"):
                    print('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";')
                    print('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+output.loc[i,'Filtername']+'";')
                    file.write('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+output.loc[i,'Filtername']+'";\n')
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
                    print('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                    print('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                    file.write('RMV FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')
                    file.write('RMV FILTER: OPMODE=SPECIFIC, FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')                
                elif(rollback.loc[i,"SVRENDPORT"] == "Remove"):
                    print('ADD FILTER: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+rollback.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(rollback.loc[i,'Subnet'])+';')
                    print('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";')
                    file.write('ADD FILTER: FILTERNAME="'+rollback.loc[i,'Filtername']+'", L34PROTTYPE=STRING, L34PROTOCOL=ANY, SVRIPMODE=IP, SVRIP="'+rollback.loc[i,'Ip Address']+'", SVRIPMASKTYPE=LENGTHTYPE, SVRIPMASKLEN='+str(rollback.loc[i,'Subnet'])+';\n')
                    file.write('ADD FLTBINDFLOWF: FLOWFILTERNAME="'+appdf.loc[userinput,'Filtergroup']+'", FILTERNAME="'+rollback.loc[i,'Filtername']+'";\n')
            file.write('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n')
            print('\nSET REFRESHSRV:REFRESHTYPE=ALL;\nSAV RUNNINGCONFIG:;\n')

            cwd = os.getcwd()
            print("Result saved in \nDirectory: "+cwd+"\nFilename: output.txt")
        file.close()

if __name__ == "__main__":
    main()
