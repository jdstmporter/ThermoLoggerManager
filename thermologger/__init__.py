from .main import RunLoop

def action():
    loop=RunLoop()
    loop.run()

if __name__=='__main__':
    action()