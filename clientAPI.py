from datetime import datetime
from flask import Flask,request

#app flask name
app = Flask(__name__)

print('**************Start of decryption *******************')

# function to authinticate the userCode 
def authinticateUserCode(clientOTP,UserCode):


    #check if the usercode length = 1
    if len(UserCode) == 1:
        UserCode= '0'+UserCode

    clientList=[]

    clientCounter = 1

#loop to divide the usercode into list contains user code listed for every 2 digits 
    for i in UserCode:
        if clientCounter//2:
            clientList.append(UserCode[clientCounter-2:clientCounter])
        clientCounter+=1
    print('usercode is here listed',clientList)


    # sum up them the list 
    codeStore = 0
    for x in range(len(clientList)):
        codeStore += int(clientList[x])
    
    # separate the usercode part from the otp    
    systemAdmin = clientOTP[-3:]

    #convert the summation of usercode list (recieved from the client) to hex  
    user = hex(codeStore)

    # compare the hex result from hex(sum(usercode Listed)) that is recieved from the client 
    # with hex(sum(usercode Listed)) from the otp 
    # if TRue continue to authinticateTimeStamp if false raise an error 
    if int(user,16) == int(systemAdmin,16):
        
        print('success of Usercode')

        #testCase variable store boolen value result from authinticateTimeStamp function 
        # if the difference from current timestamp and the admin's timestamp is 300 or greater
        # which represents 5 minutes return false else retrun true
        testCase=authinticateTimeStamp(clientOTP[:5],systemAdmin)
        if testCase ==True:
            return 'True'
        if testCase == False:
            return 'False'    

    else:
        print('Failed to authinticate userCode')
        return 'False'  
 
# function to authinticate the timestamp 
def authinticateTimeStamp(clientOTP,system_Admin_Timestamp):
        
        res = int(clientOTP,16)
        print('digits represents timestamp in decimal: ',res)
        res = str(res)
        #shift the digits represents timestamp in decimal to get the original ex: 
        # if res => 527896 then,
        # the below line convert res variable to 278965
        res = res[1:]+res[0]

        # add 2 zeros to timestamp in decimal at the last  
        res = res+'00'
        res = int(res)
        print('plus 2 zeros:  ',res)

        # add the result to 1609452000 which represents the timestamp of 1/1/2021
        system_Admin_Timestamp = res + 1609452000 

        print('System admin time:  ',system_Admin_Timestamp)

        # get the current timestamp of the client
        now = datetime.now()
        result = int(datetime.timestamp(now))
        print('current Time:  ',result)

        print('original_timestamp from admin:  ',system_Admin_Timestamp)

        #get the difference of client timestamp and admin timestamp 
        # if the difference from current timestamp and the admin's timestamp is 300 or greater
        # which represents 5 minutes return false else retrun true
        diff = result - system_Admin_Timestamp

        if diff == 300 or diff > 300: 
            return False
        if diff < 300:
            return True   

#function to deshufle the otp and extract the original otp which it's first 5 digits 
# represents hex(timestamp) before shift to get the original difference from admin timestamp and 1/1/2021 timestamp
#  and the last 3 represents the hex(user code) 
def Decryption(clientOTP):
        
        
    #first deshuffle 
    clientOTP = clientOTP[1]+clientOTP[0]+clientOTP[3]+clientOTP[2]+clientOTP[5]+clientOTP[4]+clientOTP[7]+clientOTP[6]

    #second deshuffle
    clientOTP = clientOTP[1]+clientOTP[2]+clientOTP[4]+clientOTP[6]+clientOTP[3]+clientOTP[5]+clientOTP[0]+clientOTP[7]
    clientOTP = clientOTP[1]+clientOTP[2]+clientOTP[4]+clientOTP[6]+clientOTP[3]+clientOTP[5]+clientOTP[0]+clientOTP[7]

    # take the first 3 numbers of deshuffled otp
    ptTime= clientOTP[0:3]

    # take the mid 2 numbers of deshuffled otp
    mid = clientOTP[3:5]

    # take the last 3 numbers of deshuffled otp which represents the usercode
    ptUser = clientOTP[-3:]


    #sub the first 3 digits of OTP with last 3 digits which will always represent the usercode
    r =  hex(int(ptTime,16) - int(ptUser,16))

    #return the original otp 
    orotp = r[2:]+mid+ptUser
    return orotp

# home route
@app.route('/', methods=['GET'])
def home():

    return "Enter userCode and OTp in the URL please"



# route that admin will send in it user_id and otp
@app.route('/client', methods=['GET'])
def success():

        UserCode = request.args.get('id')
        clientOTP = request.args.get('otp')

        #variable which will hold True or false as string 
        # because boolean can't be returned from a route so we can handle when we connect it to the desktop app
        thirdCase =authinticateUserCode(Decryption(clientOTP),UserCode)

        return thirdCase



# Run the application
if __name__ == '__main__':
    app.debug = True
    app.run()
