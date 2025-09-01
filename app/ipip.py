#!/usr/bin/python

'''
ipip.py -- netaddr functions used by cidrtools application


'''

# Network specific stuff
from netaddr import IPNetwork, IPAddress, cidr_merge
#from netaddr import *




def ip_summary(ip_list):

    results = []
    merged_list = []

    try:
        merged_list = cidr_merge(ip_list.split('\r\n'))
    except:
        results.append(dict(name='Well, something went wrong with the list of IPs', value="error on input"))
        return(results)
    else:
        count = 0
        for item in merged_list:
            results.append(dict(name=str(count), value=item))
            count = count + 1
        return(results)




def ip_subnet(basecidr, childcidr, netbox_text):

    results = []
    try:
        ip = IPNetwork(basecidr)
    except:
        return()
    else:
        if ip.prefixlen < childcidr:
            subnets = ip.subnet(childcidr)

            count = 0
            for item in subnets:
                results.append(dict(subid=str(count),
                                 network=item.network,
                                 netmask=item.netmask,
                                 first_ip=IPAddress(item.first+1),
                                 last_ip=IPAddress(item.last-1),
                                 netbox=str(item.cidr) + netbox_text))
                count = count + 1
            return(results)
        else:
            # results = dict(subid='The child prefix has to be longer than the parent prefix.')
            results.append(dict(subid='ERROR: The child prefix has to be longer than the parent prefix.',
                             network='',
                             netmask='',
                             first_ip='',
                             last_ip='',
                             nextbox='',
                             ))
            return(results)




def ip_supernet(cidr):
    results = []
    try:
        ip = IPNetwork(cidr)
    except:
        return()
    else:
        if ip.prefixlen > 8:
            supernets = ip.supernet(ip.prefixlen-8)
            count = 1
            for nets in supernets:
                results.append(dict(name='supernet_' + str(count), value=str(nets)))
                count = count + 1
            return(results)
        else:
            supernets = ip.supernet(1)
            count = 1
            for nets in supernets:
                results.append(dict(name='supernet_' + str(count), value=str(nets)))
                count = count + 1
            return(results)




def ip_disector(cidr):

    results = []
    
    try:
        ip = IPNetwork(cidr)
    except:
        results.append(dict(name='Well, something went wrong with the data entry', value="error on input"))
        return(results)
    else:
        results.append(dict(name='true cidr', value=ip.cidr))
        results.append(dict(name='netmask', value=str(ip.netmask)))
        results.append(dict(name='inverse mask', value=str(ip.hostmask)))
        results.append(dict(name='size', value=str(ip.size)))
        results.append(dict(name='network', value=str(IPAddress(ip.first))))
        results.append(dict(name='broadcast', value=str(IPAddress(ip.last))))
        results.append(dict(name='first host', value=str(IPAddress(ip.first+1))))
        results.append(dict(name='last host (or typically the gateway)', value=str(IPAddress(ip.last-1))))
        #print(items)

        return(results)



