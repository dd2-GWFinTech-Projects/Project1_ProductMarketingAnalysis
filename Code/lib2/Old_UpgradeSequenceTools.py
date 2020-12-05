
class OldUpgradeSequenceTool:
    
    def __init__(self, debug_level):
        self.debug_level = debug_level



    # TODO fcn to compute upgrade, downgrade, and delays between them.


    def compute_conversion_type(conversion_sequence):
        broken_conversion_sequence = break_conversion_sequence_based_on_subscription_coverage_gaps(conversion_sequence)
        conversion_sequence = broken_conversion_sequence[-1]
        if did_customer_upgrade(conversion_sequence):  # numerical return?
            return c.Upgrade
        elif did_customer_renew(conversion_sequence):
            return c.Renew
        # elif did_customer_drop():  # customer did not renew within tolerance:
        #     return c.Dropped
        else:
            return c.Dropped  # c.Unknown

    def break_conversion_sequence_based_on_subscription_coverage_gaps(conversion_sequence):
        for subscription_duration_date, subscription_duration_str in conversion_sequence:
            max_subsequent_duration_timeout = _map[subscription_duration_str]


    def did_customer_upgrade(conversion_sequence):
    def did_customer_renew(conversion_sequence):
        # Method 1: Did customer renew within duration tolerance?
        # Method 2: Did customer renew while following discrete coverage rules?
        def compute_subscription_duration_score(subscription_duration_str):
            self.subscription_duration_score_map = {
                        "1 Month": 1.0 / 12.0,
                        "3 Months": 0.25,
                        "6 Months": 0.5,
                        "1 Year": 1.0,
                        "2 Years": 2.0,
                        "3 Years": 3.0 }
            self.subscription_duration_score_max = max(subscription_duration_score_map.values())

            raw_subscription_duration_score = self.subscription_duration_score_map[subscription_duration_str]
            return raw_subscription_duration_score / self.subscription_duration_score_max
        
        if (conversion_sequence contains only upgrades or renewals):

        def compute_subscription_value_score(subscription_duration, number_of_users):
            return None
        # number_of_users_score_map = {
        #             10: ,
        #             50: ,
        #             100
        #             500
        #             1000
        #             5000
        #             10000
        #             50000
                    
        # Method 3: Did customer renew while following continuous coverage rules?










