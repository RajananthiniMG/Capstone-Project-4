import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Streamlit Part

st.set_page_config(
    page_title="Airbnb Analysis",
    page_icon=":bar_chart:",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Welcome to Airbnb Analysis\n\n#### About Airbnb:\n[Airbnb](https://www.airbnb.com/) is a popular online marketplace that connects travelers with hosts who offer lodging accommodations. Founded in 2008, Airbnb has transformed the way people travel by providing a platform for individuals to rent out their homes, apartments, or rooms to guests for short-term stays.\n\n#### Airbnb Analysis App:\nThis app allows you to explore and analyze Airbnb data from various locations. Whether you're a traveler looking for insights into accommodation prices or a host seeking to understand market trends, this app provides you with tools to dive deep into Airbnb listings.\n\n### Features:\n- **Explore Data**: Upload your dataset or use the default one provided to explore Airbnb listings.\n- **Filter Data**: Use the sidebar to filter the data by neighborhood and room type.\n- **Visualize Data**: See price distributions, room type summaries, and geospatial information through interactive visualizations.\n- **Download Data**: Download the filtered or original dataset for further analysis.\n\n#### How to Use:\n1. **Explore Data**: Click on \"Explore Data\" in the menu to start analyzing Airbnb listings.\n2. **Filter Data**: Use the sidebar to filter listings based on your preferences.\n3. **Visualize Data**: Interact with the visualizations to gain insights into Airbnb data.\n4. **Download Data**: Download the filtered or original dataset for your analysis needs.\n\n#### Need Help or Found a Bug?\nIf you need assistance or encounter any issues while using the app, feel free to reach out to us:\n- [Get Help](https://www.extremelycoolapp.com/help)\n- [Report a Bug](https://www.extremelycoolapp.com/bug)"
    }
)
st.title('Airbnb Analysis',)

#[theme]
primaryColor="#d8ecbb"
backgroundColor="#e6ffdc"
secondaryBackgroundColor="#6fa659"
textColor="#083b10"


menu = option_menu(None,["Home","Explore Data","Contact"],
        icons=['house', 'bar-chart-line-fill','chat-left-text'], 
        menu_icon="cast",
        default_index=0, 
        orientation="horizontal")

if menu == "Home":
    st.title('Welcome to Airbnb Analysis')

    st.image(r"C:\Users\rajan\OneDrive\Desktop\AirbnbAnalysis\airbnb.png", use_column_width=True)  

    st.write(
    """
    ### About Airbnb:
    Airbnb is a popular online marketplace that connects travelers with hosts who offer lodging accommodations. Founded in 2008, Airbnb has transformed the way people travel by providing a platform for individuals to rent out their homes, apartments, or rooms to guests for short-term stays.

    ### Airbnb Analysis App:
    This app allows you to explore and analyze Airbnb data from various locations. Whether you're a traveler looking for insights into accommodation prices or a host seeking to understand market trends, this app provides you with tools to dive deep into Airbnb listings.

    ### Key Features:
    - **Explore Data**: Upload your dataset or use the default one provided to explore Airbnb listings.
    - **Filter Data**: Use the sidebar to filter the data by neighborhood and room type.
    - **Visualize Data**: See price distributions, room type summaries, and geospatial information through interactive visualizations.
    - **Download Data**: Download the filtered or original dataset for further analysis.
    """
    )

    st.subheader('How to Use:')
    st.write(
    """
    1. Click on "Explore Data" in the menu to start analyzing Airbnb listings.
    2. Use the sidebar to filter listings based on your preferences.
    3. Interact with the visualizations to gain insights into Airbnb data.
    4. Download the filtered or original dataset for your analysis needs.
    """
    )

    st.subheader('Need Help or Found a Bug?')
    st.write(
    """
    If you need assistance or encounter any issues while using the app, feel free to reach out to us:
    - [Get Help](https://www.extremelycoolapp.com/help)
    - [Report a Bug](https://www.extremelycoolapp.com/bug)
    """
    )

