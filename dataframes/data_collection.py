import sys
import os

# Add the parent directory of fastAPI and data to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from fastapi_mentalhealth.models import Appointment, User  # Replace with your correct FastAPI models
from fastAPi.app.project.models import AppointmentModel, User

# Connect to the database and fetch appointments and user data
def fetch_appointments():
    try:
        # Set up the connection (replace with your actual database credentials)
        engine = create_engine("postgresql://postgres:remy2020@localhost:5432/fastapi_mentalhealth")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch 500,000 rows of appointment data (adjust query as needed)
        appointments = session.query(AppointmentModel).limit(500000).all()  # Adjust limit if necessary
        users = session.query(User).all()

        # Convert query results into pandas DataFrame
        appointments_df = pd.DataFrame([a.to_dict() for a in appointments])  # Assuming a `to_dict()` method in your model
        users_df = pd.DataFrame([u.to_dict() for u in users])

        return appointments_df, users_df
    except Exception as e:
        print(f"Error fetching data from the database: {e}")
        return None, None

# Process the data by merging, cleaning, and preprocessing
def process_data():
    try:
        # Fetch data from the database
        appointments_df, users_df = fetch_appointments()

        if appointments_df is None or users_df is None:
            print("Data fetch failed!")
            return

        # Merging the DataFrames on 'user_id' (change 'user_id' as needed)
        merged_df = pd.merge(appointments_df, users_df, left_on="user_id", right_on="id", how="inner")

        # Perform data cleaning (handle missing values)
        print("Before cleaning:")
        print(merged_df.isnull().sum())
        
        # Forward fill and backward fill missing values
        merged_df.ffill(inplace=True)
        merged_df.bfill(inplace=True)

        print("After cleaning:")
        print(merged_df.isnull().sum())

        # Convert 'created_at' or any other datetime columns if needed
        if 'created_at' in merged_df.columns:
            merged_df['created_at'] = pd.to_datetime(merged_df['created_at'])
            print(f"Data types after conversion: {merged_df.dtypes}")

        # Optionally, save the processed data to CSV (or another format)
        merged_df.to_csv("processed_appointments_data.csv", index=False)

        print(f"Shape of the merged dataframe: {merged_df.shape}")
        return merged_df

    except Exception as e:
        print(f"Error processing data: {e}")

# Example call to process the data
if __name__ == "__main__":
    processed_data = process_data()
    if processed_data is not None:
        print("Data processing complete.")
    else:
        print("Data processing failed.")
