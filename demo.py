import pandas as pd

df = pd.read_csv(r"C:\Users\aldwin\OneDrive\Desktop\part 1\all_files\netflix_titles.csv")
df = df.copy()

def standard(data):
    info = data.info()
    shape = data.shape
    columns = data.columns
    return info, shape, columns
print(standard(df))

print(df.isna().sum())

df.fillna({
    "director": "No Director",
    "cast": "No Cast",
    "country": "No Country",
    "date_added": "No date",
    "rating": "block"
})

df = df.drop_duplicates()
df = df.drop("show_id", axis=1)

df = df.sort_values(by="release_year", ascending=False).reset_index()

print(df)