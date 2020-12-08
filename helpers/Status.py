from typing import List


class Status:
    DEFAULT_HOOK_URL ="https://discordapp.com/api/webhooks/784901136946561064/MyLLLTWbJnZWBAgGJlhDxe2rdYOE41qoc03hcNue_rzfWY8HGXayqyLE6VAeO0-72fW1"

    def __init__(self, effect: int, msg: str, category: str, amount: int, hookURLs:List[str]) :
        self.effect = effect
        self.msg = msg
        self.category = category
        self.amount = amount
        self.hookUrls: List[str] = []
        for hookURL in hookURLs:
            self.hookUrls.append(hookURL)

    def getEffect(self) -> int:
        return self.effect

    def getHookUrls(self) -> List[str]:
        return self.hookUrls
