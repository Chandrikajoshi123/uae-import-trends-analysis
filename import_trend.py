import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import sqlite3
import os
file_path='/Users/chandrikajoshi/Downloads/ImportsbyChapter(HS)2008-2016.xlsx'
print(file_path)
xls = pd.ExcelFile(file_path)
print(xls.sheet_names)
df = pd.read_excel(file_path)

conn = sqlite3.connect('imports_data.db')
# Save data into the database
df.to_sql('imports', conn, if_exists='replace', index=False)
# Close the connection
conn.close()
print("🎉 New database created successfully!")



# --- Load data using cache ---
@st.cache_data
def load_data():
    conn = sqlite3.connect('imports_data.db')
    df = pd.read_sql_query("SELECT * FROM imports", conn)
    conn.close()
    return df

# Load data
df = load_data()

# --- Streamlit UI ---
st.title("📦 UAE Import Trends Analysis (2008-2016)")
st.markdown("Welcome to the visual analysis of UAE's top imported products! 🌟")
with st.expander("🔍 View Dataset"):
    st.dataframe(df)

# Plot Top 10 Imported Product Categories
st.subheader("📈 Top 10 Imported Product Categories (2008-2016)")
top_imports = df.groupby('description_EN')['number'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_imports.values, y=top_imports.index, palette="viridis", ax=ax)
ax.set_xlabel('Total Import Value (AED)')
ax.set_ylabel('Product Category')
ax.set_title('Top 10 Imported Categories (2008-2016)')
st.pyplot(fig)

st.bar_chart(top_imports)
st.bar_chart(df['number'])

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.header(":)")
sidebar_option = st.sidebar.selectbox("Options", ["Home", "View Dataset","Conclusion"])
