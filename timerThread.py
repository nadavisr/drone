from threading import Thread
import time

class Timer(Thread):
    def __init__(self, event, function, channels, interval):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.function = function
        self.channels = channels

    def run(self):
        #first time no delay
        if(not self.channels.isStarted):
            self.channels.isStarted = True
            thread = Thread(target=self.function)
            thread.start()

        while (not self.stopped.wait(self.interval)):
            self.channels.stopListen = True
            self.channels.isStarted = True

            if self.stopped.is_set():
                print('timer thread exiting...')
                return

            time.sleep(0.01)
            thread = Thread(target=self.function)
            thread.start()
