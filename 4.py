#Converts binary to decimal
def decConv(binary):
    mult = 128
    decimal = 0
    for num in binary:
        if num == "1":
            decimal += mult         
        mult /=2
    return str(int(decimal))   

#Converts decimal to binary
def binConv(decimal):
    binList = []
    binary = ""

    while True:
        mod = decimal % 2
        binList.insert(0, mod)
        decimal = int(decimal / 2)
        
        if decimal == 0:
            while len(binList) != 8:
                binList.insert(0, "0")
            break
        continue
          
    for num in binList:
        binary += str(num)
        
    return binary
      
#Checks whether IP input is valid
def ipCheck(baseIP):
    counter = 0
    digit = ""
    octet = []
    
    digitBool = False
    dotBool = False
    rangeBool = False
    octetBool = False
    
    #Checks whether IP has 3 dots
    if baseIP.count(".") == 3:
        dotBool = True
        octet = baseIP.split(".")
    
    #If IP has 3 dots
    if dotBool:
        
        #Saves all octet contents in 'digit' variable
        for num in range(len(octet)):
            digit += octet[num]
            
        #Checks whether IP is all digits
        if digit.isdigit():
            digitBool = True
            
    #Checks if octets are all non-empty
    for num in range(len(octet)):
        if octet[num] != "":
            octetBool = True
        else:
            octetBool = False
            break
    
    #Checks IP range validity
    if digitBool & octetBool:
        while True:           
            while counter != len(octet):
                #Checks whether IP is within (0 - 223) range (except 0 & 127 for first octet)
                if (0 <= int(octet[counter]) <= 223) & (0 != int(octet[0]) != 127):
                    counter += 1 
                    rangeBool = True
                    continue
                else:
                    break                       
            break

    #If all checks are passed
    if dotBool & digitBool & rangeBool & octetBool: 
        return True

#Checks whether CIDR input is valid
def cidrCheck(cidr):
    if 13 <= cidr <= 31:
        return True
     
#Converts CIDR to Binary Subnet Mask
def binCidr(cidr):
    temp = ""
    tempList = []
    dots = 0
    counter = 0
    
    #Fills in 1's
    for num in range(cidr):
        temp += "1"
    
    #Fills in 0's      
    for num in range(32 - cidr):
        temp += "0"
        
    #Add dots per 8th number
    for num in temp:
        if counter != 8:
            tempList.append(num)
            counter += 1
        else:     
            if dots != 3:  
                tempList.append(".")
                tempList.append(num)
                dots += 1 
                counter = 1
            else:
                tempList.append(num)
                counter = 1     
    
    #Transfer to string variable
    temp = ""
    for num in range(len(tempList)):
        temp += str(tempList[num])
            
    return temp

#Converts Binary Subnet Mask to Decimal Subnet Mask        
def decCidr(binSM):
    tempList = binSM.split(".")
    subnetMask = ""
     
    for num in range(len(tempList)):
        subnetMask += str(decConv(tempList[num]))
        
        if num != (len(tempList) - 1):
            subnetMask += "."     
        
    return subnetMask

#Calculates number of hosts per network
def numHost(cidr):
    hosts = 2 ** (32 - cidr) 
    return hosts
 
#Calculates number of networks
def numNet(cidr, hosts):
    bin = binCidr(cidr)
    exp = 0
    
    binList = bin.split(".")
    binList.reverse()
    
    for num in range(len(binList)):
        for num2 in str(binList[num]):
            if num2.__contains__("0"):
                exp += 1
                break
    
    networkNum = (256 ** exp) / hosts
    
    return int(networkNum)

#Converts IP to Binary
def binIP(baseIP):
    ipList = baseIP.split(".")
    bin = ""
    dots = 0
    
    for num in ipList:
        bin += str(binConv(int(num)))
    
        if dots != 3:
            bin += "."
            dots += 1
        
    return bin
        
#Determines Network ID
def id(binIP, binSM, mode, hosts):
    ipList = binIP.split(".")
    smList = binSM.split(".")
    
    ip = ""
    sm = ""
    nid = ""
    bid = ""
    
    dots = 0
    digits = 0
    
    for num in range(len(ipList)):
        ip += ipList[num]
        sm += smList[num]

    for num in range(len(sm)):
        if sm[num] == "1":
            nid += ip[num]
            bid += ip[num]
            digits += 1
        else:
            nid += "0"
            bid += "1"
            digits += 1
   
        if (dots != 3) & (digits == 8):
            nid += "."
            bid += "."
            dots += 1
            digits = 0
    
    if mode == 1:
        octet = nid.split(".")
    else:
        octet = bid.split(".")
        
    nid = ""
    bid = ""
    dots = 0
    
    #NID Correction based on CIDR
    if mode == 1:
        if hosts <= 256:
            octet[3] = "0"
        elif 256 <= hosts <= 65536:
            octet[2] = "0"
            octet[3] = "0"
        else:
            octet[3] = "0"
            octet[2] = "0"
            octet[1] = "0"
  


    for num in octet:
        nid += str(decConv(num))
        bid += str(decConv(num))
        if dots != 3:
            nid += "."
            bid += "."
            dots += 1
    
    if mode == 1:
        return nid
    else:
        return bid
    
