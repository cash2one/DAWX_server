from subprores import subprores

def check():
    pass

def rundns(unbindip,bindip,namestart,nameend,numeval):
    if unbindip:
        command = "sh app/shelltools/dnsbind.sh" + " " + "unbind" +" "+ str(unbindip) + " " + str(namestart) + " " + str(nameend) + " " + str(numeval)
        print command
        subp = subprores(command)
        if not subp:
            return [False,"sh: CreateNewZone.sh, ERROR occurred!!!"]
    if bindip:
        command = "sh app/shelltools/dnsbind.sh" + " " + "bind" +" " +  str(bindip)  + " " + str(namestart) + " " + str(nameend) + " " + str(numeval)
        print command
        subp = subprores(command)
        if not subp:
            return [False,"sh: CreateNewZone.sh, ERROR occurred!!!"]

    return [True, "unbind or bind ip OK"]

def bind(bindip,namestart,nameend,numeval):
    pass

def unbind():
    pass
