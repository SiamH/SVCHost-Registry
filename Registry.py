import cygwinreg as reg

ServicePath = []
SVCHost = []
SVCDllPath = []
SVCHostServices = []

def IsAutoStartExe(SubKey):
    j = 0
    reSet = []
    sImage = ""
    bRet = False

    while j < 3:
        reSet = reg.EnumValue(SubKey, j)
        print reSet

        k = 0
        while k <  len(reSet):
            if reSet[k] == "ImagePath" or reSet[k] == "DisplayName":
                sImage = reSet [k + 1]
            if reSet[k] == "Start":
                if reSet[k + 1] == 2: # ServiceManager must run the program
                    bRet = True
            k += 1

        j += 1

    if bRet == True:
        return sImage

    return ""

def GetSVCHostKey (SubKey):
    j = 0
    reSet = []
    sImageStored = ""
    bRet = False
    sDLLPath = ""

    while j < 3:
        reSet = reg.EnumValue(SubKey, j)

        k = 0
        while k <  len(reSet):
            if reSet[k] == "ImagePath":
                sImage = reSet [k + 1]
                if sImage.find("svchost.exe") != -1:
                    if sImage.find('-k') == -1 or sImage.find('system32') == -1:
                        bRet = True
                    else:
                        sService = sImage.split(' -k ')[1]
                        if sService not in SVCHostServices:
                            bRet = True
            if reSet[k] == "DisplayName" or reSet[k] == "Description":
                sDLLPath = reSet[k + 1]

            k += 1

        j += 1

    if bRet == True:
        return True, sImage, sDLLPath

    return False, "", ""


def GetAllSVCHostServices():
    SVCHostKeyPath = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Svchost"
    SVCHostKey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, SVCHostKeyPath)
    j = 0
    while j < int(reg.QueryInfoKey(SVCHostKey)[0]):
        SVCHostServices.append(reg.EnumKey(SVCHostKey, j))
        j += 1


# Checking the auto run services
StartPath = "System\\CurrentControlSet\\Services"
ServiceKey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, StartPath)

i = 0

GetAllSVCHostServices()

target = open("RegDLLAndPath.txt", 'w')

try:
    while i < int(reg.QueryInfoKey(ServiceKey)[0]):
        name = reg.EnumKey(ServiceKey, i)
        SubKeyPath = StartPath + "\\" + name
        SubKey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, SubKeyPath)
        if len(reg.QueryInfoKey(SubKey)) == 3 and reg.QueryInfoKey(SubKey)[1] > 0:
            sRet = IsAutoStartExe(SubKey)
            if sRet != "":
                ServicePath.append(sRet)

            bRet, sImagePath, sDll =  GetSVCHostKey(SubKey)
            if bRet:
                SVCHost.append(sImagePath)
                SVCDllPath.append(sDll)
        i += 1

except OSError:
    target.write("Auto Start Registry Check:\n")
    for path in ServicePath:
        target.write(path)
        target.write('\n')
    target.write("SVCHost Image Path:\n")
    for path in SVCHost:
        target.write(path)
        target.write('\n')
    target.write("SVCHost Image Dll:\n")
    for path in ServicePath:
        target.write(path)
        target.write('\n')

target.close()



#SVCHostKeyPath = "\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Svchost"
#SVCHostKey = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, SVCHostKeyPath)
