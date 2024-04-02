class SingleTonNew: 
    _instance = None 
    
    def __new__(cls, *args, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance 
         
    def __init__(self, a, b): 
        self.a = a 
        self.b = b

s1 = SingleTonNew(a=11, b=21)
s2 = SingleTonNew(a=11, b=21)
id(s1)
id(s2)