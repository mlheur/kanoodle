

class Pip(object):

    def __init__(self,X,Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return(f'{self.X+1},{self.Y+1}')
    
    def rotate(self,sine_theta):
        newX = -1 * (self.Y * sine_theta)
        newY = (self.X * sine_theta)
        self.X = newX
        self.Y = newY
    def ror(self): self.rotate(1)
    def rol(self): self.rotate(-1)

    def trxlate(self,xoff,yoff):
        self.X = self.X + xoff
        self.Y = self.Y + yoff


if __name__ == "__main__":
    plist = {Pip(0,0),Pip(1,0),Pip(2,0),Pip(0,1),Pip(2,1)}
    for p in plist:
        print(f'PreRor: {p}')
    for p in plist:
        p.ror()
        p.trxlate(1,0)
    for p in plist:
        print(f'PosRor: {p}')
    for p in plist:
        p.ror()
        p.trxlate(2,0)
    for p in plist:
        print(f'Further: {p}')
