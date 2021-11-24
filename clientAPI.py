from datetime import datetime
from flask import Flask,request

app = Flask(__name__)

print('**************Start of decryption *******************')


def authinticateUserCode(clientOTP,UserCode):
    
    if len(UserCode) == 1:
        UserCode= '0'+UserCode

    clientList=[]

    clientCounter = 1

    for i in UserCode:
        
        if clientCounter//2:
            clientList.append(UserCode[clientCounter-2:clientCounter])
        clientCounter+=1
    print('usercode is here listed',clientList)

    codeStore = 0
    for x in range(len(clientList)):

        codeStore += int(clientList[x])
    systemAdmin = clientOTP[-3:]
    user = hex(codeStore)

    if int(user,16) == int(systemAdmin,16):
        print('success of Usercode')
        
        res = int(clientOTP[:5],16)

        print('digits represents timestamp in decimal: ',res)
        res = str(res)
        res = res[1:]+res[0]
        res = res+'00'
        res = int(res)
        print('plus 2 zeros:  ',res)
        system_Admin_Timestamp = res + 1609452000 

        print('System admin time:  ',system_Admin_Timestamp)
        now = datetime.now()
        result = int(datetime.timestamp(now))

        print('current Time:  ',result)

        print('original_timestamp:  ',system_Admin_Timestamp)

        diff = result - system_Admin_Timestamp

        if diff == 300 or diff > 300: 
            return 'False'
        if diff < 300:
            return 'True'   
    else:
        print('Failed to authinticate userCode')

        return 'False'  
 
def Decryption(clientOTP):
        
        
    #first deshuffle 
    clientOTP = clientOTP[1]+clientOTP[0]+clientOTP[3]+clientOTP[2]+clientOTP[5]+clientOTP[4]+clientOTP[7]+clientOTP[6]

    #second deshuffle
    clientOTP = clientOTP[1]+clientOTP[2]+clientOTP[4]+clientOTP[6]+clientOTP[3]+clientOTP[5]+clientOTP[0]+clientOTP[7]
    clientOTP = clientOTP[1]+clientOTP[2]+clientOTP[4]+clientOTP[6]+clientOTP[3]+clientOTP[5]+clientOTP[0]+clientOTP[7]


    ptTime= clientOTP[0:3]
    mid = clientOTP[3:5]
    ptUser = clientOTP[-3:]


    #sub the first 3 digits of OTP with last 3 digits which will always represent the usercode
    r =  hex(int(ptTime,16) - int(ptUser,16))

    orotp = r[2:]+mid+ptUser

    return orotp

@app.route('/', methods=['GET'])
def home():

    return "Enter userCode and OTp in the URL please"






# route that admin will send in it user_id 
@app.route('/client', methods=['GET'])
def success():

        UserCode = request.args.get('id')
        clientOTP = request.args.get('otp')
        thirdCase =authinticateUserCode(Decryption(clientOTP),UserCode)


        print(UserCode,'  ',clientOTP)

        return thirdCase



# Run the application
if __name__ == '__main__':
    app.debug = True
    app.run()
