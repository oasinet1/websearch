# class SearchResult{
#    String[] words; # strings matched for this url
#    String url;   # url matching search query 
#    long frequency; #number of hits for page
# }

# interface PeerSearch {
#     void init(DatagramSocket udp_socket); # initialise with a udp socket
#     long joinNetwork(IPAddress bootstrap_node); #returns network_id, a locally 
#                                        # generated number to identify peer network
#     boolean leaveNetwork(long network_id); # parameter is previously returned peer network identifier
#     void indexPage(String url, String[] unique_words);
#     SearchResults[] search(String[] words)
# }
from time 
import sys
import socket
import json
import random
from numpy import int32
from pif import get_public_ip

#"--bootstrap [IP Address] --id [Integer Identifier 232]".

# parser = argparse.ArgumentParser(description='Process bootstrap')
# parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max,help='sum the integers (default: find the max)')
# args = parser.parse_args()
# print(args.accumulate(args.integers))
UDP_PORT = 8767
class node(object):

    def  __init__(self,word,IP):
        self.ID = self.hashCode(word)
        URLSave = dict()
        self.IP = IP

    def hashCode(self,str):
        hash = int32(0)
        for c in str: 
            hash = hash * 31 + ord(c)      
        return abs(hash)

    def indexPage(URL,indexWord):
        foreignhash = hashCode(indexWord)
        if(foreignhash == self.ID):
            self.URLSave[URL] = 1
            return -1
        else:
            return findNearestMatch(self.ID,foreignhash)
            
    
