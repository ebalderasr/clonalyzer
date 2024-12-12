import streamlit as st
import pandas as pd
import os
from clonalyzer import load_and_clean_data, process_data, generate_plots  # Asegúrate de tener estas funciones

# Title and description
st.title("Clonalyzer: Kinetics Data Analysis for CHO Cell Clones")
st.write("""
This tool allows you to clean, process, and analyze kinetic data for CHO cell clones.
Upload your data, specify the exponential phase, and visualize the results dynamically.
""")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    # Display the first rows of the uploaded file
    st.write("Preview of uploaded file:")
    uploaded_data = pd.read_csv(uploaded_file)
    st.dataframe(uploaded_data.head())

    # Exponential phase selection
    time_start = st.number_input("Start time for exponential phase (days)", min_value=0.0, value=0.0)
    time_end = st.number_input("End time for exponential phase (days)", min_value=0.0, value=4.0)

    # Analyze button
    if st.button("Analyze"):
        # Process the data
        st.write("Processing data...")
        expected_columns = [
            "Clone", "T", "G", "Gln", "Xv", "Xd", "L", "V", "MAb", "rP", "rep"
        ]
        kinetics_data = load_and_clean_data(uploaded_file, expected_columns)
        df_results = process_data(kinetics_data, time_start, time_end)

        # Display results
        st.write("Analysis complete. Results:")
        st.dataframe(df_results)

        # Generate plots
        st.write("Generating plots...")
        output_dir = "figures"
        os.makedirs(output_dir, exist_ok=True)
        generate_plots(df_results, output_dir)

        # Display plots in the app
        for filename in os.listdir(output_dir):
            if filename.endswith(".png"):
                st.image(os.path.join(output_dir, filename), caption=filename, use_column_width=True)
