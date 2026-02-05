def z_score_outliers(df, feature):
    if df[feature].std() == 0:
        return 
    
    low = df[feature].mean() - 3 * df[feature].std()
    high = df[feature].mean() + 3 * df[feature].std()

    return df[(df[feature] > high) | (df[feature] < low)]

def iqr_outliers(df, feature):
    if df[feature].std() == 0:
        return 0
    
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)

    IQR = Q3 - Q1

    low = Q1 - 1.5 * IQR
    high = Q3 + 1.5 * IQR

    return df[(df[feature] > high) | (df[feature] < low)]