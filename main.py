import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Data loading 
df=pd.read_csv("netflix.csv")
print("="*50)
print("Netflix analysis")
print("="*50)
print(df.head())
print(df.tail())
print("\nDataset shape:")
print(df.shape)
print("\nDataset information:")
print(df.info())

#DATA CLEANING 
df['Show_ID']=df['Show_ID'].fillna(df["Show_ID"].mode()[0])
print("\nmissing values  in show_ID after inputation")

df['Type']=df['Type'].fillna(df["Type"].mode() [0])
print("\nmissing values in Type after inputation")

df['Title']=df['Title'].fillna(df["Type"].mode()[0])
print("\nmissing values in  Title after inputation")

df['Director']=df['Director'].fillna("unknown")
print("\nmissing values in Director after inputation")

df['Cast']=df['Cast'].fillna(df["Cast"].mode()[0])
print("\nmissing values in  Cast after inputation")

df['Country']=df['Country'].fillna(df["Country"].mode()[0])
print("\nmissing values in  Country after inputation")

df['Release_Year']=df['Release_Year'].fillna(df["Release_Year"].mean())
print("\nmissing values in  Release_Year  after inputation")

df['Rating']=df['Rating'].fillna(df["Rating"].mode()[0])
print("\nmissing values in Rating after inputation")

df['Duration']=df['Duration'].fillna(df["Duration"].mode()[0])
print("\nmissing values in Duration after inputation")

df['Description']=df['Description'].fillna(df["Description"].mode()[0])
print("\nmissing values in Description after inputation")

df=df.drop_duplicates()
print("\nDataset shape after removing duplicates")

df["Director"]=df["Director"].str.title()

df["Country"]=df["Country"].str.strip()

df["Type"]=df["Type"].str.title()

df["Duration"]=df["Duration"].str.replace("min"," min",regex=False)
df["Duration"]=df["Duration"].str.replace(" " , " ")

df["Country"]=df["Country"].str.title()

df["Date_Added"]=df["Date_Added"].str.strip()
df["Date_Added"]=pd.to_datetime(df["Date_Added"],errors="coerce")   #error=coerce--- means if pandas find incorrect date it give NaT(not a time) instead of error
df["Date_Added"]=df["Date_Added"].dt.strftime("%Y-%m-%d")  #dt--a datetime coulm ,strftime--string format time
df["Date_Added"]=df["Date_Added"].fillna("unknown")
print(df.isnull().sum())  #isnull is used to detect missing values 

df.to_csv("output/cleaned netflix.csv",index=False) 


#Exploratory Data Analysis
#total no.of netflix titles
print("Total number of netflix titles:",len(df))

print("Total number of Tv shows and movies:",df["Type"].value_counts())

#oldest and newest release year
print(df["Release_Year"].min())

print(df["Release_Year"].max())

#Find the average release year
print("Average release year:", df["Release_Year"].mean())

#Count content by rating
print("count content by rating:",df["Rating"].value_counts())

#Find the top 10 most common genres.
top_10=df["Genre (Listed_In)"].value_counts().head(10)
print(top_10)

#Find the top 10 countries with the most Netflix content.
top_10=df["Country"].value_counts().head(10)
print(top_10)

#Find the top 10 directors with the highest number of titles.
top_10=df["Director"].value_counts().head(10)
print(top_10)

#Find the year with the highest number of releases.
print("Highest releases:",df["Release_Year"].max())

#Find the month in which Netflix added the most content
df["Date_Added"]=df["Date_Added"].replace("Unknown",pd.NA)
df["Date_Added"]=pd.to_datetime(df["Date_Added"],errors="coerce") 
month_count=df["Date_Added"].dt.month_name().value_counts()
print(month_count.idxmax())
print(month_count.max())

#Find all Movies released after 2020.
movies_after_2020 = df[df["Release_Year"] > 2020]
print( "Number of movies released after 2020:", len(movies_after_2020))

#Find all TV Shows with more than 3 seasons.
tv_shows_with_3_seasons = df[(df["Type"] == "TV Show") & (df["Duration"].str.contains("min"))]
print("Number of TV shows with more than 3 seasons:", len(tv_shows_with_3_seasons))

#Find content released in India.
Indian_content=df[df["Country"]=="India"]
print("Number of content released in india:",len(Indian_content))

#Find content directed by a specific director.
director_content=df[df["Director"]=="Specific Director"]
print("Number of content directed by Specific Director:",len(director_content))

#Find titles containing the word Love.
love_titles=df[df["Title"].str.contains("Love",case=False)]
print("Number of titles containing love:", len(love_titles))

#Count Movies and TV Shows year-wise.
yearly_counts=df.groupby(["Release_Year","Type"]).size()
print("Year-wise count of movies and  TV shows:",yearly_counts)

