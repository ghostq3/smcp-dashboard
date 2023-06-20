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


def generate_line_chart(data,metrics1="",metrics2="",metrics3=""):
    """Generate Line chart."""
    chart_data = data.set_index('Date')  # Set 'Date' column as index

    # Get user selection from multiselect checkbox
    options = st.multiselect('Select Counts to Display', [metrics1, metrics2, metrics3], default=[metrics1,metrics2,metrics3])

    # Plot the line chart based on user selection
    selected_columns = [option for option in options if option in chart_data.columns]
    if selected_columns:
        st.line_chart(chart_data[selected_columns])
    else:
        st.write("Please select at least one count to display.")


def generate_pie_chart(data,widget_id,chart_title):
    """Generate Pie Chart."""
    options = ['Tweet', 'Retweet Count', 'Likes Count']
    selected_options = st.multiselect(widget_id, options, default=options)

    fig = go.Figure()

    for option in selected_options:
        fig.add_trace(go.Pie(labels=data['Game'], values=data[option], name=option, textinfo='label+percent', textposition='inside'))

    fig.update_layout(title=chart_title)

    st.plotly_chart(fig)

def generate_bar_chart(data,widget_id):
    """Generate Bar Chart."""
    options = ['Tweet', 'Retweet Count', 'Likes Count']
    selected_options = st.multiselect(widget_id, options, default=options)

    counts = data.groupby('Game')[selected_options].sum().reset_index()
    counts['Total'] = counts[selected_options].sum(axis=1)  # Calculate the sum of selected options as the 'Total' column
    counts_sorted = counts.sort_values(by='Total', ascending=True)  # Sort by the 'Total' column

    labels = counts_sorted['Game']
    values = counts_sorted[selected_options]

    fig = go.Figure()
    for option in selected_options:
        fig.add_trace(go.Bar(y=labels, x=values[option], orientation='h', name=option))

    fig.update_layout(title='Count of Tweets, Retweets, and Likes',
                      xaxis_title='Count',
                      yaxis_title='Game',
                      barmode='stack')

    st.plotly_chart(fig, use_container_width=True)

# Main function
def main():
    """Initialize the program."""
    st.title("Twitter Share of Voice")

    # Read CSV file
    filename = 'csvs/SOV - SoV_twitter.csv'
    data = read_data(filename)

    # Generate line chart
    st.subheader("Axie Infinity Trend")
    generate_line_chart(data,'Tweet','Likes Count','Retweet Count')

    pie_df = pd.read_csv('csvs/SOV - Twitter_axie_vs_field.csv')

    generate_pie_chart(pie_df,'Select AVF metrics','Axie Infinity vs Field')
    generate_bar_chart(pie_df,' ')

    ronin_games_df = pd.read_csv('csvs/SOV - Twitter_ronin_games.csv')

    generate_pie_chart(ronin_games_df,'Select Ronin Games metrics','Ronin Games VS Each Other')
    generate_bar_chart(ronin_games_df,'  ')

    rvf_df = pd.read_csv('csvs/SOV - Twitter_RVF.csv')

    generate_pie_chart(rvf_df,'Select RVF metrics','Ronin Games VS Field')
    generate_bar_chart(rvf_df,'   ')

if __name__ == '__main__':
    main()
