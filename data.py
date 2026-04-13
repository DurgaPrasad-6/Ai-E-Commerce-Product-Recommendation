import pandas as pd
data={
    "customer_id":[1225,2155,1245,1225,1768,2155,6304,1225,9193,2155,9492,1245,6304,9193,9492,1768,2155,1768,1225,1245],
    "product_id":[1789,1895,2568,4658,6548,8523,8564,7412,6124,3214,4689,9874,2024,2506,2025,6544,2026,2015,2027,2023],
    "product_name":['lenvo  lapotp','realme mobile','hitachi AC','boat buds','realme earphones','home theatre jbl','projector jbl','pouches','pendrives sandisc','superwoc charger','lg tv','iq mobile','dell laptop','cam lens',
                      'iphone 16','charger cables','samsung tv','lg fridge','mivi soundbar','vivo phones'],
    "ratings":[4,3.8,4,3.9,4.2,4.5,4.3,3.5,4,3.7,4.4,4.1,4.6,3.8,4.8,3.5,4.2,4.5,4.3,3.9]
    }
df=pd.DataFrame(data)
print(df)
df.to_csv("dataset.csv")

