#Mark Whelan  - 10368335    
from time 
import sys
import socket
import json
import random
from numpy import int32
from pif import get_public_ip

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
            
    #class deals with sending of all messages
    #the functions of this class have two basic functionality types
    # 1. create the message as a string to send
    # 2. package as json and send 
class message(object):
    def __init__(self,UDP_PORT):
        pass
        #params(IP to send to, MyID,Receivers ID)
    def joinNetwork(self,ipAddr, src,dest):    
        
        msg = { "type": "JOINING_NETWORK", "node_id": src, "target_id": dest, "ip_address": "127.0.0.1" } 
        jsmsg = json.dumps(msg)
        self.send(jsmsg, ipAddr)
        #need to resolve bootstrap IP with command line arguments
        sock.sendto(jsmsg, (ipAddr, UDP_PORT))
        #params(messageOrigin,Message Destination, myNode, Myrouting table)
    def joinNetworkRelay(self,src,dest,myNode,rTable):
        msg = { "type": "JOINING_NETWORK_RELAY",  "node_id": src.ID, "target_id": dest.ID,"gateway_id": myNode.ID}
        jsmsg = json.dumps(msg)        
        self.send(jsmsg,rTable[findNearestMatch (myNode.ID,dest)])

    def leaveNetwork(self,node,routingTable):
        msg = {"type": "LEAVING_NETWORK", "node_id": node.ID}
        jsmsg = json.dumps(msg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #multicasts message to all nodes in my routing table
        for ip in routingTable.itervalues():    
            self.send(jsmsg,ip)

    def routingInfo(self, Target, Gateway, rTable,myNode):
        rt = []
        #creates json style list(according to spec) of my routing table
        for entry in rTable:
            rt.append({"node_id": entry, "ip_address": rTable[entry]})

        msg = {
        "type": "ROUTING_INFO", 
        "gateway_id": Gateway, 
        "node_id": Target, 
        "ip_address": myNode.IP, 
        "route_table": rt
        }
        jsmsg = json.dumps(msg)
        self.send(jsmsg,Target)

    def index(self,word, URLs,rTable,myNode):
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
        self.send(jsmsg,rTable[myNode.hashCode(word)])
    def search(self,word,myNode,rTable):
        msg = {
        "type": "SEARCH", # string
        "word": word, # The word to search for
        "node_id": myNode.hashCode(word),  # target node id
        "sender_id": myNode.ID, # a non-negative number of order 2'^32^', of this message originator
        }
        jsmsg = js.dumps(msg)
        #this rTable function within function call is messy
        #it finds the nearest node ID to the destination of the hashcoded word 
        #according to my routing table and forwards it to that address
        self.send(jsmsg,rTable[rTable.findNearestMatch(myNode.ID,myNode.hashcode(word))])
        
    def ping(self,target_id,target_ip,myNode,rTable):
        msg = {
        "type": "PING", 
        "target_id": target_id, 
        "sender_id": myNode.ID, 
        "ip_address": myNode.IP 
        }
        jsmsg = json.dumps(msg)
        #same functionality of the above message.send
        self.send(jsmsg,rTable[rTable.findNearestMatch(myNode.ID,target_ip)])
    def ack(self, myNode,target_ip):
        msg = {
        "type": "ACK", 
        "node_id": myNode.ID, 
        "ip_address": myNode.IP 
        }
        self.send(msg,target_ip)
    def ackIndex(self, target_id,target_ip,keyword):
        msg = {
        "type": "ACK_INDEX", 
        "node_id": target_id,
        "keyword": keyword 
        }
        jsmsg = json.dumps(msg)
        self.send(jsmsg,target_ip)

    def searchResponse(self,target_id,target_ip):
        passin = []
        for entry in myNode.URLSave:
            passin.append({"url": entry, "rank": myNode.URLSave[entry]})
            myNode.URLSave[entry]+=1

        msg ={
        "type": "SEARCH_RESPONSE",
        "word": "word", 
        "node_id": target_id,  
        "sender_id": myNode.ID, 
        "response": passin # passes list created above into the json formatted string
        } 
        jsmsg = json.dumps(msg)
        self.send(jsmsg,target_ip)    
        #generic send function used by every above function of this object
    def send(self,msg,target):
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(msg,(target,UDP_PORT))

#class deals with receipt of all messages    
class receive(object):

    def __init__(self,UDP_PORT,routingTable):
        self.routingTable = routingTable
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        sock.bind((UDP_IP, UDP_PORT))
   
    def messageRead(self,myNode,Message):
        while(True):
            data, addr = sock.recvfrom(1024) 
            #load message into json format (a list in python)
            msg = json.loads(data)
            msgtype = msg["type"]
            #If its a join, send it my routing table and check if im 
            if msgtype == "JOINING_NETWORK":
                #send it my own routing table
                Message.routingInfo(msg["node_id"],myNode.ID,self.routingTable)
                #find node it should be routed to if its not me(im gateway and target)
                #send a relay to that node
                nearest = findNearestMatch(myNode.ID,msg[node_id])
                if nearest != myNode.ID:

                    Message.joinNetworkRelay(msg["node_id"],nearest,myNode.ID)
                #add new node to myself regardless            
                self.routingTable.add(msg["node_id"],msg["ip_address"])
                break
                
            elif msgtype == "LEAVING_NETWORK":
                self.routingTable.remove(msg["node_id"])
                #remove data from routing table
                break
            elif msgtype == "JOINING_NETWORK_RELAY":
                #if its me send a routing info message back to gateway
                if(msg["node_id"] == myNode.ID):
                    Message.routingInfo(msg["node_id"],msg["gateway_id"],myNode,routingTable)
                    break
                else:
                    #node is not me and i shouldnt have received it? orrrrrrrr
                    #forward it to the nearest if its not indeed myself
                    Message.send(data,rTable[findNearestMatch(myNode.ID,msg["target_id"])])
                    break
                
            elif msgtype =="ROUTING_INFO":
                #takes all message info regardless
                for val in msg["route_table"]:
                    routingTable.add(val["ip_address"],val["node_id"])
                if gateway_id == myNode.ID 
                    #if im the gateway, send it to the newnode, from my routing table
                    Message.send(data,routingTable[msg["node_id"]])
                    break
            elif msgtype == "INDEX":
                #assuming the message sender is looking for my word
                if msg["target_id"] == myNode.ID:
                    #add all the urls to my dict,if not already there, if s, add 1 to its rank
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
                    #if its a search response not meant for me, send it to my nearest match
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
     bootIP = raw_input("IP of known network node is:")
     bootID = raw_input("and its ID is?")
     m.joinNetwork(bootIP,n.ID,boot.ID)
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
        elif user == 2:
            
            word = raw_input("what word is it referring to?")
            ind = []
            while(True):
                ind.append (raw_input("what is the url you want it saved to?,press 0 to end"))
                if ind == 0:
                    break
            ind.pop()
            m.index(word,ind,r,n)
            #if a node doesnt exist to index this word, were in trouble



if __name__ == "__main__":
    if len(sys.argv) != 3:
        #this initialises a node, you will be asked to join a network after this
        print "usage:", sys.argv[0], "word IP"
    else:   
        main(sys.argv[1],sys.argv[2])
        
