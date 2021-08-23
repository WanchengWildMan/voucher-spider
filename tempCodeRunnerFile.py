    df_imp = df_all_info[
        ["城市", "省份", "2019年gdp", "城市经济分级_2019年gdp", "人口", "lon", "lat"] + ["money_digit", "发放方式0领取1摇号2抢券", "领取方式", "发放时间", "发放金额", "领取数量", "领取规则", "url"]].fillna(value="")
    df_imp = df_imp.rename(columns={"城市": "city", "省份": "province", "2019年gdp": "gdp19", "城市经济分级_2019年gdp": "gdpStage19", "人口": "peo", "发放方式0领取1摇号2抢券": "giveOutMethod",
                                    "领取方式": "methodDescribe", "发放时间": "giveTimeDescribe", "发放金额": "moneyDescribe", "领取数量": "numDescribe", "领取规则": "ruleDescribe", "url": "url", "money_digit": "moneyDigit"})
    df_imp["giveOutMethod"] = df_imp["giveOutMethod"].map(
        {0: "领取", 1: "摇号", 2: "抢券"})