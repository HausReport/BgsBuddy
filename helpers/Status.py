class Status:
    DEFAULT_HOOK_URL ="https://discordapp.com/api/webhooks/784901136946561064/MyLLLTWbJnZWBAgGJlhDxe2rdYOE41qoc03hcNue_rzfWY8HGXayqyLE6VAeO0-72fW1"

    def __init__(self, effect: int, msg: str, category: str, amount: int, hookURL=DEFAULT_HOOK_URL) :
        self.effect = effect
        self.msg = msg
        self.category = category
        self.amount = amount
        self.hookUrl = hookURL

    def getEffect(self) -> int:
        return self.effect

    def getHookUrl(self) -> int:
        return self.hookUrl
