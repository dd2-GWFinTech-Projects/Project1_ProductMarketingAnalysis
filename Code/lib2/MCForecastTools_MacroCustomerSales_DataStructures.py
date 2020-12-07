from UpgradeSequenceDataStructures import UpgradeType
from UpgradeSequenceDataStructures import CustomerBehaviorObservations
from UpgradeSequenceDataStructures import CustomerBehaviorClassifications

class MacroCustomerBehaviorCounts:

    def __init__(self,
            nbr_new_customers,
            nbr_continued_loyal_customers,
            nbr_continued_at_risk_customers,
            nbr_continued_nominal_customers,
            nbr_dropped_customers,
            year):
        self.nbr_new_customers = nbr_new_customers
        self.nbr_continued_loyal_customers = nbr_continued_loyal_customers
        self.nbr_continued_at_risk_customers = nbr_continued_at_risk_customers
        self.nbr_continued_nominal_customers = nbr_continued_nominal_customers
        self.nbr_dropped_customers = nbr_dropped_customers
        self.year = year

    def build_from_list_map(self, item_list_map, index):
        return MacroCustomerBehaviorCounts(
            nbr_new_customers                   = item_list_map[str(CustomerBehaviorClassifications.New)][index],
            nbr_continued_loyal_customers       = item_list_map[str(CustomerBehaviorClassifications.Continued_Loyal)][index],
            nbr_continued_at_risk_customers     = item_list_map[str(CustomerBehaviorClassifications.Continued_AtRisk)][index],
            nbr_continued_nominal_customers     = item_list_map[str(CustomerBehaviorClassifications.Continued_Nominal)][index],
            nbr_dropped_customers               = item_list_map[str(CustomerBehaviorClassifications.Dropped)][index],
            year                                = item_list_map["year"][index]
        )

# Average sales within each customer classification (per year, and per customer)
class MacroCustomerAverageAnnualSales:

    def __init__(self,
            avg_annual_sales_new_customers,
            avg_annual_sales_continued_loyal_customers,
            avg_annual_sales_continued_at_risk_customers,
            avg_annual_sales_continued_nominal_customers,
            avg_annual_sales_dropped_customers,
            year):
        self.avg_annual_sales_new_customers = avg_annual_sales_new_customers
        self.avg_annual_sales_continued_loyal_customers = avg_annual_sales_continued_loyal_customers
        self.avg_annual_sales_continued_at_risk_customers = avg_annual_sales_continued_at_risk_customers
        self.avg_annual_sales_continued_nominal_customers = avg_annual_sales_continued_nominal_customers
        self.avg_annual_sales_dropped_customers = avg_annual_sales_dropped_customers
        self.year = year

    def build_from_list_map(self, item_list_map, index):
        return MacroCustomerAverageAnnualSales(
            avg_annual_sales_new_customers                    = item_list_map[str(CustomerBehaviorClassifications.New)][index],
            avg_annual_sales_continued_loyal_customers        = item_list_map[str(CustomerBehaviorClassifications.Continued_Loyal)][index],
            avg_annual_sales_continued_at_risk_customers      = item_list_map[str(CustomerBehaviorClassifications.Continued_AtRisk)][index],
            avg_annual_sales_continued_nominal_customers      = item_list_map[str(CustomerBehaviorClassifications.Continued_Nominal)][index],
            avg_annual_sales_dropped_customers                = item_list_map[str(CustomerBehaviorClassifications.Dropped)][index],
            year                                              = item_list_map["year"][index]
        )

# def extract_from_list_map(macro_customer_behavior_counts_list_map):
# def extract_from_list_map(macro_customer_avg_annual_sales_list_map):