#Find the most common content rating.
print("Most common content rating:",df["Rating"].mode()[0])   #mode()[0] is used to get the  most common value in the column

#Find the longest movie.
longest_movie=df[df["Duration"]==df["Duration"].max()]
print("Longest movie is:", longest_movie["Title"].iloc[0])

#Find the shoretest movie
shortest_movie=df[df["Duration"]==df["Duration"].min()]
print("Shortest movie is:", shortest_movie["Title"].iloc[0])

#Find the top 10 latest releases.
top_10_latest_releases=df.sort_index(ascending=False).head(10)
print("Top 10 latest releases:",top_10_latest_releases["Title"].tolist())

#Find the oldest 10 titles
oldest_10_titles=df.sort_index(ascending=True).head(10)
print("Top 10 oldest titles:",oldest_10_titles["Title"].tolist())

#Find genre-wise content count.
genre_counts=df["Genre (Listed_In)"].value_counts()
print("Genre-wise content count:",genre_counts)

#Find country-wise average release year.
country_avg_release_year=df.groupby("Country")["Release_Year"].mean()
print("Country wise average release year:",country_avg_release_year)

#VISULAIZATION
#create a Pie Chart showing Movies vs TV Shows.
type_counts=df["Type"].value_counts()
plt.figure(figsize=(6,6))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%')
plt.title('Distribution of Movies vs TV Shows')
plt.show()

#Create a Bar Chart for the Top 10 Genres.
top_10_genres=df["Genre (Listed_In)"].value_counts().head(10)
plt.figure(figsize=(10,6))
plt.bar(top_10_genres.index, top_10_genres.values)
plt.title('Top 10 Genres')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Create a Bar Chart for the Top 10 Countries.
top_10_countries=df["Country"].value_counts().head(10)
plt.figure(figsize=(10,6))
plt.bar(top_10_countries.index, top_10_countries.values)
plt.title('Top 10 Countries')
plt.xlabel('Country')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Create a Histogram for Release Year Distribution.
plt.figure(figsize=(10,6))
plt.hist(df["Release_Year"],bins=20,edgecolor='black')
plt.title("Release year Distribution")
plt.xlabel("Release_Year")
plt.ylabel("Count")
plt.show()

#Create a Count Plot for Content Ratings.
plt.figure(figsize=(10,6))
sns.countplot(data=df,x="Rating",order=df["Rating"].value_counts().index)
plt.title("Content Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

#Create a Horizontal Bar Chart for the Top 10 Directors.
top_10_directors=df["Director"].value_counts().head(10)
plt.figure(figsize=(10,6))
plt.barh(top_10_directors.index,top_10_directors.values)
plt.title("Top 10 Directors")
plt.xlabel("Count")
plt.ylabel("Director")
plt.show()

#Create a Line Chart showing Releases by Year.
plt.figure(figsize=(10,6))
yearly_counts=df.groupby("Release_Year").size()
plt.plot(yearly_counts.index, yearly_counts.values)
plt.title("Releases by Year")
plt.xlabel("Release Year")
plt.ylabel("Count")
plt.show()

#43.Create a Box Plot for Movie Duration.
plt.figure(figsize=(10,6))
sns.boxplot(data=df[df["Type"]=="Movie"],x="Duration")
plt.title("Distribution of Movie Duration")
plt.xlabel("Duration")
plt.show()

#Create a Heatmap of correlations between numerical features.
plot_data=df.select_dtypes(include=[np.number])
plt.figure(figsize=(10,6))
sns.heatmap(plot_data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap between Numerical features")
plt.show()

#Create a Dashboard containing at least six visualizations.
plt.figure(figsize=(18,10))

# 1. Movies vs TV Shows
plt.subplot(2,3,1)
df["Type"].value_counts().plot(kind="bar")
plt.title("Movies vs TV Shows")

# 2. Top 5 Countries
plt.subplot(2,3,2)
df["Country"].value_counts().head(5).plot(kind="bar")
plt.title("Top 5 Countries")

# 3. Top 5 Genres
plt.subplot(2,3,3)
df["Genre (Listed_In)"].value_counts().head(5).plot(kind="bar")
plt.title("Top 5 Genres")
plt.xticks(rotation=45, ha="right")

# 4. Content Ratings
plt.subplot(2,3,4)
df["Rating"].value_counts().plot(kind="bar")
plt.title("Content Ratings")
plt.xticks(rotation=45)

# 5. Releases by Year
plt.subplot(2,3,5)
df["Release_Year"].value_counts().sort_index().plot(kind="line", marker="o")
plt.title("Releases by Year")

# 6. Top 10 Directors
plt.subplot(2,3,6)
df["Director"].value_counts().head(10).plot(kind="barh")
plt.title("Top 10 Directors")

plt.tight_layout(pad=3)
plt.show()


