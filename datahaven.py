import streamlit as st
import pandas as pd

# App title
st.title("DataHaven - Your Safe Haven for Clean Data")
st.write("Upload your Excel or CSV file to analyze data completeness, field types, and picklist values before migration.")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

if uploaded_file:
    # Load data based on file type
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    
    # Display data preview
    st.write("### Data Preview")
    st.write(df.head())
    
    # Analyze Data Function
    def analyze_data(df):
        results = []
        picklist_dict = {}
        for column in df.columns:
            total_rows = len(df)
            non_empty_count = df[column].count()
            completion_rate = round((non_empty_count / total_rows) * 100, 2)
            
            # Detect field type
            if pd.api.types.is_numeric_dtype(df[column]):
                field_type = "Number"
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                field_type = "Date"
            elif df[column].nunique() / total_rows < 0.05 and not pd.api.types.is_datetime64_any_dtype(df[column]):
                field_type = "Picklist"
                picklist_dict[column] = df[column].value_counts().to_dict()
            else:
                field_type = "Text"
            
            results.append({
                "Column Name": column,
                "Completion Rate (%)": completion_rate,
                "Field Type": field_type
            })
        
        return pd.DataFrame(results), picklist_dict
    
    # Perform analysis
    st.write("### Analysis Results")
    analysis_results, picklist_values = analyze_data(df)
    st.write(analysis_results)
    
    # Convert results to CSV
    csv = analysis_results.to_csv(index=False).encode('utf-8')
    
    # Create picklist values table
    if picklist_values:
        st.write("### Picklist Values")
        picklist_df = pd.DataFrame([(col, key, val) for col, values in picklist_values.items() for key, val in values.items()], 
                                   columns=["Column Name", "Picklist Value", "Count"])
        st.write(picklist_df)
        picklist_csv = picklist_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Picklist Values", picklist_csv, "datahaven_picklist_values.csv", "text/csv")
    
    # Provide download option for analysis results
    st.download_button("Download Analysis Results", csv, "datahaven_analysis.csv", "text/csv")
