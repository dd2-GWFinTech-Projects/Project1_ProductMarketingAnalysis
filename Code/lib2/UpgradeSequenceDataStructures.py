
class UpgradeType(enum.Enum):
    Unknown         = 0
    Started         = 1
    Upgrade         = 2
    Renewal         = 3
    Downgrade       = 4
    Stopped         = 5

class CustomerBehaviorObservations(enum.Enum):
    Active = 0                      # Subscription ends within 1 month of end of year.
    Current = 1                     # Subscription ends past end of current year.
    HasUpgrades = 2                 #
    HasDowngrades = 3               #
    HasMultiplePurchases = 4        #
    HighCoverage = 5                #
    MediumCoverage = 6              #
    LowCoverage = 7                 #
    NewThisYear = 8                 #

class CustomerBehaviorClassifications(enum.Enum):
    New = 0                     # (Active or Current) and NewThisYear
    Continued_Loyal = 1         # ((Active or Current) and (not NewThisYear)) and HighCoverage and HasMultiplePurchases
    Continued_AtRisk = 2        # ((Active or Current) and (not NewThisYear)) and (LowCoverage or HasDowngrades)
    Continued_Nominal = 3       # ((Active or Current) and (not NewThisYear))
    Dropped = 4                 # not (Active or Current)
