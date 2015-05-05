
class ThreadSafeDict(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

    def __iter__(self):
        return ThreadSafeDictIterator(self)

    def iteritems(self):
        return ThreadSafeDictIterator(self)

"""
        def append(self, i):
                self[i] = i        
    
        def remove(self, i):
                del self[i]
"""

class ThreadSafeDictIterator:
    def __init__(self, dict):
        self.__dict = dict
        self.__keys = dict.keys()
        self.__x = -1
    
    def __iter__(self):
        return self
        
    def next(self):
        self.__x += 1
        # Check if we've reached the end
        if self.__x == len(self.__keys):
            raise StopIteration
        # Check if this value still exists in the original dictionary, TODO: Check and Retrieve in lock?
        value = self.__dict.get(self.__keys[self.__x], None)
        if value == None:
            return self.next()
        else:
            return value

from collections import deque

class ThreadSafeList(deque):
    """thread safe deque using generator to iterate"""

    def __init__(self, iterable=None, maxlen=None):
        if iterable == None and maxlen == None:
            super(deque, self).__init__()
        elif maxlen == None:
            super(deque, self).__init__(iterable)
        else:
            super(deque, self).__init__(iterable, maxlen)
        #eif

    def __iter__(self):
        return self

    def next(self):
        x = self.popleft()
        self.append(x)
        yield x


# Thinking need my own thread safe linked list?


class ThreadSafeLinkedList(object):
    def __init__(self):
        self.__head = None
        self.__last = None
        self.__itemcount = 0

    def __len__(self):
        return self.__itemcount

    def append(self, item):
        if self.__head == None:
            self.__head = Node(item)
            self.__last = self.__head
        else:
            self.__last.nextnode = Node(item)
            self.__last = self.__last.nextnode
        self.__itemcount += 1

    def remove(self, item):
        if self.__last == None: return False
        current = self.__head
        if item == current.data:
            self.__head = current.nextnode
            if self.__head == None: 
                self.__last = None
            self.__itemcount -= 1
            return True
        last = current
        while current.nextnode != None:
            if item == current.nextnode.data:
                current.nextnode = current.nextnode.nextnode
                if current.nextnode == None:
                    self.__last = current
                self.__itemcount -= 1 
                return True
            last = current
            current = current.nextnode
        if current.data == item:
            last.nextnode = None
            self.__last = last
            self.__itemcount -= 1
            return True
        return False

    def __iter__(self):
        if self.__last == None:
            return
        current = self.__head
        yield current.data
        while current.nextnode != None:
            yield current.nextnode.data
            current = current.nextnode

class Node(object):
    def __init__(self, data):
        self.data = data
        self.nextnode = None

if __name__ == "__main__":
    import timeit      
    s1 = """\
        for i in xrange(2000):
            t.append(i)
        """
    s2 = """\
        for i in xrange(2000):
            t.append(i)
        for i in xrange(900, 1100):
            t.remove(i)
        """
    s3 = """\
        for i in xrange(2000):
            t.append(i)
        for i in t:
            x = repr(i)
         """ 
    t = timeit.Timer(s1, "t = []")
    la1 = t.timeit(number=10)/10
    print "List Add: %.2f usec/pass" % (100 * la1)
    t = timeit.Timer(s1, "from collections import deque; t = deque()")
    da1 = t.timeit(number=10)/10
    print "Deque Add: %.2f usec/pass" % (100 * da1)
    t = timeit.Timer(s1, "from __main__ import ThreadSafeLinkedList; t = ThreadSafeLinkedList()")
    tslla1 = t.timeit(number=10)/10
    print "TSLL Add: %.2f usec/pass" % (100 * tslla1)
    t = timeit.Timer(s1, "from __main__ import ThreadSafeDict; t = ThreadSafeDict()")
    tsd1 = t.timeit(number=10)/10
    print "TSD Add: %.2f usec/pass" % (100 * tsd1)	
    
    t = timeit.Timer(s2, "t = []")
    la2 = t.timeit(number=10)/10 - la1
    print "List Rem: %.2f usec/pass" % (100 * la2)
    t = timeit.Timer(s2, "from collections import deque; t = deque()")
    da2 = t.timeit(number=10)/10 - da1
    print "Deque Rem: %.2f usec/pass" % (100 * da2)
    t = timeit.Timer(s2, "from __main__ import ThreadSafeLinkedList; t = ThreadSafeLinkedList()")
    tslla2 = t.timeit(number=10)/10 - tslla1
    print "TSLL Rem: %.2f usec/pass" % (100 * tslla2)
    t = timeit.Timer(s2, "from __main__ import ThreadSafeDict; t = ThreadSafeDict()")
    tsd2 = t.timeit(number=10)/10 - tsd1
    print "TSD Rem: %.2f usec/pass" % (100 * tsd2)
    
    t = timeit.Timer(s3, "t = []")
    la2 = t.timeit(number=10)/10 - la1
    print "List Iter: %.2f usec/pass" % (100 * la2)
    t = timeit.Timer(s3, "from collections import deque; t = deque()")
    da2 = t.timeit(number=10)/10 - da1
    print "Deque Iter: %.2f usec/pass" % (100 * da2)
    t = timeit.Timer(s3, "from __main__ import ThreadSafeLinkedList; t = ThreadSafeLinkedList()")
    tslla2 = t.timeit(number=10)/10 - tslla1
    print "TSLL Iter: %.2f usec/pass" % (100 * tslla2)	
    t = timeit.Timer(s3, "from __main__ import ThreadSafeDict; t = ThreadSafeDict()")
    tsd2 = t.timeit(number=10)/10 - tsd1
    print "TSD Iter: %.2f usec/pass" % (100 * tsd2)
