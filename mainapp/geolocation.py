import urllib2, json

apikey = 'ce2c79057b1cc11dc76bf76102911316147723edc4ed58717ec9c398fe048046'
def get_addr_from_ip(ip):
    baseurl = 'http://api.ipinfodb.com/v3/ip-city/?key=' + str(apikey) + '&ip=' + ip_addr
    response = urllib2.urlopen(baseurl)
    data = response.read()
    response.close()
    return_data = {}
    data_list = data.split(';')
    # print data_list
    return_data['latitude'] = data_list[len(data_list)-3]
    return_data['longitude'] = data_list[len(data_list)-2]
    index = data_list.index(ip)
    addr_list = data_list[index+2: len(data_list)-4]
    return_data['address'] = ','.join(addr_list)
    return return_data

# ip_addr = '110.44.117.62'
# print get_addr_from_ip(ip_addr)