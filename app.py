import streamlit as st
import pandas as pd

# Define a function to transform the data
def transform_data(df, user_id):
    # Filter the data to only include the specified user ID
    user_data = df[df["User ID"] == user_id]
    
    # Calculate the duration for each row
    user_data["Duration"] = pd.to_datetime(user_data["Left (Local)"]) - pd.to_datetime(user_data["Joined (Local)"])
    
    # Find the minimum Joined (Local) and maximum Left (Local) for the user
    min_joined = user_data["Joined (Local)"].min()
    max_left = user_data["Left (Local)"].max()
    
    # Filter the user data to only include rows where the Joined (Local) is equal to the minimum and the Left (Local) is equal to the maximum
    user_duration = user_data[(user_data["Joined (Local)"] == min_joined) & (user_data["Left (Local)"] == max_left)]
    
    # Drop the Peer ID and Role columns, as they are the same for all rows in the user_duration dataframe
    user_duration = user_duration.drop(["Peer ID", "Role"], axis=1)
    
    # Return the transformed data
    return user_duration

# Define the Streamlit app
def app():
    st.title("Transform CSV data")
    
    # Allow the user to upload a CSV file
    file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if file is not None:
        # Load the CSV file into a Pandas dataframe
        df = pd.read_csv(file)
        
        # Allow the user to select a User ID
        user_id = st.selectbox("Select a User ID", df["User ID"].unique())
        
        # Transform the data for the selected User ID
        transformed_data = transform_data(df, user_id)
        
        # Display the transformed data in a table
        st.write(transformed_data)
        
        # Add a download button for the transformed data
        csv = transformed_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="transformed_data.csv">Download CSV file</a>'
        st.markdown(href, unsafe_allow_html=True)
