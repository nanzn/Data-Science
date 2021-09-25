def proportion_of_education():
    """ Proportion of children based on mother's education level. """
    import pandas as pd
    # Read CSV
    df = pd.read_csv("1-Intro/assets/NISPUF17.csv")

    # Number of Rows 
    nrow = df["EDUC1"].count()

    # Proportion in each group
    proportion = df.groupby("EDUC1").size()/nrow

    proportion.rename(index={
        1: "less than high school",
        2: "high school",
        3: "more than high school but not college",
        4: "college"
    }, inplace=True)

    # Create Dictionary
    results = proportion.to_dict()

    return results

#print(proportion_of_education())

def average_influenza_doses():
    """ Average no. of influenza vaccines for children we know received breastmilk as a child and those who know did not """
    import pandas as pd
    # Read CSV
    df = pd.read_csv("1-Intro/assets/NISPUF17.csv")
    vaccine_df = df["P_NUMFLU"]
    # Average vaccine for child who received breast milk 
    received = vaccine_df[df["CBF_01"].eq(1)].mean()
    # Average vaccine for child who received breast milk 
    not_received = vaccine_df[df["CBF_01"].eq(2)].mean()
    
    return received, not_received

#print(average_influenza_doses())

def chickenpox_by_sex():
    """ Ratio of the number of children who contracted chickenpox but were vaccinated against it versus those who were vaccinated but did not contract chick pox by sex"""
    import pandas as pd
    # Read CSV
    df = pd.read_csv("1-Intro/assets/NISPUF17.csv") # Relevant columns: "HAD_CPOX", "P_NUMVRC", "SEX"

    # Count of vaccinated and contracted children by gender
    male_vac_cp = len(df[df["P_NUMVRC"].gt(0) & df["SEX"].eq(1) & df["HAD_CPOX"].eq(1)])
    female_vac_cp = len(df[df["P_NUMVRC"].gt(0) & df["SEX"].eq(2) & df["HAD_CPOX"].eq(1)])
    
    # Count of vaccinated and not contracted children by gender
    male_vac_ncp = len(df[df["P_NUMVRC"].gt(0) & df["SEX"].eq(1) & df["HAD_CPOX"].eq(2)])
    female_vac_ncp = len(df[df["P_NUMVRC"].gt(0) & df["SEX"].eq(2) & df["HAD_CPOX"].eq(2)])
    
    # Calculate Ratio
    male = male_vac_cp / male_vac_ncp
    female = female_vac_cp / female_vac_ncp

    # Results dictionary
    results = {"male": male, "female": female}

    return results

#print(chickenpox_by_sex())

def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd
    
    # Read CSV
    df = pd.read_csv("1-Intro/assets/NISPUF17.csv") # Relevant columns: "HAD_CPOX", "P_NUMVRC"

    # Data cleaning
    # For "HAD_CPOX" only keep rows with 1=YES or 2=NO
    # For "P_NUMVRC" only keep rows with not "nan"
    df=df[df["HAD_CPOX"].lt(3) & df["P_NUMVRC"].notna()]
    df=pd.DataFrame({"had_chickenpox_column":df["HAD_CPOX"],
    "num_chickenpox_vaccine_column":df["P_NUMVRC"]})

    # here is some stub code to actually run the correlation
    corr, pval=stats.pearsonr(df["had_chickenpox_column"],df["num_chickenpox_vaccine_column"])
    
    # just return the correlation
    return corr

print(corr_chickenpox())