'''creating an interface class that will include the physical interfaces only (no loopback or virtual)
interface attributes 
    iname: interface name
    itype: interface type (Ethernet, Wireless, USB)
    istat: insterface stat (UP or DOWN)
    ilink: connection stat (UP or DOWN)
    ipadd: the ip address (if connected Ex. 192.168.1.5/24 or "NULL" for not connected interfaces)
interface methods
    show:       print current attribute values
    set_up:     bring the interface to UP stat
    set_down:   bring the interface to DOWN stat
    connect:    bring connection stat to UP
    disconnect: bring connection stat to DOWN
'''
class interface:
    def __init__(self,n,t,s,l):
        self.iname = n
        self.itype = t
        self.istat = s
        self.ilink = l
        self.ipadd = ["NULL"]
        if self.ilink == "UP":
            shellcommand = r"ip addr show dev "+self.iname+r" | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}'"
            process = subprocess.run(shellcommand, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            self.ipadd = list(filter(None,map(str.strip, process.stdout.split("\n"))))
    def show(self):
        print(self.iname,self.itype,self.istat,self.ilink,self.ipadd)
    def set_up(self):
        process = subprocess.run("ip link set " + self.iname + " up", shell=True,\
            check=True, stdout=subprocess.PIPE, universal_newlines=True)
        if(process.stdout == ""):
            print("interface statu changed successfully")
            self.istat = "UP"