
import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(layout= 'wide', page_title= 'Fashion EDA',page_icon="🛍️")
# Add Title
st.title('Fashion Project')

# Another way using html
html_title = """<h1 style="color:white;text-align:center;"> Fashion Data Analysis </h1>"""
st.markdown(html_title, unsafe_allow_html=True)

# Add Image
st.image('https://as2.ftcdn.net/jpg/02/96/96/13/1000_F_296961342_hoyYSlbuXseQuyCUzZv9Rc0ZIFg7hrRE.webp.jpg')

# Read Data
df = pd.read_csv('cleaned_FashionDataset.csv')

page = st.sidebar.radio('Go To Page', ["🏠Home", "📊Univariate Analysis", "📈Mulivariate Dashboard", "📋Brand Fashion Report"])

if page == "🏠Home":

    # Dataframe
    st.title("🛍️ Fashion Project Dashboard")
    st.subheader('Dataset Overview')
    st.dataframe(df)
    # Data Description
    column_descriptions = {
    "Brand_Name": "The brand or manufacturer of the fashion product.",
    "Product_Details": "A textual description of the product, often including fabric, design, fit, and style information.",
    "Available_Sizes": "The range of sizes available for the product, listed as a comma-separated string.",
    "Main_Retail_Price": "The original (undiscounted) retail price of the product, in the local currency.",
    "Price_After_Discount": "The price after applying any discounts or offers .",
    "Discount_Rate": "The fraction of the discount applied to the original price (e.g., 0.5 means 50% off).",
    "Category": "The category of clothing, which includes gender and clothing style.",
    "Product_color": "The primary color of the product."}

    # Create a table for descriptions
    desc_df = pd.DataFrame(list(column_descriptions.items()), columns=["Column Name", "Description"])

    # Display table
    st.subheader("📝 Column Descriptions")
    st.table(desc_df)


elif page == "📊Univariate Analysis":

    html_title = """<h1 style="color:white;text-align:center;"> Univariate Analysis </h1>"""
    st.markdown(html_title, unsafe_allow_html=True)
    tab1 , tab2 , tab3 ,tab4 = st.tabs(['Categories' , 'Brands' , 'Sizes','Color'])    
    with tab1 :
      col1, col2 = st.columns(2)
      col1.metric("Total Categories",df["Category"].nunique())
      st.write("Category Names:", df["Category"].unique())
      col2.metric('Total Revenue after Discount', df["Price_After_Discount"].sum())
      df_Category_Name_Distribution=df["Category"].value_counts().reset_index()
      st.plotly_chart(px.bar(df_Category_Name_Distribution,x="Category",y="count",title="Category_Name_Distribution",color="Category"))
    with tab2 :
       col3, = st.columns(1)
       col3.metric('Total Brands', df["Brand_Name"].nunique())
       df_brand_dist = df["Brand_Name"].value_counts().reset_index()
       df_brand_dist.columns = ["Brand_Name", "count"]
       st.plotly_chart(px.bar(df_brand_dist,x="Brand_Name",y="count",title="Brand Distribution",color="Brand_Name"))

    with tab3 : 
        df_Available_Sizes_Distribution=df["Available_Sizes"].value_counts().reset_index().head(10)
        df_Available_Sizes_Distribution.columns = ["Sizes", "count"]
        st.plotly_chart(px.bar(df_Available_Sizes_Distribution,x="Sizes",y="count",title="Available_Sizes_Distribution",color="Sizes"))
    with tab4 :  
        df_Product_color_Distribution=df["Product_color"].value_counts().reset_index().head(10)
        df_Product_color_Distribution.columns = ["Color", "count"]
        st.plotly_chart(px.bar(df_Product_color_Distribution,x="count",y="Color",title="Color_Distribution",color="Color"))
