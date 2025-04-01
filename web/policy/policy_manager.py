

import web.policy.policy_1
from web.policy.policy_type import FBaseRendingPolicy


class PolicyManager:
    def __init__(self):
        self.policy = {
            "draw_rect" : web.policy.policy_1.FRendingPolicy
        }

    def find_policy(self,name)->FBaseRendingPolicy:
        return self.policy[name]