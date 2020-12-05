
class UpgradeType(enum.Enum):
    Unknown         = 0
    Started         = 1
    Upgrade         = 2
    Renewal         = 3
    Downgrade       = 4
    Stopped         = 5


class UpgradeSequenceTool:
    
    def __init__(self, debug_level):
        self.debug_level = debug_level
    
    # Define a function to extract the conversion upgrade sequence
    def get_upgrade_sequence(df):
        customer_subscriptions_ordered_by_date = df.loc[:, ["ServiceStart", "ServiceEnd", "Subscription", "SubscriptionDuration_Timedelta", "SubscriptionDuration_Years"]].sort_values("ServiceStart")
        return (df.index[0], customer_subscriptions_ordered_by_date)

    def extract_dict_values_to_dataframe(data_dict):
        df = pd.DataFrame({})
        for value in data_dict.values():
            df = df.append(value[1])
        return df
        
    def compute_subscription_coverage_df(df):
        
        subscription_coverage_years_outer = (df["ServiceEnd"][-1] - df["ServiceStart"][0]).days / constants.DAYS_PER_YEAR
        
        subscription_coverage_list = []
        subscription_coverage_years_covered = 0
        for index, row in df.iterrows():
            subscription_coverage_years_covered += row["SubscriptionDuration_Years"]
            subscription_coverage_list.append(subscription_coverage_years_covered / subscription_coverage_years_outer)
        
        return subscription_coverage_list

    def compute_upgrade_type_df(df):
        
        upgrade_type_list = []
        prev_subscription_duration_years = None

        for index, row in df.iterrows():

            # Get current subscription duration
            subscription_duration_years = row["SubscriptionDuration_Years"]
            if (prev_subscription_duration_years == None):
                prev_subscription_duration_years = subscription_duration_years
                upgrade_type_list.append(UpgradeType.Started)
                continue

            # Determine subscription type
            if subscription_duration_years > prev_subscription_duration_years:
                upgrade_type = UpgradeType.Upgrade
            elif subscription_duration_years == prev_subscription_duration_years:
                upgrade_type = UpgradeType.Renewal
            elif subscription_duration_years < prev_subscription_duration_years:
                upgrade_type = UpgradeType.Downgrade
            else:
                upgrade_type = UpgradeType.Unknown
            
            # Build upgrade_type_list
            upgrade_type_list.append(upgrade_type)

            # Store previous subscription duration
            prev_subscription_duration_years = subscription_duration_years
        
        return upgrade_type_list


class UpgradeSequenceFilterTool:
    
    def __init__(self, debug_level):
        self.debug_level = debug_level
        self.today = pd.Timestamp.now(tz="America/New_York")
        self.current_year = today.year
        self.high_coverage_threshold = 10.0 / 12.0
        self.low_coverage_threshold = 3.0 / 12.0

    
    # Source: https://blog.finxter.com/how-to-filter-a-dictionary-in-python/#:~:text=%20The%20Most%20Pythonic%20Way%29%20%201%20Method,iterable%29%20function%20takes%20a%20function%20as...%20More%20
    def filter_dict(d, f):
        ''' Filters dictionary d by function f. '''
        newDict = dict()
        # Iterate over all (k,v) pairs in names
        for key, value in d.items():
            # Is condition satisfied?
            if f(key, value):
                newDict[key] = value
        return newDict

    # Time-based filters
    def filter_active_customers(key, value):
        last_service_end_date = value[1]["ServiceEnd"][-1]
        duration_days_until_service_end = (last_service_end_date - today).days
        return duration_days_until_service_end >= 0

    def filter_new_customers_2020(key, value):
        first_service_start_date = value[1]["ServiceStart"][0]
        return first_service_start_date.year == current_year

    def filter_new_customers_march2020(key, value):
        TODO
        first_service_start_date = value[1]["ServiceStart"][0]
        return first_service_start_date.year == current_year


    # Upgrade type filters
    def filter_customers_with_upgrades(key, value):
        upgrade_type = value[1]["UpgradeType"]
        upgrade_type_set = set(upgrade_type.to_list())

        if length == 1:
            return UpgradeType.Started in upgrade_type_set
        else:
            return UpgradeType.Upgrade in upgrade_type_set

    def filter_customers_with_downgrades(key, value):
        upgrade_type = value[1]["UpgradeType"]
        upgrade_type_set = set(upgrade_type.to_list())
        return UpgradeType.Downgrade in upgrade_type_set


    # Coverage filters
    def filter_high_coverage_customers(key, value):
        subscription_coverage = value[1]["SubscriptionCoverage"][-1]
        return subscription_coverage >= high_coverage_threshold

    def filter_medium_coverage_customers(key, value):
        subscription_coverage = value[1]["SubscriptionCoverage"][-1]
        return (subscription_coverage < high_coverage_threshold) and (subscription_coverage > low_coverage_threshold)

    def filter_low_coverage_customers(key, value):
        subscription_coverage = value[1]["SubscriptionCoverage"][-1]
        return subscription_coverage <= low_coverage_threshold