if menu == "Explore Data":
     with st.container(border=True):

        upload_file = st.file_uploader("Upload a File:", type=["csv","txt","xlsx","xls"]) #here we uploading the data file to Analysis and vizualise those data in various format
        if upload_file is not None:
            df = pd.read_csv(upload_file)
            df.fillna(value='NA', inplace=True)
            df.drop_duplicates(inplace=True)
        else:
            df = pd.read_csv("airbnb.listingsAndReviews.csv")
            df.fillna(value='NA', inplace=True)
            df.drop_duplicates(inplace=True)
            

        st.sidebar.header("Choose your filter: ")  

        Neighbourhood_group = st.sidebar.multiselect("Pick your Neighbourhood_group", df["Neighbourhood_group"].unique())
        if not Neighbourhood_group:
            df2 = df.copy()
        else:
             df2 = df[df["Neighbourhood_group"].isin(Neighbourhood_group)]

        # Create for Neighbourhood
        Neighbourhood = st.sidebar.multiselect("Pick the Neighbourhood", df2["Neighbourhood"].unique())
        if not Neighbourhood:
           df3 = df2.copy()
        else:
          df3 = df2[df2["Neighbourhood"].isin(Neighbourhood)]

        if not Neighbourhood_group and not Neighbourhood:
             filtered_df_data = df
        elif not Neighbourhood:
           filtered_df_data = df[df["Neighbourhood_group"].isin(Neighbourhood_group)]
        elif not Neighbourhood_group:
             filtered_df_data = df[df["Neighbourhood"].isin(Neighbourhood)]
        elif Neighbourhood:
            filtered_df_data = df3[df["Neighbourhood"].isin(Neighbourhood)]
        elif Neighbourhood_group:
            filtered_df_data = df3[df["Neighbourhood_group"].isin(Neighbourhood_group)]
        elif Neighbourhood_group and Neighbourhood:
             filtered_df_data = df3[df["Neighbourhood_group"].isin(Neighbourhood_group) & df3["Neighbourhood"].isin(Neighbourhood)]
        else:
             filtered_df_data = df3[df3["Neighbourhood_group"].isin(Neighbourhood_group) & df3["Neighbourhood"].isin(Neighbourhood)]

        room_type_df = filtered_df_data.groupby(by=["room_type"], as_index=False)["price"].sum()

        col1, col2 = st.columns(2)
        with col1:
              fig = px.scatter(room_type_df, x="room_type", y="price", color="room_type", color_discrete_sequence=px.colors.qualitative.Set3,  
                    title='Room Type Prices', labels={'price': 'Price', 'room_type': 'Room Type'},symbol="room_type", size="price",        
                    hover_name="room_type") 
              
             # Customize layout
              fig.update_layout(xaxis_title='Room Type', 
                    yaxis_title='Price',
                    title='Room Type Prices Variation',
                    legend_title='Room Type')

             # Show the plot
              st.plotly_chart(fig, use_container_width=True)


        with col2:            
            fig = px.sunburst(filtered_df_data, 
                    path=['Neighbourhood_group'], 
                    values='price',
                    title='Room Type Distribution Across Neighbourhoods and Neighbourhood Groups')

            # Customize layout
            fig.update_layout(title='Room Type Distribution Across Neighbourhoods and Neighbourhood Groups')

            # Show the plot
            st.plotly_chart(fig,use_container_width=True)

     with st.expander("Room_type and Neighbourhood_group wise price"):
            col1, col2 = st.columns(2)

            with col1:
                # Room_type wise price
                st.subheader("Room_type wise price")
                st.write(room_type_df.style.background_gradient(cmap="Blues"))
                room_type_data_csv = room_type_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Room_type Data", data=room_type_data_csv, file_name="room_type.csv", mime="text/csv",
                                help='Click here to download the Room_type data as a CSV file')
            
            with col2:
                # Neighbourhood_group wise price
                st.subheader("Neighbourhood_group wise price")
                Neighbourhood_group = filtered_df_data.groupby(by="Neighbourhood_group", as_index=False)["price"].sum()
                st.write(Neighbourhood_group.style.background_gradient(cmap="Greens"))
                neighbourhood_group_data_csv = Neighbourhood_group.to_csv(index=False).encode('utf-8')
                st.download_button("Download Neighbourhood_group Data", data= neighbourhood_group_data_csv, file_name="Neighbourhood_group.csv", mime="text/csv",
                                help='Click here to download the Neighbourhood_group data as a CSV file')
            
     with st.container(border=True):
        fig = px.bar(filtered_df_data, x='Neighbourhood_group', y='price', color='Neighbourhood', facet_col='room_type',
                    barmode='group', title='Room Type Distribution Across Neighbourhoods and Neighbourhood Groups',hover_data=['Neighbourhood_group', 'Neighbourhood', 'price'],
                    labels={'Neighbourhood_group': 'Neighbourhood Group', 'Neighbourhood': 'Neighbourhood', 'price': 'Price'})

        # Customize layout
        fig.update_layout(xaxis_title='Neighbourhood Group', 
                        yaxis_title='Price',
                        title='Room Type Distribution Across Neighbourhoods and Neighbourhood Groups')

        # Show the plot
        st.plotly_chart(fig, use_container_width=True)


     with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
            st.write(filtered_df_data.iloc[:500, 1:15:2].style.background_gradient(cmap="Oranges"))

                # Download orginal DataSet
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

     st.subheader(":point_right: Neighbourhood_group wise Room_type and Price")
     with st.expander("Summary_Table"):
            df_sample = df[0:5][["Neighbourhood", "room_type", "name","price","host_name","cancellation_policy","minimum_nights"]]
            fig = ff.create_table(df_sample, colorscale="Cividis")
            for i in range(len(fig.layout.annotations)):
                fig.layout.annotations[i].font.size = 11 
                fig.layout.annotations[i].width =1500

            st.plotly_chart(fig, use_container_width=True)

    # Display the map
     st.subheader('Geospatial Visualization')
     fig = go.Figure(go.Scattermapbox(
            lat=df['latitude'],  
            lon=df['longitude'],  
            mode='markers+text',  
            marker={'size': 10, 'color': 'blue'},  
            text=df['Neighbourhood'], 
            textposition='top left',  
            textfont=dict(size=12, color='black')
        ))

        # Update map layout
     fig.update_layout(
            mapbox_style="carto-positron",  
            mapbox_center={"lat": df['latitude'].mean(), "lon": df['longitude'].mean()}, 
            margin={"r":0,"t":0,"l":0,"b":0}, 
        )

        # Show the map
     st.plotly_chart(fig, use_container_width=True)

     st.image(r"C:\Users\rajan\OneDrive\Desktop\AirbnbAnalysis\powerbi Report.png", caption="Power BI Report")
                


if menu == "Contact":
    st.title('Contact Information')

    st.write("Mail id : mgrajananthini@gmail.com")
    st.write("Name: M G Rajananthini")

    st.subheader('Project Achievements:')
    st.write("- Analyzed Airbnb data to provide insights into price distribution, room type summaries, and geographical visualization.")
    st.write("- Implemented data filtering by neighborhood and room type.")
    st.write("- Visualized data using various plots such as scatter plots, bar charts, and treemaps.")
    st.write("- Provided downloadable CSV files for filtered and original datasets.")

    st.subheader('Connect with Me:')

    col1, col2 = st.columns(2)
    with col1:
        st.write("- [LinkedIn](www.linkedin.com/in/rajananthini-m-g-b2285b207)")

    with col2:    
        st.write("- [GitHub](https://github.com/RajananthiniMG/RajananthiniMG.git)")
