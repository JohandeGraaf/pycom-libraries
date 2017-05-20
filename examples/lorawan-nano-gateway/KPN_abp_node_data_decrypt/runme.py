import get_loggly_data
print ('Make sure you\'ve changed all the needed settings in config.py')
dataset = get_loggly_data.get_loggly()
print ('If we got to this point without error you should have seen 1 or more decrypted messages on your screen.')
print ('That output has also been stored in a file "dataset.txt", it is in JSON format.')
