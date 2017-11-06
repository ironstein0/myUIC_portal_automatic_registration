from threading import Timer

def hello_world():
    print('hello world')

t1 = Timer(4.0, hello_world)
t2 = Timer(5.0, hello_world)
t1.start()
t2.start()