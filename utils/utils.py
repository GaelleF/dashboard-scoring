import gc
import numpy as np
import pandas as pd


def scoring_result(target):
    if target == 0:
        scoring = 'Prêt accepté'
    else:
        scoring = 'Prêt refusé'
    return scoring


def get_columns(data):
    columns = []
    for c in data.columns:
        # print(c)
        if (data[c].nunique() < 30) & (c not in ['TARGET']):
            columns.append(c)
    return columns


# Rare Encoding
def rare_encoder(dataframe, rare_perc, cat_cols):

    rare_columns = [col for col in cat_cols if
                    (dataframe[col].value_counts() / len(dataframe) < rare_perc).sum() > 1]

    for col in rare_columns:
        tmp = dataframe[col].value_counts() / len(dataframe)
        rare_labels = tmp[tmp < rare_perc].index
        dataframe[col] = np.where(dataframe[col].isin(
            rare_labels), 'Rare', dataframe[col])

    return dataframe

# One-hot Encoding


def one_hot_encoder(df, nan_as_category=True):
    original_columns = list(df.columns)
    categorical_columns = [
        col for col in df.columns if df[col].dtype == 'object']
    df = pd.get_dummies(df, columns=categorical_columns,
                        dummy_na=nan_as_category)
    new_columns = [c for c in df.columns if c not in original_columns]
    return df, new_columns


