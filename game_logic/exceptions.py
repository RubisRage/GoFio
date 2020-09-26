class GoRuleException(Exception):
    OCCUPIED_EXCEPTION = 0
    KO_EXCEPTION = 1
    SUICIDE_EXCEPTION = 2

    def __init__(self, error_code):
        super().__init__()
        self.error_code = error_code
    
    def __str__(self):
        if self.error_code == GoRuleException.OCCUPIED_EXCEPTION:
            return "Can't play in top of other stones!"
        elif self.error_code == GoRuleException.KO_EXCEPTION:
            return "Can't return to the same board state!"
        elif self.error_code == GoRuleException.SUICIDE_EXCEPTION:
            return "Can't place a stone where there are no liberties!"