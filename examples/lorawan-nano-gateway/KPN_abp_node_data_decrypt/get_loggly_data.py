from base64 import b64encode
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import time
import loramac_decrypt
import config

def get_loggly():

    user = config.LOGGLY_USER
    password = config.LOGGLY_PASSWORD
    key = config.APPSKEY
    dev_addr = config.DEVADDRESS
    dev_eui = config.DEVEUI
    
    dataset = get_loggly_data(user, password, dev_eui, dev_addr, key)
    # print(dataset)
    # log response to file for debugging purposes
    file = open("dataset.txt","w")
    file.write(json.dumps(dataset))
    file.close()
    return dataset


def get_loggly_data(user, password, dev_eui, dev_addr, key, since = '-1d'):

    # retrieving the data from loggly is a 2-step process
    # first we need to send a search query that gets scheduled on the server
    # then we need to retrieve the results using the rsid that we get from the
    # first call.
    # if we do this all too quick or too often we get a 403 back so we have to try
    # until there is an result
    # see: https://www.loggly.com/docs/api-retrieving-data/
    
    # user = str(user)
    # password = str(password)
    # dev_eui = str(dev_eui)
    # dev_addr = str(dev_addr)
    # key = str(key)
    # since = str(since)
   
    url1 = 'http://'+user+'.loggly.com/apiv2/search'
    url2 = 'http://'+user+'.loggly.com/apiv2/events'
       
    # schedule query and get rsid 
    data = {}
    data['q'] = dev_eui
    data['from'] = since
    data['until'] = 'now'
    data['size'] = 1 # it looks like loggly API ignores this ?
    url_values = urlencode(data).encode('ascii')                                
    headers = {'Authorization': b'Basic ' + b64encode((user + ':' + password).encode('utf-8'))}
    print('Scheduling query...')    
    attempts = 0
    while attempts < 10:
        try:        
            response = urlopen(Request(url1, url_values, headers))
            break
        except:
            attempts += 1
            print('Schedule request failed. Waiting 10 seconds for retry...')
            time.sleep(10) # delays for 10 seconds         
    if attempts == 10:
        print('Oops, did not get rsid in time!')
        return 'failed to get rsid'
        
    js = response.read().decode()
    jsonresponse = json.loads(js)
    rsid = jsonresponse["rsid"]["id"]

    print('rsid= '+ str(rsid))
    print('Waiting for 10 seconds before getting result...')
    time.sleep(10) # delays for 10 seconds

    # try to get result
    data = {}
    data['rsid'] = str(rsid)
    url_values = urlencode(data).encode('ascii')
    headers = {'Authorization': b'Basic ' +  b64encode((user + ':' + password).encode('utf-8'))}
        
    attempts = 0
    while attempts < 10:
        try:        
            response = urlopen(Request(url2, url_values, headers))
            break
        except:
            attempts += 1
            print('Open failed on attempt '+str(attempts)+'. Waiting for 10 more seconds...')
            time.sleep(10) # delays for 10 seconds 

    if attempts == 10:
        print('Oops, did not get result in time!')
        return 'failed to get query result'
            
    js = response.read().decode()
    jsonresponse = json.loads(js)
    # log response to file for debugging purposes
    # file = open("responselog.txt","w")
    # file.write(js)
    # file.close() 


    num_results = int(jsonresponse["total_events"])
    datasample = {}
    for x in range(0, num_results-1):
        datatuple = {}
        DevEUI_uplink = jsonresponse["events"][x]["event"]["json"]["DevEUI_uplink"]
        datatuple['payload_hex'] = DevEUI_uplink["payload_hex"]
        datatuple['FCntUp'] = DevEUI_uplink["FCntUp"]
        datatuple['Time'] = DevEUI_uplink["Time"]
        datatuple['LrrLON'] = DevEUI_uplink["LrrLON"]
        datatuple['LrrLAT'] = DevEUI_uplink["LrrLAT"]
        datatuple['Lrrid'] = DevEUI_uplink["Lrrid"]
        datatuple['LrrRSSI'] = DevEUI_uplink["LrrRSSI"]
        datatuple['LrrSNR'] = DevEUI_uplink["LrrSNR"]
        datatuple['SpFact'] = DevEUI_uplink["SpFact"]   
        datatuple['DevEUI'] = DevEUI_uplink["DevEUI"]  
         
        print('payload_hex = ' + datatuple['payload_hex'])
        print('FCntUp = ' + datatuple['FCntUp'])
        decrypted = loramac_decrypt.loramac_decrypt(datatuple['payload_hex'], int(datatuple['FCntUp']), key, dev_addr)

        print('Decrypted message:', decrypted )  
        decoded = ''
        current = 0
        while current < len(decrypted):
            try:
                character = chr(int(decrypted[current]))
            except:
                character = ''
            decoded += character
            current += 1
        decoded = decoded.encode('utf-8')    
        print('Decoded message: ', decoded)
            
        datatuple['payload_decrypted'] = str(decrypted)
        datatuple['payload_decoded'] = str(decoded)       
        datasample[x] = datatuple
        
    return datasample