def application_train_test(df, num_rows=None, nan_as_category=False):
    df = df.reset_index()

    # Cinsiyeti belirtilmeyen 4 kişi var bunları çıkarıyoruz.
    df = df[df['CODE_GENDER'] != 'XNA']
    # Medeni durumu unknown olan 1 kişi var bunu dropladık.
    df = df[df['NAME_FAMILY_STATUS'] != "Unknown"]
    # NaN values for DAYS_EMPLOYED: 365243 -> nan
    df['DAYS_EMPLOYED'].replace(365243, np.nan, inplace=True)

    ########
    # RARE
    ########
    # NAME_INCOME_TYPE değişkeninin 4 sınıfının frekansı diğerlerine göre düşük olduğunu gözlemledik.
    # Bu nedenle bu 4 sınıfı kendilerine en yakın olabilecek sınıfın için dahil ettik.
    # Yani rare sınıfını diğerlerine eklemiş olduk.
    df.loc[df['NAME_INCOME_TYPE'] == 'Businessman',
           'NAME_INCOME_TYPE'] = 'Commercial associate'
    df.loc[df['NAME_INCOME_TYPE'] == 'Maternity leave',
           'NAME_INCOME_TYPE'] = 'Pensioner'
    df.loc[df['NAME_INCOME_TYPE'] == 'Student',
           'NAME_INCOME_TYPE'] = 'State servant'
    df.loc[df['NAME_INCOME_TYPE'] == 'Unemployed',
           'NAME_INCOME_TYPE'] = 'Pensioner'

    # ORGANIZATION_TYPE
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].str.contains("Business Entity"),
                                       "Business_Entity", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].str.contains("Industry"),
                                       "Industry", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].str.contains("Trade"),
                                       "Trade", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].str.contains("Transport"),
                                       "Transport", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].isin(["School", "Kindergarten", "University"]),
                                       "Education", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].isin(["Emergency", "Police", "Medicine", "Goverment",
                                       "Postal", "Military", "Security Ministries", "Legal Services"]), "Official", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].isin(["Bank", "Insurance"]),
                                       "Finance", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].str.contains("Goverment"),
                                       "Government", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].isin(
        ["Realtor", "Housing"]), "Realty", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].isin(
        ["Hotel", "Restaurant", "Services"]), "TourismFoodSector", df["ORGANIZATION_TYPE"])
    df["ORGANIZATION_TYPE"] = np.where(df["ORGANIZATION_TYPE"].isin(
        ["Cleaning", "Electricity", "Telecom", "Mobile", "Advertising", "Religion", "Culture"]), "Other", df["ORGANIZATION_TYPE"])

    # OCCUPATION_TYPE
    df["OCCUPATION_TYPE"] = np.where(df["OCCUPATION_TYPE"].isin(["Low-skill Laborers", "Cooking staff", "Security staff",
                                     "Private service staff", "Cleaning staff", "Waiters/barmen staff"]), "Low_skill_staff", df["OCCUPATION_TYPE"])
    df["OCCUPATION_TYPE"] = np.where(df["OCCUPATION_TYPE"].isin(
        ["IT staff", "High skill tech staff"]), "High_skill_staff", df["OCCUPATION_TYPE"])
    df["OCCUPATION_TYPE"] = np.where(df["OCCUPATION_TYPE"].isin(
        ["Secretaries", "HR staff", "Realty agents"]), "Others", df["OCCUPATION_TYPE"])

    # NAME_EDUCATION_TYPE
    # Akademik derecenin frekansı az olduğu için bununla yüksek eğitimi aynı sınıfa aldık.
    df["NAME_EDUCATION_TYPE"] = np.where(df["NAME_EDUCATION_TYPE"] == "Academic degree",
                                         "Higher education", df["NAME_EDUCATION_TYPE"])

    df["NAME_EDUCATION_TYPE"] = np.where(df["NAME_EDUCATION_TYPE"].str.contains("Secondary / secondary special"),
                                         "Secondary_secondary_special", df["ORGANIZATION_TYPE"])

    # NAME_FAMILY_STATUS
    df["NAME_FAMILY_STATUS"] = np.where(df["NAME_FAMILY_STATUS"].str.contains("Single / not married"),
                                        "Single_not_married", df["NAME_FAMILY_STATUS"])

    # NAME_HOUSING_TYPE
    df["NAME_HOUSING_TYPE"] = np.where(df["NAME_HOUSING_TYPE"].str.contains("House / apartment"),
                                       "House_apartment", df["NAME_HOUSING_TYPE"])

    # NAME_CONTRACT_TYPE
    # Kategorik olan ama cinsiyet gibi 0 ve 1 olarak kodlanacak değişkenlere binary encode yaptık.
    for bin_feature in ["NAME_CONTRACT_TYPE", 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']:
        df[bin_feature], uniques = pd.factorize(df[bin_feature])

    # WEEKDAY_APPR_PROCESS_START
    # Gün isimlerini 1,2,3....,7 olarak değiştireceğiz.
    # Daha sonra günler döngüsel yapıda oldukları için bunlara cycle encode uygulayacağız.
    # Asıl değişkenleri silmedik feature importance da bak!
    weekday_dict = {'MONDAY': 1, 'TUESDAY': 2, 'WEDNESDAY': 3,
                    'THURSDAY': 4, 'FRIDAY': 5, 'SATURDAY': 6, 'SUNDAY': 7}
    df.replace({'WEEKDAY_APPR_PROCESS_START': weekday_dict}, inplace=True)
    # Cycle encode
    df['NEW_WEEKDAY_APPR_PROCESS_START' +
        "_SIN"] = np.sin(2 * np.pi * df["WEEKDAY_APPR_PROCESS_START"]/7)
    df["NEW_WEEKDAY_APPR_PROCESS_START" +
        "_COS"] = np.cos(2 * np.pi * df["WEEKDAY_APPR_PROCESS_START"]/7)

    # HOUR_APPR_PROCESS_START
    # değişken müşterinin hangi saatte başvurduğu bilgisini veriyordu.
    # Saat bilgisi de yine döngüsel olduğu için buna da cycle encode yapıyoruz.
    df['NEW_HOUR_APPR_PROCESS_START' +
        "_SIN"] = np.sin(2 * np.pi * df["HOUR_APPR_PROCESS_START"]/23)
    df["NEW_HOUR_APPR_PROCESS_START" +
        "_COS"] = np.cos(2 * np.pi * df["HOUR_APPR_PROCESS_START"]/23)

    ###########
    # DROP
    ###########
    # FLAG_MOBIL ve FLAG_CONT_MOBILE değişkenlerinde iki alt sınıfı var ve birinin frekansı çok az.
    # Yani bilgi taşımayan değişken bu nedenle drop ediyoruz.
    drop_cols = ["FONDKAPREMONT_MODE", "WALLSMATERIAL_MODE", "HOUSETYPE_MODE",
                 "EMERGENCYSTATE_MODE", "FLAG_MOBIL", "FLAG_EMP_PHONE", "FLAG_WORK_PHONE", "FLAG_CONT_MOBILE",
                 "FLAG_PHONE", "FLAG_EMAIL", "NAME_TYPE_SUITE"]
    df.drop(drop_cols, axis=1, inplace=True)

    # OBS_30_CNT_SOCIAL_CIRCLE,OBS_60_CNT_SOCIAL_CIRCLE
    df.drop(['OBS_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE'],
            axis=1, inplace=True)

    # REGION
    # Bu değişkenler bölge ve şehir bazında ayrı ayrı puan veriyordu
    # Biz bunları toplayarak tek bir değişken elde ettik ve diğerlerini dropladık.
    cols = ["REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION", "LIVE_REGION_NOT_WORK_REGION",
            "REG_CITY_NOT_LIVE_CITY", "REG_CITY_NOT_WORK_CITY", "LIVE_CITY_NOT_WORK_CITY"]
    df["NEW_REGION"] = df[cols].sum(axis=1)
    df.drop(cols, axis=1, inplace=True)

    # Flag_DOCUMENT
    # Bu değişkenler her dökümanın ayrı ayrı verilip verilmediği bilgisini veriyordu.
    # Biz bunları toplayarak tek bir değişken elde ettik,yani totalde verilen belge sayısını hesapladık
    # ve diğerlerini dropladık.
    docs = [col for col in df.columns if 'FLAG_DOC' in col]
    df['NEW_DOCUMENT'] = df[docs].sum(axis=1)
    df.drop(docs, axis=1, inplace=True)

    ##########################
    # FEATURE ENGINEERING
    ##########################

    # 2. Müşterinin toplam geliri / kredi tutarı
    df['NEW_INCOME_CREDIT_RATIO'] = df['AMT_INCOME_TOTAL'] / df['AMT_CREDIT']

    # 12. Kişinin DAYS_BIRTH değişkeni gün cinsindn yaşını veriyordu.
    # Ama değerler - (çünkü şu kadar gün önce doğmuş bilgisini veriyor.)
    # Bu yüzden müşterinin yaşını bulmak için - ile çarpıp 360 a böleceğiz.
    df["NEW_DAYS_BIRTH"] = round(df["DAYS_BIRTH"] * -1 / 365)
    df['AGE'] = df["NEW_DAYS_BIRTH"]
    # 13. Yaşlara göre müşterileri segmentlere ayırma
    df.loc[df["NEW_DAYS_BIRTH"] <= 34, "NEW_SEGMENT_AGE"] = "Young"
    df.loc[(df["NEW_DAYS_BIRTH"] > 34) & (df["NEW_DAYS_BIRTH"] <= 54),
           "NEW_SEGMENT_AGE"] = "Middle_Age"
    df.loc[(df["NEW_DAYS_BIRTH"] > 54), "NEW_SEGMENT_AGE"] = "Old"

    # 14. Gelire göre müşterileri segmentlere ayırma
    df.loc[df["AMT_INCOME_TOTAL"] <= 112500,
           "NEW_SEGMENT_INCOME"] = "Low_Income"
    df.loc[(df["AMT_INCOME_TOTAL"] > 112500) & (df["AMT_INCOME_TOTAL"]
                                                <= 225000), "NEW_SEGMENT_INCOME"] = "Middle_Income"
    df.loc[(df["AMT_INCOME_TOTAL"] > 225000),
           "NEW_SEGMENT_INCOME"] = "High_Income"

    ########################
    # One-Hot Encoding
    ########################
    df, cat_cols = one_hot_encoder(df, nan_as_category=False)

    # Dropping feature named index
    df.drop('index', axis=1, inplace=True)
    df.drop(['REGION_POPULATION_RELATIVE', 'DAYS_BIRTH',
             'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'CNT_FAM_MEMBERS',
             'REGION_RATING_CLIENT', 'WEEKDAY_APPR_PROCESS_START',
             'HOUR_APPR_PROCESS_START', 'NEW_WEEKDAY_APPR_PROCESS_START_SIN',
             'NEW_WEEKDAY_APPR_PROCESS_START_COS', 'NEW_HOUR_APPR_PROCESS_START_SIN',
             'NEW_HOUR_APPR_PROCESS_START_COS', 'NEW_REGION', 'NEW_DOCUMENT',
             'NEW_DAYS_BIRTH', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'DAYS_EMPLOYED',
             'OWN_CAR_AGE', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
             'APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG',
             'YEARS_BUILD_AVG', 'COMMONAREA_AVG', 'ELEVATORS_AVG', 'ENTRANCES_AVG',
             'FLOORSMAX_AVG', 'FLOORSMIN_AVG', 'LANDAREA_AVG',
             'LIVINGAPARTMENTS_AVG', 'LIVINGAREA_AVG', 'NONLIVINGAPARTMENTS_AVG',
             'NONLIVINGAREA_AVG', 'APARTMENTS_MODE', 'BASEMENTAREA_MODE',
             'YEARS_BEGINEXPLUATATION_MODE', 'YEARS_BUILD_MODE', 'COMMONAREA_MODE',
             'ELEVATORS_MODE', 'ENTRANCES_MODE', 'FLOORSMAX_MODE', 'FLOORSMIN_MODE',
             'LANDAREA_MODE', 'LIVINGAPARTMENTS_MODE', 'LIVINGAREA_MODE',
             'NONLIVINGAPARTMENTS_MODE', 'NONLIVINGAREA_MODE', 'APARTMENTS_MEDI',
             'BASEMENTAREA_MEDI', 'YEARS_BEGINEXPLUATATION_MEDI', 'YEARS_BUILD_MEDI',
             'COMMONAREA_MEDI', 'ELEVATORS_MEDI', 'ENTRANCES_MEDI', 'FLOORSMAX_MEDI',
             'FLOORSMIN_MEDI', 'LANDAREA_MEDI', 'LIVINGAPARTMENTS_MEDI',
             'LIVINGAREA_MEDI', 'NONLIVINGAPARTMENTS_MEDI', 'NONLIVINGAREA_MEDI',
             'TOTALAREA_MODE', 'DEF_30_CNT_SOCIAL_CIRCLE',
             'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE',
             'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY',
             'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON',
             'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_YEAR'
             ], axis=1, inplace=True)
    #del test_df
    gc.collect()
    # print(df.columns.tolist())
    return df
