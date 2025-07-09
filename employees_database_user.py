import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.title("📂 Upload Your File")

# Upload any file (CSV, Excel)
file_name = st.text_input("Enter file name")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
file_name_to_work = file_name.replace(".csv",".xlsx")
if uploaded_file:
    
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Save the file

    with open(file_name_to_work, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # st.success(f"📁 File saved to: `{file_name}`")

    # Determine file type and display content
    df = pd.read_excel(file_name_to_work)

    # Streamlit layout
    st.title("📊 Employee Data Dashboard")

    if st.checkbox("Show Raw Data"):
        st.dataframe(df)

    filtered_mean_salary_all_dept = pd.DataFrame()
    final_mean_salary = pd.DataFrame()
    # Filter by department
    mean_salary = df.groupby('Department')['Salary'].mean()
    mean_salary = mean_salary.reset_index()
    mean_salary_all_dept = mean_salary['Salary'].mean()
    new_row={'Department': 'All Departments', 'Salary': mean_salary_all_dept}
    final_mean_salary = mean_salary.copy()
    new_row = pd.DataFrame([{'Department': 'All Departments', 'Salary': mean_salary['Salary'].mean()}])
    final_mean_salary = pd.concat([new_row, mean_salary], ignore_index=True)
    selected_dept = st.selectbox("Select Department", final_mean_salary['Department'].unique())
    if selected_dept == 'All Departments':
        filtered_mean_salary_all_dept = mean_salary
    else:
        # Filter the mean salary based on the selected department
        st.write(f"Selected Department: {selected_dept}")
        
    st.subheader(f"Average Salary in {selected_dept} Department")
    st.metric(label="Average Salary", value=f"${final_mean_salary[final_mean_salary['Department'] == selected_dept]['Salary'].values[0]:,.2f}")


    # Plotting
    if filtered_mean_salary_all_dept.empty:
        filtered_df = df[df['Department'] == selected_dept]
        st.bar_chart(filtered_df[['Name', 'Salary']].set_index('Name'))
        names_for_bar_graph = filtered_df['Name']
        salary_for_bar_graph = filtered_df['Salary']
        plt.bar(names_for_bar_graph,salary_for_bar_graph)
        st.write((filtered_df[['Name', 'Salary']].set_index('Name')))
        save_image_file_name="Average _Salary_for_{selected_dept}_Department.png"
        plt.savefig(save_image_file_name)

    else:
        st.write("Average Salary by Department")
        filtered_salary = final_mean_salary[final_mean_salary['Department'] == selected_dept]['Salary']
    #    st.write(mean_salary['Salary', Where 'Departmet'='selected_dept'])    
        st.write(f"Average Salary for {selected_dept} Department: ${final_mean_salary[final_mean_salary['Department'] == selected_dept]['Salary'].values[0]:,.2f}" if not filtered_salary.empty else "No data found.")
        st.bar_chart(final_mean_salary[['Department', 'Salary']].set_index('Department'))
        st.write((final_mean_salary[['Department', 'Salary']].set_index('Department')))
        names_for_bar_graph = final_mean_salary['Department']
        salary_for_bar_graph = final_mean_salary['Salary']
        plt.bar(names_for_bar_graph,salary_for_bar_graph)
        save_image_file_name="Average _Salary_for_Department.png"
        plt.savefig(save_image_file_name)
    st.download_button(
        label="📥 Download data graph image",
        data=save_image_file_name,
        file_name=save_image_file_name,
    )
    #os.remove(save_image_file_name)
    #os.remove(file_name_to_work)



else: 
    select_box_empty=[]
    st.selectbox(" ",select_box_empty)
    