class message(object):
    def __init__(self,UDP_PORT):
        pass
        
    def joinNetwork(self,ipAddr, src,dest):    
        #message to send
        msg = { "type": "JOINING_NETWORK", "node_id": src, "target_id": dest, "ip_address": "127.0.0.1" } 
        jsmsg = json.dumps(msg)
        self.send(jsmsg, ipAddr)
        #need to resolve bootstrap IP with command line arguments
        sock.sendto(jsmsg, (ipAddr, UDP_PORT))
    def joinNetworkRelay(self,src,dest,myNode,rTable):
        msg = { "type": "JOINING_NETWORK_RELAY",  "node_id": src.ID, "target_id": dest.ID,"gateway_id": myNode.ID}
        jsmsg = json.dumps(msg)        
        self.send(jsmsg, rTable[dest])

    def leaveNetwork(self,node,routingTable):
        msg = {"type": "LEAVING_NETWORK", "node_id": node.ID}
        jsmsg = json.dumps(msg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for ip in routingTable.itervalues():    
            self.send(jsmsg,ip)

    def routingInfo(self, Target, Gateway, rTable,myNode):
        rt = []
        for entry in rTable:
            rt.append({"node_id": entry, "ip_address": rTable[entry]})

        msg = {
        "type": "ROUTING_INFO", # a string
        "gateway_id": Gateway, # a non-negative number of order 2'^32^', of the gateway node
        "node_id": Target, # a non-negative number of order 2'^32^', indicating the target node (and also the id of the joining node).
        "ip_address": myNode.IP, # the ip address of the node sending the routing information
        "route_table": rt
        }
        jsmsg = json.dumps(msg)
        self.send(jsmsg,Target)

    def index(self,word, URLs,TargetIP,ID,rTable,myNode):
        msg = {
        "type": "INDEX", #string
        "target_id": myNode.hashCode(word), #the target id
        "sender_id": myNode.ID, # a non-negative number of order 2'^32^', of the message originator
        "keyword": word, #the word being indexed
        "link": [
               URLs
              ]
        }
        jsmsg = json.dumps(msg)
        self.send(jsmsg,TargetIP)
    def search(self,word,myNode,rTable):
        msg = {
        "type": "SEARCH", # string
        "word": word, # The word to search for
        "node_id": myNode.hashCode(word),  # target node id
        "sender_id": myNode.ID, # a non-negative number of order 2'^32^', of this message originator
        }
        jsmsg = js.dumps(msg)
        self.send(jsmsg,rTable[rTable.findNearestMatch(myNode.hashcode(word))])
        
    def ping(self,target_id,target_ip,myNode,rTable):
        msg = {
        "type": "PING", # a string
        "target_id": target_id, # a non-negative number of order 2'^32^', identifying the suspected dead node.
        "sender_id": myNode.ID, # a non-negative number of order 2'^32^', identifying the originator                            #    of the ping (does not change)
        "ip_address": myNode.IP # the ip address of  node sending the message (changes each hop)
        }
        jsmsg = json.dumps(msg)
        self.send(jsmsg,rTable[rTable.findNearestMatch(myNode.ID,target_ip)])
    def ack(self, myNode,target_ip):
        msg = {
        "type": "ACK", # a string
        "node_id": myNode.ID, # a non-negative number of order 2'^32^', identifying the suspected dead node.
        "ip_address": myNode.IP # the ip address of  sending node, this changes on each hop (or used to hold the keyword in an ACK message returned following an INDEX message - see note below)
        }
        self.send(msg,target_ip)
    def ackIndex(self, target_id,target_ip,keyword):
        msg = {
        "type": "ACK_INDEX", # a string
        "node_id": target_id, # a non-negative number of order 2'^32^', identifying the target node.
        "keyword": keyword # the keyword from the original INDEX message 
        }
        jsmsg = json.dumps(msg)
        self.send(jsmsg,target_ip)

    def searchResponse(self,target_id,target_ip):
        passin = []
        for entry in myNode.URLSave:
            passin.append({"url": entry, "rank": myNode.URLSave[entry]})

        msg ={
        "type": "SEARCH_RESPONSE",
        "word": "word", # The word to search for
        "node_id": target_id,  # target node id
        "sender_id": myNode.ID, # a non-negative number of order 2'^32^', of this message originator
        "response": passin
        } 
        jsmsg = json.dumps(msg)
        self.send(jsmsg,target_ip)    

    def send(self,msg,target):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(msg,(target,UDP_PORT))

    
class receive(object):

    def __init__(self,UDP_PORT,routingTable):
        self.routingTable = routingTable
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        sock.bind((UDP_IP, UDP_PORT))
   
    def messageRead(self,myNode,Message):
        while(True):
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            msg = json.loads(data)
            msgtype = msg["type"]
            if msgtype == "JOINING_NETWORK":
                #send it my own routing table
                Message.routingInfo(msg["node_id"],myNode.ID,self.routingTable)
                #find node 
                nearest = findNearestMatch(myNode.ID,msg[node_id])
                Message.joinNetworkRelay(msg["node_id"],nearest,myNode.ID)            
                self.routingTable.add(msg["node_id"],msg["ip_address"])
                break
                
            elif msgtype == "LEAVING_NETWORK":
                self.routingTable.remove(msg["node_id"])
                #remove data from routing table
                break
            elif msgtype == "JOINING_NETWORK_RELAY":
                if(msg["node_id"] == myNode.ID):
                    Message.routingInfo()
                    break
                else:
                    #node is not me and i shouldnt have received it? orrrrrrrr
                    #forward it to the nearest if its not indeed myself
                    Message.send(data,rTable[findNearestMatch(myNode.ID,msg["target_id"])])
                    break
                
            elif msgtype =="ROUTING_INFO":
                for val in msg["route_table"]:
                    routingTable.add(val["ip_address"],val["node_id"])
                if gateway_id == myNode.ID 
                    Message.send(data,routingTable[msg["node_id"]])
                    break
            elif msgtype == "INDEX":
                if msg["target_id"] == myNode.ID:
                    for url in msg["link"]:
                        if url in mynode.URLSave.keys()
                            myNode.URLSave[url] = myNode.URLSave[url] + 1

                        else:
                            myNode.URLSave[url] = 1
                    #acknowledge index message has been saved to my current indexes
                    Message.ackIndex(msg["sender_id"],rTable[msg["sender_id"]],msg[keyword])
                    break
                else:
                    #send message to node nearest target according to my routing table
                    Message.send(data,rTable[findNearestMatch(myNode.ID,msg["sender_id"])])
                    break
            elif msgtype == "SEARCH"
                if(msg["node_id"] == myNode.ID)
                    Message.searchResponse(msg["sender_id"],routingTable[msg["sender_id"]])
                    break
            elif msgtype == "SEARCH_RESPONSE":
                resp = ""
                for val in msg["response"]:
                    resp += val["url"] + "has been searched:" + val["rank"] + "times!\n" 

                

                return resp 

                else:
                    Message.send(data,findNearestMatch(myNode.ID,msg["myNode"]))
                    break
            elif msgtype == "PING":
                if msg["target_id"] == myNode.ID:
                    Message.ack(myNode,msg["ip_address"])
                    break
                else:
                    Message.send(data,rTable[findNearestMatch(myNode.ID,msg["target_id"])])
                    break
            elif msgtype == "ACK_INDEX":
                if msg["node_id"] != myNode.ID:
                    Message.send(data, rTable[findNearestMatch(myNode.ID,msg["node_id"])])
                    break
class routingTable(dict):    
        
    def add(self,IP,ID):
        if ID not in self.keys():
            self[ID] = IP
    
    def remove(self,ID):
        del self[ID]
    
    def update(self,IP,ID):
        self.remove(ID)
        self.add(IP,ID)
    def findNearestMatch(self,myID,target):
        int(target)
        closest = myID
        for key in self.keys():
            if Math.abs(key - target) < Math.abs(closest- target):
                closest = key
        return closest






def main(word,ip):
     m = message(UDP_PORT)
     r = routingTable()
     n = node(word, ip)
     rec = receive(UDP_PORT,r)
    while(True):
        rec.messageRead(n,m)
        print "would you like to leave[0],search[1], index[2]"
        user = raw_input()
        if user == 0:
            m.leaveNetwork(n,r)
        elif user == 1:
            word = raw_input("what word you looking for? do you feel lucky, punk?")
            m.search(word,n,r)
            currtime = time.time() 
            timeRespCall =  time.time()
            while(abs(currtime- timeRespCall) < 10)
            
                resp = rec.messageRead(n,m)
                    if resp != None
                        print resp    
                        break
                currtime = time.time()
            
            if resp == None
                print "That word aint here, fool!"
        elif user == 2
            
            word = raw_input("what word is it referring to?")
            ind = []
            while(True):
                ind.append (raw_input("what is the url you want it saved to?,press 0 to end"))
                if ind == 0:
                    break
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage:", sys.argv[0], "word IP"
    else:   
        main(sys.argv[1],sys.argv[2])
        