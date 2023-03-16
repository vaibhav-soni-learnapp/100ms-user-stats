import pandas as pd
import streamlit as st

# Define function to extract relevant data for a given user ID
def extract_user_data(df, user_id):
    user_data = df[df['User ID'] == user_id].copy()
    if len(user_data) > 0:
        user_data['Joined (Local)'] = pd.to_datetime(user_data['Joined (Local)'])
        user_data['Left (Local)'] = pd.to_datetime(user_data['Left (Local)'])
        duration = (user_data['Joined (Local)'].min() - user_data['Left (Local)'].max()).total_seconds()
        user_data = user_data[['Name', 'Role', 'User ID', 'Duration', 'Joined (Local)', 'Left (Local)']].iloc[0]
        user_data['Duration'] = duration
        return user_data
    else:
        return None

# Define Streamlit app
def main():
    # Set page title
    st.set_page_config(page_title='User Data Extractor')

    # Add file upload widget to sidebar
    uploaded_file = st.sidebar.file_uploader('Upload a CSV file', type='csv')

    # If file is uploaded, read it into a DataFrame
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Add user ID selection widget to sidebar
        user_id = st.sidebar.selectbox('Select a User ID', df['User ID'].unique())

        # If user ID is selected, extract relevant data and display in table format
        if user_id:
            user_data = extract_user_data(df, user_id)
            if user_data is not None:
                st.write('User Data for User ID:', user_id)
                st.write(user_data)
                st.download_button('Download User Data as CSV', pd.DataFrame(user_data).T.to_csv(), file_name=f'user_{user_id}.csv', mime='text/csv')
            else:
                st.write('No data found for User ID:', user_id)

# Run the app
if __name__ == '__main__':
    main()
