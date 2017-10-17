class Token():
    """Token is a textual chunk (=string) in context, denoted by its positional unique identifier"""
    def __init__(self):
        pass

    def __init__(self,idx,text):
        self.idx=idx
        self.text=text

    def setIdx(self,idx):
        self.idx=idx

    def getIdx(self):
        return self.idx

    def setText(self,text):
        self.text=text

    def getText(self):
        return self.text
