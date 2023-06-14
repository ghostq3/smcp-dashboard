"""Third party imports."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read data from CSV
def read_data(filename):
    """Read data from csv."""
    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime
    return df

def generate_line_chart(data, metrics1="", metrics2="", metrics3=""):
    """Generate Line charts."""
    chart_data = data.set_index('Date')  # Set 'Date' column as index

    # Plot the line charts
    if metrics1 in chart_data.columns:
        st.line_chart(chart_data[metrics1])

    if metrics2 in chart_data.columns:
        st.line_chart(chart_data[metrics2])

    if metrics3 in chart_data.columns:
        st.line_chart(chart_data[metrics3])

    # Add a message if no metrics were selected
    if not (metrics1 or metrics2 or metrics3):
        st.write("Please select at least one metric to display.")


def generate_pie_chart(data,widget_id,chart_title):
    """Generate Pie Chart."""
    options = ['View Count', 'Like Count', 'Comment Count']
    selected_options = st.multiselect(widget_id, options, default=options)

    fig = go.Figure()

    for option in selected_options:
        fig.add_trace(go.Pie(labels=data['Game'], values=data[option], name=option, textinfo='label+percent', textposition='inside'))

    fig.update_layout(title=chart_title)

    st.plotly_chart(fig)

def generate_bar_chart(data,widget_id):
    """Generate Bar Chart."""
    options = ['View Count', 'Like Count', 'Comment Count']
    selected_options = st.multiselect(widget_id, options, default=options)

    counts = data.groupby('Game')[selected_options].sum().reset_index()
    counts['Total'] = counts[selected_options].sum(axis=1)  # Calculate the sum of selected options as the 'Total' column
    counts_sorted = counts.sort_values(by='Total', ascending=True)  # Sort by the 'Total' column

    labels = counts_sorted['Game']
    values = counts_sorted[selected_options]

    fig = go.Figure()
    for option in selected_options:
        fig.add_trace(go.Bar(y=labels, x=values[option], orientation='h', name=option))

    fig.update_layout(title='Count of View Count, Like Count, Comment Count',
                      xaxis_title='Count',
                      yaxis_title='Game',
                      barmode='stack')

    st.plotly_chart(fig, use_container_width=True)

# Main function
def main():
    """Initialize the program."""
    st.title("Youtube Share of Voice")

    # Read CSV file
    filename = 'csvs/SOV - SoV_YT.csv'
    data = read_data(filename)

    # Generate line chart
    st.subheader("Axie Infinity Trend")
    generate_line_chart(data,'View Count', 'Like Count', 'Comment Count')


    # Generate pie chart
    pie_df = pd.read_csv('csvs/SOV - YT_axie_vs_field.csv')

    generate_pie_chart(pie_df,'Select AVF Metrics','Axie Infinity VS Field')
    generate_bar_chart(pie_df,' ')

    # Generate pie chart for Ronin Games
    rgpie_df = pd.read_csv('csvs/SOV - YT_ronin_games.csv')

    generate_pie_chart(rgpie_df,'Select Ronin Games Metrics','Ronin Games VS Each Other')
    generate_bar_chart(rgpie_df,'  ')

    # Generate pie chart for Ronin Games vs Field
    rvfpie_df = pd.read_csv('csvs/SOV - YT_RVF.csv')


    generate_pie_chart(rvfpie_df,'Select RVF Metrics','Ronin Games VS Field')
    generate_bar_chart(rvfpie_df,'   ')

    

if __name__ == '__main__':
    main()