elif page == "📈Mulivariate Dashboard":
    # Total Revenue for Each Category
    tab1 , tab2  = st.tabs(['Categories' , 'Brands']) 
    with tab1 :
       
         st.subheader('📈 What is the Total Revenue for Each Category')
         reven_per_cat = df.groupby('Category')['Price_After_Discount'].sum().sort_values(ascending=False).reset_index()
         st.plotly_chart(px.bar(data_frame= reven_per_cat, x= 'Category', y= 'Price_After_Discount',color="Category", labels= {'Category' : 'Product Category', 'Price_After_Discount' : 'Total Revenue for Each Cat'}))
         df5=df.groupby(["Category","Brand_Name"])["Brand_Name"].count().sort_values(ascending=False).reset_index(name='Product_Count')
         st.plotly_chart(px.treemap(df5,path=["Category","Brand_Name"],values="Product_Count",title="Category VS. Brand_Name"))
         df8=df.groupby(["Category","Discount_Rate"])["Discount_Rate"].count().sort_values(ascending=False).reset_index(name="Count")
         st.plotly_chart(px.treemap(df8,path=["Category","Discount_Rate"],values="Count",title="Distribution of Discount Rate by Category"))
         df9=df.groupby(["Category","Product_color"])["Product_color"].count().sort_values(ascending=False).reset_index(name="Count")
         Top_color_cat = (df9.groupby("Category").apply(lambda x: x.nlargest(10, "Count"))).reset_index(drop=True) ##Top 10 brands have purchases in each cat
         st.plotly_chart(px.treemap(Top_color_cat,path=["Category","Product_color"],values="Count",title="Top 10 Product_color by Category"))
         st.subheader('📈 Comparison between Main Retail Price and Price After Disount for Each Category')
         d11=df.groupby("Category")[["Main_Retail_Price","Price_After_Discount"]].sum().sort_values(by="Main_Retail_Price",ascending=False).reset_index()
         d11_melted = d11.melt(
         id_vars="Category",
         value_vars=["Main_Retail_Price", "Price_After_Discount"],
         var_name="Price_Type",
         value_name="Total_Price")
         st.plotly_chart(px.bar(d11_melted, x="Category", y="Total_Price", color="Price_Type", text_auto=True, barmode="group"))
         d12 = df.groupby(["Category", "Discount_Rate"])["Price_After_Discount"].sum().reset_index()
         idx_max = d12.groupby('Category')['Price_After_Discount'].idxmax()
         idx_min = d12.groupby('Category')['Price_After_Discount'].idxmin()
         d13 = pd.concat([d12.loc[idx_max], d12.loc[idx_min]])
         d13 = d13.sort_values(by=['Category', 'Price_After_Discount'], ascending=[True, False]).reset_index(drop=True)
         d13["Type"] = d13.groupby("Category")["Price_After_Discount"].transform(lambda x: ["High" if val == x.max() else "Low" for val in x])
         st.plotly_chart(px.bar(d13,x="Category",y="Discount_Rate",color="Type",text="Price_After_Discount",barmode="group"))


  
    
    
    with tab2 :
       # Top Brands by revenue
       st.subheader("🏙️Top 10 Brand_Name Revenue")
       Top_brands_rev = df.groupby('Brand_Name')['Price_After_Discount'].sum().sort_values(ascending=False).head(10).reset_index()
       st.plotly_chart(px.bar(Top_brands_rev, x='Brand_Name', y='Price_After_Discount',color="Brand_Name", title='Top 10 Brand_Name Revenue'))
       #worst Brands by revenue
       st.subheader("🏙️Worst 10 Brand_Name Revenue")
       worst_brands_rev = df.groupby('Brand_Name')['Price_After_Discount'].sum().sort_values(ascending=False).tail(10).reset_index()
       st.plotly_chart(px.bar(worst_brands_rev, x='Brand_Name', y='Price_After_Discount',color="Brand_Name",title='Top 10 Brand_Name Revenue'))   
    
elif page == '📋Brand Fashion Report':
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Global Filters")
    Brands_list = df["Brand_Name"].unique().tolist() + ['All Brands']
    category_list=df["Category"].unique().tolist() + ['All categories']
    color_list=df["Product_color"].unique().tolist() 
    selected_colors = st.sidebar.multiselect( "Product Color (optional)",options=color_list)  
    Brands_state = st.sidebar.selectbox('Brand',Brands_list)
    cat_state=st.sidebar.selectbox('Category',category_list)
    df_filtered = df.copy()
    if  Brands_state != 'All Brands' and cat_state != "All categories":
        df_filtered = df[(df["Brand_Name"] ==Brands_state) &(df["Category"]==cat_state)]
        
    elif Brands_state == 'All Brands' and cat_state=="All categories":
        df_filtered = df
    elif  Brands_state != 'All Brands' and cat_state=="All categories":
        st.write("Choose All Brands plz")
    if selected_colors :
        df_filtered = df_filtered[df_filtered["Product_color"].isin(selected_colors)]
    st.dataframe(df_filtered)
    reven_per_Brand = df_filtered.groupby(["Category",'Brand_Name'])['Price_After_Discount'].sum().sort_values(ascending= False).reset_index()
    st.subheader("🔥 Top Products by Brand")
    st.plotly_chart(px.bar(data_frame = reven_per_Brand, x = 'Brand_Name', y= 'Price_After_Discount', labels = {'Brand_Name' :'Brand Name','Price_After_Discount' : 'Total Revenue'}))    
    
