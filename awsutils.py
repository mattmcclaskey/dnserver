import boto3
import re

sessions = {}

def get_instance_ip(name):
    p_hostname = re.compile("^([a-zA-Z0-9]+|[a-zA-Z0-9]+[-a-zA-Z0-9]*[a-zA-Z0-9]+)(\.|$)") #hostname, not fqdn
    p_fqdn = re.compile("^([a-zA-Z0-9]+|[a-zA-Z0-9]+[-a-zA-Z0-9]*[a-zA-Z0-9]+)\.([a-zA-Z0-9]+|[a-zA-Z0-9]+[-a-zA-Z0-9]*[a-zA-Z0-9]+)(\.|$)")
    ip = None
    region = None
    session = None

    # extract the hostname from the request and return none if it is invalid
    m_hostname = p_hostname.search(name)
    m_region = p_fqdn.search(name)
    if m_hostname is None:
        print('invaid hostname')
        return
    name = m_hostname.group(1)
    print('hostname', name)

    # extract the zone from the request, default to boto config default if not provided
    if m_region and m_region.group(2) != 'ec2':
        region = m_region.group(2)
    else:
        region = 'us-east-1'

    if region not in sessions:
        sessions['region'] = boto3.Session(region_name=region)
    session = sessions['region']
    print('region: ', region)

    session = sessions['region']
    ec2 = session.resource('ec2')
    for instance in ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [ name ] }]):
        if 'PrivateIpAddress' in instance.meta.data:
            ip = instance.meta.data['PrivateIpAddress']
            return ip

    print('no aws record found')
    return ip
