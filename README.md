# dnserver

Simple DNS server to provide AWS name resolution based on instance name. It is a fork of the original https://github.com/samuelcolvin/dnserver, which is a standard DNS server sans the AWS. This service is intended to be behind a robust caching DNS server such as bind or unbound, with stub zones configured. The caching DNS server should be configured to forward all requests to the AWS internal DNS service with the excpeption of the following zones which should be forwarded to this python service.

us-east-1.<custom>
us-east-2.<custom>
...

There should be a zone for each AWS region. The domain name should be <region-name>.<custom>. The ending custom part is optional and you can choose to mirror the aws internal domain name or use your own. For example...

us-east-1.compute.internal

The default region is us-east-1. If a request comes in with only the hostname, us-east-1 will be used. You must install and configure boto3.