class Element(object):
    def __init__(self, *args, **kwargs):
        size = kwargs.get("size", 0)
        superfamily = kwargs.get("superfamily", None)

class Retroelement(Element):
    def __init__(self, *args, **kwargs):
        super(Retroelement, self).__init__(args, kwargs)

        orf_1 = kwargs.get("orf_1", (0, 0))
        orf_2 = kwargs.get("orf_2", (0, 0))

class LTR(Retroelement):
    def __init__(self, *args, **kwargs):
        super(LTR, self).__init__(args, kwargs)
    
        ltr_5 = kwargs.get("ltr_5", (0, 0))
        ltr_3 = kwargs.get("ltr_3", (0, 0))
        orf_3 = kwargs.get("orf_3", (0, 0))

class LINE(Retroelement):
    def __init__(self, *args, **kwargs):
        super(LINE, self).__init__(args, kwargs)

        utr_5 = kwargs.get("utr_5", (0, 0))
        utr_3 = kwargs.get("utr_3", (0, 0))

class SINE(Retroelement):
    def __init__(self, *args, **kwargs):
        super(SINE, self).__init__(args, kwargs)

class DNATransposon(Element):
    def __init__(self, *args, **kwargs):
        super(DNATransposon, self).__init__(args, kwargs)

class Other(Element):
    def __init__(self, *args, **kwargs):
        super(Other, self).__init__(args, kwargs)
