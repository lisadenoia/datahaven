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
        for column in df.columns:
            total_rows = len(df)
            non_empty_count = df[column].count()
            completion_rate = round((non_empty_count / total_rows) * 100, 2)
            
            # Detect field type
            if pd.api.types.is_numeric_dtype(df[column]):
                field_type = "Number"
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                field_type = "Date"
            elif df[column].nunique() / total_rows < 0.05:
                field_type = "Picklist"
            else:
                field_type = "Text"
            
            # Identify picklist values if applicable
            picklist_values = df[column].value_counts().to_dict() if field_type == "Picklist" else None
            
            results.append({
                "Column Name": column,
                "Completion Rate (%)": completion_rate,
                "Field Type": field_type,
                "Picklist Values": picklist_values
            })
        
        return pd.DataFrame(results)
    
    # Perform analysis
    st.write("### Analysis Results")
    analysis_results = analyze_data(df)
    st.write(analysis_results)
    
    # Provide download option
    csv = analysis_results.to_csv(index=False).encode('utf-8')
    st.download_button("Download Analysis Results", csv, "datahaven_analysis.csv", "text/csv")