#Displays IP Range
def ipRange(nid, networks, hosts):
    bid = ""
    dots = 0
    counter = 0
    tempNum = 0
    
    print("\nHosts: " , hosts - (networks * 2))
    print("Networks: " , networks)
    
    print("\n--------------------------------------------------------------------------------------------")
    print("\t NETWORK ID     |\t\t    IP RANGE                    |     BROADCAST ID    ")
    print("--------------------------------------------------------------------------------------------")
               
    while networks != 0:
        ipStart = ""
        ipEnd = ""
            
        #Isolate ip octets
        ipList = nid.split(".")
            
        #Start of ip range
        ipList[3] = str(int(ipList[3]) + 1)
            
        for num in range(len(ipList)):
            if dots != 3:
                ipStart += ipList[num]
                ipStart += "."
                dots += 1
            else:
                ipStart += ipList[num]
                    
        #Reset dot counter        
        dots = 0
                              
        #Calculate ip range (End)
        tempNum = hosts - 2
         
        #Fourth Octet exceed 255
        if tempNum <= 254:
            ipList[3] = str(int(ipList[3]) + hosts - 3)
            
        else:
            while tempNum > 255:
                if (int(ipList[3]) + tempNum) > 254:
                        
                    #Third Octet exceed 255
                    if (int(ipList[2]) + 1) > 255:
                        tempNum -= 256
                        ipList[1] = str(int(ipList[1]) + 1)         
                        ipList[2] = "0"

                    else:
                        tempNum -= 256
                        ipList[2] = str(int(ipList[2]) + 1)
                        ipList[3] = "0"
                        ipList[3] = str(int(ipList[3]) + 254)
                    
                else:
                    ipList[3] = str(int(ipList[3]) + 253)
                
        
        #Construct ip range (End)           
        for num in range(len(ipList)):
            if dots != 3:
                ipEnd += ipList[num]
                ipEnd += "."
                dots += 1
            else:
                ipEnd += ipList[num]
                
        #Reset dot counter        
        dots = 0   
                
        #Broadcast ID
        ipList[3] = str(int(ipList[3]) + 1)
        for num in range(len(ipList)):
            if dots != 3:
                bid += ipList[num]
                bid += "."
                dots += 1
            else:
                bid += ipList[num]
                   
        #Print content
        networks -= 1
        counter += 1
         
        print("#" + str(counter) + "\t" + nid + "\t| " + ipStart + "\t\t-\t" + ipEnd + "\t| " + bid + "\n")

        
        #Preparation for next iteration
        ipList = bid.split(".")
        
        #Reset variables
        dots = 0
        nid = ""
        bid = ""

             
        #Update Network ID (Modify)
        if (int(ipList[3]) + 1) > 255:
            if (int(ipList[2]) + 1) > 255:
                ipList[1] = str(int(ipList[1]) + 1)      
                ipList[2] = "0"
                ipList[3] = "0"

            else:
                ipList[2] = str(int(ipList[2]) + 1)
                ipList[3] = "0"
                
        else:
            ipList[3] = str(int(ipList[3]) + 1)
        
        
        #Construct next Network ID
        for num in range(len(ipList)):
            if dots != 3:
                nid += ipList[num]
                nid += "."
                dots += 1
            else:
                nid += ipList[num]
        
        #Reset dot counter
        dots = 0
            
#Main code
def ipMain():

    #Network IP
    while True:
        print("____________________________")
        baseIP = input("Enter network IP: ")
            
        if ipCheck(baseIP) == True:            
            print("\n[IP Accepted]")
            break
        else:
            print("\n[INVALID IP]")
            continue
        
    #CIDR (Slash Number)
    while True:
        try:
            print("____________________________")
            cidr = int(input("Enter CIDR: "))
            
            if cidrCheck(cidr) == True:
                print("\n[CIDR Accepted]")
                print("____________________________")
                break
            else:
                print("\n[Invalid CIDR. Please try again]")
                continue
        except ValueError:
            print("\n[Invalid CIDR. Please try again]")
            continue
          
    #Finalize values
    binSM = binCidr(cidr)
    hostNum = numHost(cidr)
    networks = numNet(cidr, hostNum)
    ip = binIP(baseIP)
    nid = id(ip, binSM, 1, hostNum)
    
    print("\n* * * * * * * * * * * * * * * *")
    print("\nNetwork: " , baseIP , "/" , cidr)
    print("\n* * * * * * * * * * * * * * * *")
    
    while True:
        print("____________________________")
        proc = input("Proceed? [Y/N]: ") 
        
        match proc.lower():
            
            case "y":
                ipRange(nid, networks, hostNum)
                break
            case "n":
                print("____________________________")
                print("[GOODBYE!]")
                print("____________________________")
                exit()
            case _:
                print("[INVALID INPUT]")
                continue

ipMain()