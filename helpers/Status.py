class Status:

    def __init__(self, effect: int, msg: str, category: str, amount: int) :
        self.effect = effect
        self.msg = msg
        self.category = category
        self.amount = amount

    def getEffect(self) -> int:
        return self.effect
