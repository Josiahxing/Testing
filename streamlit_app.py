import streamlit as st
import pandas as pd
import numpy as np

def perform_lookup(df, lookup_column, lookup_value, return_columns):
    """Performs the lookup operation on the DataFrame.

    Args:
        df: The pandas DataFrame.
        lookup_column: The name of the column to search within.
        lookup_value: The value to search for.
        return_columns: A list of column names to return.

    Returns:
        A pandas DataFrame containing the matching rows with selected columns, or None if no match is found.
    """
    if lookup_column not in df.columns:
        st.error(f"Lookup column '{lookup_column}' not found in the uploaded file.")
        return None

    try:
      filtered_df = df[df[lookup_column].astype(str).str.lower() == str(lookup_value).lower()]
    except:
      st.error(f"The format of the lookup value or the lookup column is incorrect")
      return None

    if filtered_df.empty:
        st.warning("No matching rows found.")
        return None

    # Ensure return columns exist
    invalid_return_columns = [col for col in return_columns if col not in df.columns]
    if invalid_return_columns:
        st.error(f"The following selected columns to return are invalid: {', '.join(invalid_return_columns)}")
        return None

    return filtered_df[return_columns]

def main():
    st.title("Audit Lookup App")

    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("File successfully uploaded!")

            # User inputs
            lookup_value = st.text_input("Enter the lookup value:")
            lookup_column = st.selectbox("Select the lookup column:", df.columns)
            return_columns = st.multiselect("Select the columns to return:", df.columns)

            if st.button("Perform Lookup"):
                if not lookup_value:
                    st.error("Please enter a lookup value.")
                elif not return_columns:
                    st.error("Please select at least one column to return.")
                else:
                    results = perform_lookup(df, lookup_column, lookup_value, return_columns)
                    if results is not None:
                        st.dataframe(results)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
