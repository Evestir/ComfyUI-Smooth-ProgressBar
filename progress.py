from time import sleep
import threading

#-------------- Easing Functions --------------#
def BezierBlend(t: float):
    sqr = t * t
    return sqr / (2.0 * (sqr - t) + 1.0)

def easeOutCirc(t: float):
    return math.sqrt(1 - math.pow(t - 1, 2))

def easeInOutBack(t: float):    
    c1 = 1.70158
    c2 = 2.5949095
    ret = 0

    if t < 0.5:
        ret = (math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    else:
        ret = (math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2
    return ret
#----------------------------------------------#

def is_odd(n):
    if n % 2 == 0:
        return False
    else:
        return True
    
def is_undivisible_3(n):
    if n % 3 == 0:
        return False
    else:
        return True

#--------------- Configuration ----------------#
sleepTime = 0.0015
steps = 200
multiplyFactor = math.floor(10000 / steps) / 10000
#----------------------------------------------#

class ProgressBar:
    def __init__(self, total):
        global PROGRESS_BAR_HOOK
        self.total = total
        self.current = 0
        self.hook = PROGRESS_BAR_HOOK

    def update_absolute(self, value, total=None, preview=None):
        def hook():
            if self.hook is not None:
                self.hook(self.current, self.total, preview)
        if total is not None:
            self.total = total
        if value > self.total:
            value = self.total

        # Display progress only when the completed steps are two compared to the period when the last animation happend.
        if is_undivisible_3(value) and value is not total:
            return
        def animate():
            origin = self.current
            diff = value - origin
            for i in range(steps):
                self.current = origin + (easeOutCirc(i * multiplyFactor) * diff)
                sleep(sleepTime)
                hook()
            self.current = value # Ensure
            #print(f" value {value} total {total} self.current {self.current}")
            if value == total: # Once the progress bar reaches 100%, then this motion will be played.     
                for i in range(steps):
                    self.current = total - (BezierBlend(i * multiplyFactor) * total)
                    hook()
                    sleep(sleepTime)
        thread = threading.Thread(target=animate)
        thread.start()
        if value == total:
            thread.join()

    def update(self, value):
        self.update_absolute(self.current + value)