class UpgradeSequenceReportTool:
    
    def __init__(self, debug_level):
        self.debug_level = debug_level
        
        
    def generate_basic_customer_report_data()
        active_customers_dict = filter_dict(upgrade_sequence_dict, filter_active_customers)


        # Compute and validate total number of customers
        total_number_of_customers_1 = len(set(invoice_data_by_customer.index))
        total_number_of_customers_2 = len(upgrade_sequence_dict)
        
        len(invoice_data_by_customer.index)


    def generate_basic_customer_report()
        print(f"Customer Purchase History Report")
        print(f"--------------------------------")
        print(f"")
        print(f"There are currently {len(active_customers_dict)} active and {len(upgrade_sequence_dict) - len(active_customers_dict)} inactive customers.")

        print(f"There are {total_number_of_customers_1} total customers according to the invoice_data_by_customer DataFrame, and {total_number_of_customers_2} for upgrade_sequence_dict.")





    def generate_customer_purchase_history_report_data(customers_dict):

        new_customers_2020_dict = filter_dict(customers_dict, filter_new_customers_2020)
        new_customers_march2020_dict = filter_dict(customers_dict, filter_new_customers_march2020)

        customers_with_upgrades_dict = filter_dict(customers_dict, filter_customers_with_upgrades)
        customers_with_downgradess_dict = filter_dict(customers_dict, filter_customers_with_downgrades)

        high_coverage_customers_dict = filter_dict(customers_dict, filter_high_coverage_customers)
        medium_coverage_customers_dict = filter_dict(customers_dict, filter_medium_coverage_customers)
        low_coverage_customers_dict = filter_dict(customers_dict, filter_low_coverage_customers)

        # Build customer purchase history report data
        customer_purchase_history_report = pd.DataFrame.from_dict({
            f"New Customers (as of 2020)":                                                   len(new_customers_2020_dict),
            f"New Customers (as of 2020)":                                                   len(new_customers_march2020_dict),
            f"Customers with Upgrades (see footnote 1)":                                     len(customers_with_upgrades_dict),
            f"Customers with Downgrades":                                                    len(customers_with_downgradess_dict),
            f"Customers with High Subscription Coverage (see footnote 2,3)":                 len(high_coverage_customers_dict),
            f"Customers with Medium Subscription Coverage":                                  len(medium_coverage_customers_dict),
            f"Customers with Low Subscription Coverage":                                     len(low_coverage_customers_dict)
            }, orient="index", columns=[""])




    def generate_customer_purchase_history_report_data():

        print(f"Customer Purchase History Report")
        print(f"--------------------------------")
        print(f"")
        print(f"Of the {} customers, the following customer behaviors are identified based on the purchase history:")
        print(f"")
        display(customer_purchase_history_report)
        print(f"")
        print(f"")
        print(f"(1) The existence of Upgrades and Downgrades is considered across the entire customer's purchase history.")
        print(f"(2) Subscription coverage refers to the fraction of time during which the customer has had an active subscription, divided by the total period of time in which the customer has been a customer.")
        print(f"(3) The thresholds used for high, medium, and low subscription coverage are as follows: High (>={high_coverage_threshold}), Medium ({low_coverage_threshold} to {high_coverage_threshold}), Low (<={low_coverage_threshold})")
        print(f"")






