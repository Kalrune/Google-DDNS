# Dynamic DNS Python script
# Author: Chris Stokes-Pham
# v1.0 7/28/15

# The legal stuff:
# The MIT License (MIT)

# Copyright (c) [2015] [Christopher Andrew Stokes-Pham]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# libraries we need
import urllib.request
import urllib.parse
import http.client
import base64
import socket

#------------------------------
# all the user specific var
# define google username & password for DDNS service
myUname = 'Google Dynamic DNS generated username here'
myPasswd = 'Google Dynamic DNS generated password here'

# define your subdomain to update
myDomain = 'yourSubDomain.YourDomain.YourTLD'

#------------------------------
# Determine our current external IPs
# use https://domains.google.com/checkip http server to obtain public IP, Google will return IPv6 so
# other good server is http://ip.42.pl/raw which returns IPv4
url4 = 'http://ip.42.pl/raw'
req4 = urllib.request.Request(url4)
resp4 = urllib.request.urlopen(req4)
respData4 = resp4.read()
extIP4 = respData4.decode('utf-8')

url6 = 'https://domains.google.com/checkip'
req6 = urllib.request.Request(url6)
resp6 = urllib.request.urlopen(req6)
respData6 = resp6.read()
extIP6 = respData6.decode('utf-8')

#print IPs to console for troubleshooting
print (extIP4)
print (extIP6)

#------------------------------

# Check current subdomain IP, if matches don't overwork Google's DNS server
currentIP = socket.gethostbyname(myDomain)

if currentIP != extIP4:
    # connect to Google DDNS to update IP
    # Google example syntax per https://support.google.com/domains/answer/6147083
    # https://username:password@domains.google.com/nic/update?hostname=subdomain.yourdomain.com&myip=1.2.3.4

    # base64 encode username & password
    myUsrPass = myUname + ":" + myPasswd
    myUsrPass = base64.b64encode(bytes(myUsrPass, 'utf-8')).decode("ascii")
    print (myUsrPass)

    # encode data & user agent
    # Google DDNS only supports IPv4 for now so we will us it
    myData = urllib.parse.urlencode({'hostname' : myDomain, 'myip' : extIP4 }).encode("UTF-8")
    upUrl= '/nic/update?'
    upHost = 'domains.google.com'

    # URL query example & Headers
    # POST /nic/update?hostname=subdomain.yourdomain.com&myip=1.2.3.4 HTTP/1.1
    # Host: domains.google.com
    # Authorization: Basic base64-encoded-auth-string User-Agent: Chrome/41.0 your_email@yourdomain.com

    headers = {
        'Content-Type'  : "application/x-www-form-urlencoded",
        'User-Agent'    : 'Chrome/41.0',
        'Authorization' : 'Basic %s' % myUsrPass
        }

    # connect & update (need to include some catch for errors later)
    conn = http.client.HTTPSConnection(upHost)
    conn.request("POST", upUrl, myData, headers)
    upResp = conn.getresponse()
    print(upResp.status, upResp.reason)
    print(upResp.read().decode('utf-8'))

else:
    print("Current DNS shows your IP " + extIP4 + " no need to bother Google DNS")
