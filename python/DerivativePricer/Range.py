class Range(object):
    
    def __init__(self, begin, end, interval):
	    self.begin = begin
	    self.end = end
	    self.interval = interval
	    
    def toString(self):
	    print("From",self.begin,"To=",self.end,"Interval=",self.interval)

B = Range(100,200,5)
B.toString()
