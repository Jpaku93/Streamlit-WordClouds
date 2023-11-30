import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import math


# Function to save a figure as an image file
def save_figure_as_image(fig, filename):
    fig.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

# upload csv file and read into dataframe
st.title("Word Clouds")
st.write("Drop the cluster csv in the app to generate word clouds")
st.write("optional: add summary column")
st.write("Make sure to pick the right columns to process")
st.write("")
st.write("Upload CSV file and read into dataframe")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # pick column in dataframe
    st.write("pick text and cluster columns to process") 

    text = st.selectbox('Choose text column', data.columns, index=len(data.columns)-2 )
    cluster = st.selectbox('Choose cluster column', data.columns, index= len(data.columns)-1)
    # summary is empty
    summary = st.selectbox('Choose summary column', data.columns, index=None)
    
    data[text] = data[text].astype(str)
    # preview dataframe
    st.write("data preview")
    st.write(data)

    if text and cluster:
        try:
            # Create a list to store figures
            figures = []

            # Get unique cluster IDs
            unique_clusters = data[cluster].unique()

            # Calculate the number of rows and columns for subplots
            num_clusters = len(unique_clusters)
            num_cols = 3
            num_rows = math.ceil(num_clusters / num_cols)

            # Iterate through clusters and generate word clouds
            for i, cluster_id in enumerate(unique_clusters):
                # Filter the data for the current cluster
                cluster_data = data[data[cluster] == cluster_id]

                # Combine text within the cluster
                text_cluster = ' '.join(cluster_data[text])

                # Generate a word cloud for the cluster's text
                wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text_cluster)

                # Plot the word cloud in the appropriate subplot
                fig, ax = plt.subplots(figsize=(20, 35))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                if summary:
                    ax.set_title(f'Cluster {cluster_id} - {cluster_data[summary].iloc[0]}')
                else:
                    ax.set_title(f'Cluster {cluster_id}')

                # Save the figure as an image file
                image_filename = f"cluster_{cluster_id}_wordcloud.png"
                save_figure_as_image(fig, image_filename)

                # Append the image filename to the list
                figures.append(image_filename)

            # Display the saved images with adjustable size
            for image_filename in figures:
                st.image(image_filename)
                
        except Exception as e:
            st.write(f"An error occurred: {str(e)}. Please pick correct columns to continue.")
