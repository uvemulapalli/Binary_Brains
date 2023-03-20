class Range(object):
    
    def __init__(self, begin, end, interval):
	    self.begin = begin
	    self.end = end
	    self.interval = interval
	    
    def display(self):
	    print("From",self.begin,"To=",self.end,"Interval=",self.interval);
