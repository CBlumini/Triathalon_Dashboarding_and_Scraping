import pandas as pd

url = "https://raw.githubusercontent.com/CBlumini/Triathlon_Dashboarding_and_Scraping/main/data/Santa-Cruz-Sprint.csv"

df = pd.read_csv(url)
print(df.head())