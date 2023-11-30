# create word clouds from clustered data
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import math

# upload csv file and read into dataframe
st.title("Word Clouds")
st.write("Drop the cluster csv in the app to generate wordclouds")
st.write("optional: add summary column")
st.write("Make sure to pick the write columns to process")
st.write("")
st.write("upload csv file and read into dataframe")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # pick column in dataframe
    st.write("pick text and cluster columns to process") 
    text = st.selectbox('Choose text column', data.columns, index=3)
    cluster = st.selectbox('Choose cluster column', data.columns, index=5)
    # summary is empty
    summary = st.selectbox('Choose summary column', data.columns , index = None)
    
    data[text] = data[text].astype(str)
    # preview dataframe
    st.write("data preview")
    st.write(data.head())

    if text != None:
        if cluster != None:
            try:
                # Create a list to store figures
                figures = []

                # Get unique cluster IDs
                unique_clusters = data[cluster].unique()

                # Calculate the number of rows and columns for subplots
                num_clusters = len(unique_clusters)
                num_cols = 3
                num_rows = math.ceil(num_clusters / num_cols)

                # Create subplots
                fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

                # Iterate through clusters and generate word clouds
                for i, cluster_id in enumerate(unique_clusters):
                    # Filter the data for the current cluster
                    cluster_data = data[data[cluster] == cluster_id]

                    # Combine text within the cluster
                    text_cluster = ' '.join(cluster_data[text])

                    # Generate a word cloud for the cluster's text
                    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text_cluster)

                    # Plot the word cloud in the appropriate subplot
                    row_idx = i // num_cols
                    col_idx = i % num_cols
                    ax = axes[row_idx, col_idx]
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    if summary != None:
                        ax.set_title(f'Cluster {cluster_id} - {cluster_data[summary].iloc[0]}')
                    else:
                        ax.set_title(f'Cluster {cluster_id}')

                # Remove any empty subplots
                for i in range(num_clusters, num_rows * num_cols):
                    fig.delaxes(axes.flatten()[i])

                # Adjust layout
                plt.tight_layout()

                # Append the figure to the list
                figures.append(fig)

                # Display the figures using st.pyplot()
                for fig in figures:
  
                    st.pyplot(fig)
            except:
                st.write("Pick the text column and cluster column to process")
