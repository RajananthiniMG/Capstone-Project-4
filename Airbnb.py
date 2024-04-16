import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# Streamlit Part

st.set_page_config(
    page_title="Airbnb Analysis",
    page_icon=":bar_chart:",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app! Where you can Analysis Airbnb data"
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

    st.markdown(
    """
    This app allows you to explore and analyze Airbnb data. Upload your own dataset or use the default one provided. 
    You can filter the data by neighborhood and room type, visualize price distributions, and view geospatial information.

    ### How to Use:
    1. **Explore Data**: Upload your dataset or use the default one to explore Airbnb listings.
    2. **Filter Data**: Use the sidebar to filter the data by neighborhood and room type.
    3. **Visualize Data**: See price distributions, room type summaries, and geospatial information.
    4. **Download Data**: Download the filtered or original dataset for further analysis.

    [Need Help?](https://www.extremelycoolapp.com/help) | [Report a Bug](https://www.extremelycoolapp.com/bug)
    """
    )

if menu == "Explore Data":
     with st.container(border=True):

        upload_file = st.file_uploader("Upload a File:", type=["csv","txt","xlsx","xls"]) #here we uploading the image to extract text from i
            
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
             filtered_df = df
        elif not Neighbourhood:
           filtered_df = df[df["Neighbourhood_group"].isin(Neighbourhood_group)]
        elif not Neighbourhood_group:
             filtered_df = df[df["Neighbourhood"].isin(Neighbourhood)]
        elif Neighbourhood:
            filtered_df = df3[df["Neighbourhood"].isin(Neighbourhood)]
        elif Neighbourhood_group:
            filtered_df = df3[df["Neighbourhood_group"].isin(Neighbourhood_group)]
        elif Neighbourhood_group and Neighbourhood:
             filtered_df = df3[df["Neighbourhood_group"].isin(Neighbourhood_group) & df3["Neighbourhood"].isin(Neighbourhood)]
        else:
             filtered_df = df3[df3["Neighbourhood_group"].isin(Neighbourhood_group) & df3["Neighbourhood"].isin(Neighbourhood)]

        room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

        col1, col2 = st.columns(2)
        with col1:
           fig = px.scatter(room_type_df, x="room_type", y="price", 
              color="room_type",  # Use room type for color differentiation
              color_discrete_sequence=px.colors.qualitative.Set3,  # Specify color palette
              title='Room Type Prices',
              labels={'price': 'Price', 'room_type': 'Room Type'},
              symbol="room_type",  # Use different symbols for each room type
              size="price",        # Use price values to determine marker sizes
              hover_name="room_type")  # Display room type on hover)

            # Customize layout
           fig.update_layout(xaxis_title='Room Type', 
                  yaxis_title='Price',
                  title='Room Type Prices Variation',
                  legend_title='Room Type')

            # Show the plot
           st.plotly_chart(fig, use_container_width=True)

        with col2:
           fig = px.bar(filtered_df, y="Neighbourhood_group", x="price", 
                 orientation='h', 
                 labels={'price': 'Price', 'Neighbourhood_group': 'Neighbourhood Group'},
                 color='Neighbourhood_group',  # Specify color based on neighborhood group
                 color_discrete_sequence=px.colors.qualitative.Dark24,  # Choose a different color scheme
                 title='Distribution of Prices Across Neighbourhood Groups')

            # Customize layout
           fig.update_layout(yaxis={'categoryorder': 'total ascending'},  # Sort by total price
                            xaxis_title='Price', 
                            yaxis_title='Neighbourhood Group',
                            bargap=0.20)

            # Show the plot
           st.plotly_chart(fig, use_container_width=True)


        with st.expander("Room_type and Neighbourhood_group wise price"):
            col1, col2 = st.columns(2)

            with col1:
                # Room_type wise price
                with st.container():
                    st.subheader("Room_type wise price")
                    st.write(room_type_df.style.background_gradient(cmap="Blues"))
                    csv_room_type = room_type_df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Room_type Data", data=csv_room_type, file_name="room_type.csv", mime="text/csv",
                                    help='Click here to download the Room_type data as a CSV file')
                
            with col2:
                # Neighbourhood_group wise price
                with st.container():
                    st.subheader("Neighbourhood_group wise price")
                    Neighbourhood_group = filtered_df.groupby(by="Neighbourhood_group", as_index=False)["price"].sum()
                    st.write(Neighbourhood_group.style.background_gradient(cmap="Oranges"))
                    csv_neighbourhood_group = Neighbourhood_group.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Neighbourhood_group Data", data=csv_neighbourhood_group, file_name="Neighbourhood_group.csv", mime="text/csv",
                                    help='Click here to download the Neighbourhood_group data as a CSV file')
        
     # Create a treemap
        fig = px.treemap(filtered_df, path=['Neighbourhood_group', 'Neighbourhood', 'room_type'], values='price',
                        title='Room Type Distribution Across Neighbourhoods and Neighbourhood Groups')

        # Customize layout
        fig.update_layout(title='Room Type Distribution Across Neighbourhoods and Neighbourhood Groups')

        # Show the plot
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
            st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

        # Download orginal DataSet
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

        import plotly.figure_factory as ff

        st.subheader(":point_right: Neighbourhood_group wise Room_type and Price")
        with st.expander("Summary_Table"):
            df_sample = df[0:5][["Neighbourhood_group", "Neighbourhood",  "room_type", "price",  "host_name"]]
            fig = ff.create_table(df_sample, colorscale="Cividis")
            st.plotly_chart(fig, use_container_width=True)
 

        # Display the map
        st.subheader('Geospatial Visualization')
        st.map(data=df, latitude='latitude', longitude='longitude', color=None, size=100, zoom=None, use_container_width=True)
                


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