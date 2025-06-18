from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
df=pd.read_csv('Shopping Trends And Customer Behaviour Dataset.csv')
#print(df.info())
Gender_per = df['Gender'].value_counts(normalize=True) * 100
Gender_count=df['Gender'].value_counts() 
#print(Gender_per)
#print(Gender_count)
Gender_df = pd.DataFrame({
    'Gender': Gender_count.index.values,
    'Count': Gender_count.values,
    'Percentage': Gender_per.values
})
#print(Gender_df)
#---------
Age_per = df['Age'].value_counts(normalize=True) * 100
Age_count=df['Age'].value_counts() 
#print(Age_per)
#print(Age_count)
Age_df = pd.DataFrame({
    'Age': Age_count.index.values,
    'Count': Age_count.values,
    'Percentage': Age_per.values
})
age_std = df['Age'].std()  # Standard deviation
age_var = df['Age'].var()  # Variance
age_min = df['Age'].min()
age_max = df['Age'].max()

print(age_std)
print(age_var)
print(age_min)
print(age_max)
#-----------
#print(Age_df)


Season_per = (
    df.groupby('Season')['Customer ID'].count()  # Get raw counts
    .div(len(df))  # Divide by total customers
    .mul(100)  # Convert to percentage
    
)
Season_count=df.groupby('Season')['Customer ID'].count()
Season_df = pd.DataFrame({
    'Season': Season_count.index.values,
    'Count': Season_count.values,
    'Percentage': Season_per.values
})


#--------------
Age_usd = df.groupby('Age')['Purchase Amount (USD)'].sum()

#print(Age_per)
#print(Age_count)
Age_usd_df = pd.DataFrame({
    'Age': Age_usd.index.values,
    'Total Purchase Amount (USD)': Age_usd.values,
    
})
fig_Age_usd_df = px.line(Age_usd_df, x="Age",
                         y="Total Purchase Amount (USD)",
                         title='Total Purchase Amount (USD) of Ages')
#---------
Category_usd = df.groupby('Category')['Purchase Amount (USD)'].sum()

#print(Age_per)
#print(Age_count)
Category_usd_df = pd.DataFrame({
    'Category': Category_usd.index.values,
    'Total Purchase Amount (USD)': Category_usd.values,
    
})
fig_Category_usd_df = px.line(Category_usd_df, x="Category",
                         y="Total Purchase Amount (USD)",
                         title='Total Purchase Amount (USD) of Category')
#-------------
Item_usd = df.groupby('Item Purchased')['Purchase Amount (USD)'].sum()

#print(Age_per)
#print(Age_count)
Item_usd_df = pd.DataFrame({
    'Item Purchased': Item_usd.index.values,
    'Total Purchase Amount (USD)': Item_usd.values,
    
})
fig_Item_usd_df = px.line(Item_usd_df, x="Item Purchased",
                         y="Total Purchase Amount (USD)",
                         title='Total Purchase Amount (USD) of Items')
#----------

Color_count=df.groupby('Color')['Customer ID'].count()
Color_df = pd.DataFrame({
    'Color': Color_count.index.values,
    'Count': Color_count.values,
    
})


#-----


# 1. Aggregate both metrics by location
location_stats = df.groupby('Location').agg(
    Customer_Count=('Customer ID', 'count'),
    Total_Purchases=('Purchase Amount (USD)', 'sum')
).reset_index()

# 2. Create the bar chart
fig_Location_df = px.bar(
    location_stats,
    x='Location',
    y='Customer_Count',
    title='Customer Count & Total Purchases by Location',
    labels={'Customer_Count': 'Number of Customers'}
      # Color by location
)

# 3. Add purchase amounts as a second axis
fig_Location_df.add_trace(
    px.line(
        location_stats,
        x='Location',
        y='Total_Purchases',
        markers=True
    ).update_traces(
        yaxis='y2',
        line=dict(color='black', width=3),
        name='Total Purchases ($)',
        hovertemplate="<b>%{x}</b><br>Total Sales: $%{y:,.2f}<extra></extra>",
        showlegend=False
    ).data[0]
)

# 4. Configure dual axes
fig_Location_df.update_layout(
    yaxis=dict(title='Number of Customers'),
    yaxis2=dict(
        title='Total Purchases (USD)',
        
        overlaying='y',
        side='right',
        rangemode='tozero'
    ),
    hovermode='x unified'
)




#------
Payment_per = (
    df.groupby('Payment Method')['Customer ID'].count()  # Get raw counts
    .div(len(df))  # Divide by total customers
    .mul(100)  # Convert to percentage
    
)
Payment_count=df.groupby('Payment Method')['Customer ID'].count()
Payment_df = pd.DataFrame({
    'Payment Method': Payment_count.index,
    'Count': Payment_count,
    'Percentage': Payment_per
}).reset_index(drop=True)
#-----
Frequency_per = (
    df.groupby('Frequency of Purchases')['Customer ID'].count()  # Get raw counts
    .div(len(df))  # Divide by total customers
    .mul(100)  # Convert to percentage
    
)
Frequency_count=df.groupby('Frequency of Purchases')['Customer ID'].count()
Frequency_df = pd.DataFrame({
    'Frequency of Purchases': Frequency_count.index.values,
    'Count': Frequency_count.values,
    'Percentage': Frequency_per.values
})
#---------------
Season_item = (
    df.groupby('Season')['Item Purchased'] )
# 1. Prepare the data with all three levels
season_category_items = (
    df.groupby(['Season', 'Category', 'Item Purchased'])
    .size()
    .reset_index(name='Count')
)

# 2. Create the 3-level sunburst chart
fig_Season_item = px.sunburst(
    season_category_items,
    path=['Season', 'Category', 'Item Purchased'],  # Hierarchy: Season → Category → Item
    values='Count',                                # Segment size based on purchase count
    title='Purchases by Season → Category → Item',
    color='Season',                               # Color by season for visual distinction
    color_discrete_sequence=px.colors.qualitative.Pastel,
    hover_data={'Count': ':,0'},                  # Format hover counts with thousands separators
    branchvalues='total'                          # Show absolute counts (not relative percentages)
)

# 3. Advanced formatting
fig_Season_item.update_layout(
    margin=dict(t=40, b=10, l=10, r=10),         # Tighter margins
    hoverlabel=dict(
        bgcolor="white",                          # White hover background
        font_size=12,
        font_family="Arial"
    )
)

fig_Season_item.update_traces(
    textinfo="label+percent parent",              # Show item name + % of parent category
    insidetextorientation='radial',               # Curve text radially
    textfont=dict(size=14)                       # Larger text for readability
)

# 4. Add interactive features
fig_Season_item.update_layout(
    clickmode='event+select',                     # Enable click interactions
    annotations=[
        dict(
            text="Click segments to drill down!",
            showarrow=False,
            x=0.5, y=-0.1,
            xref="paper", yref="paper"
        )
    ]
)
      
    

#----------------



fig_Payment_df = px.bar(Payment_df, x='Payment Method', y='Percentage', title='Payment method percentage')


fig_Season_df = px.line(Season_df, x="Season", y="Percentage", title='Seasonal customer percentage')

fig_Color_df = px.line(Color_df, x="Color", y="Count", title='Color sales')



fig_Frequency_df = px.pie(
    Frequency_df, 
    values='Percentage',
    names='Frequency of Purchases',
    title='Frequency of Purchases Distribution',
    labels={'Percentage': 'Percentage (%)'}
   
).update_layout(
    title_x=0.5,title_y=0.95)


fig_Gender_df = px.pie(
    Gender_df, 
    values='Percentage',
    names='Gender',
    title='Gender Distribution',
    labels={'Percentage': 'Percentage (%)'}
   
).update_layout(
    title_x=0.5,title_y=0.95)
#------------


fig_Age_df = px.bar(
    Age_df,
    x='Age',
    y='Count',
    title='Customer Count by Age Group',
    text_auto=True
).update_layout(
    xaxis_title='Age Group',
    yaxis_title='Number of Customers',
    uniformtext_minsize=8
)


#-----------------
external_stylesheets = ['/assets/custom.css']

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,  # ✅ Correct position
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Set global style variables
TAB_STYLE = {
    'padding': '12px',
    'fontWeight': 'bold',
    'backgroundColor': '#f8f9fa',
    'border': '1px solid #dee2e6',
    'borderBottom': 'none'
}

TAB_SELECTED_STYLE = {
    'backgroundColor': '#ffffff',
    'borderTop': '2px solid #007bff',
    'color': '#007bff',
    'padding': '12px',
    'fontWeight': 'bold'
}

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Shopping Trends Dashboard</title>
        <link rel="icon" href="/assets/favicon.ico" />
        <link rel="icon" type="image/png" href="/assets/store.png" />
        {%css%}
    </head>
    <body>
        {%app_entry%}  <!-- REQUIRED -->
        <footer>
            {%config%}   <!-- REQUIRED -->
            {%scripts%}  <!-- REQUIRED -->
            {%renderer%} <!-- REQUIRED -->
        </footer>
    </body>
</html>
'''
# Layout
app.layout = html.Div([
    
   
    
    html.Div([
        dcc.Tabs(
            id="tabs", value='tab1', 
            children=[
                dcc.Tab(label='Seasonal Trends', value='tab1', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label='Customer Behavior', value='tab2', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            ],
            style={'marginBottom': '20px'}
        ),
        html.Div(id='tabs-content')
    ], style={
        'backgroundColor': '#ffffff',
        'border': '1px solid #dee2e6',
        'padding': '10px',
        'boxShadow': '0 0 10px rgba(0,0,0,0.05)',
        'borderRadius': '6px',
        'maxWidth': '1400px',
        'margin': 'auto'
    })
], style={
    'backgroundColor': '#f4f4f9',
    'padding': '20px',
    'minHeight': '100vh'
})

app.layout = html.Div([
    html.H1('Seasonal Trends And Customer Behaviour Analysis Dashboard', id='h1', style={'textAlign': 'center', 'padding': '20px'}),
    
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Seasonal Trends', value='tab1'),
        dcc.Tab(label='Customer Behavior', value='tab2'),
    ]),
    
    html.Div(id='tabs-content')
])

@callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_tab(tab):
    if tab == 'tab1':
        return html.Div([
            # Full width graph, centered, max width for big screens
            html.Div(
                dcc.Graph(figure=fig_Location_df, style={'height': '350px', 'width': '100%'}),
                style={'maxWidth': '1200px', 'margin': 'auto'}
            ),

            # Two graphs side by side or stacked on small screens
            html.Div([
                html.Div(
                    dcc.Graph(figure=fig_Season_item, style={'height': '350px', 'width': '100%'}),
                    style={'flex': '1 1 300px', 'minWidth': '280px', 'margin': '10px'}
                ),
                html.Div(
                    dcc.Graph(figure=fig_Frequency_df, style={'height': '350px', 'width': '100%'}),
                    style={'flex': '1 1 300px', 'minWidth': '280px', 'margin': '10px'}
                ),
            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'maxWidth': '1200px',
                'margin': 'auto',
            }),

            # Full width graph again
            html.Div(
                dcc.Graph(figure=fig_Color_df, style={'height': '350px', 'width': '100%'}),
                style={'maxWidth': '1200px', 'margin': 'auto'}
            ),
        ], style={'padding': '10px', 'maxWidth': '1300px', 'margin': 'auto'})

    elif tab == 'tab2':
        return html.Div([
            html.Div([
                html.Div(
                    dcc.Graph(figure=fig_Gender_df, style={'height': '350px', 'width': '100%'}),
                    style={'flex': '1 1 300px', 'minWidth': '280px', 'margin': '10px'}
                ),
                html.Div(
                    dcc.Graph(figure=fig_Age_df, style={'height': '350px', 'width': '100%'}),
                    style={'flex': '1 1 300px', 'minWidth': '280px', 'margin': '10px'}
                ),
            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'maxWidth': '1200px',
                'margin': 'auto'
            }),

            html.Div(
                dcc.Graph(figure=fig_Payment_df, style={'height': '350px', 'width': '100%'}),
                style={'maxWidth': '1200px', 'margin': '20px auto'}
            ),

            html.Div([
                html.Div(
                    dcc.Graph(figure=fig_Age_usd_df, style={'height': '350px', 'width': '100%'}),
                    style={'flex': '1 1 300px', 'minWidth': '280px', 'margin': '10px'}
                ),
                html.Div(
                    dcc.Graph(figure=fig_Category_usd_df, style={'height': '350px', 'width': '100%'}),
                    style={'flex': '1 1 300px', 'minWidth': '280px', 'margin': '10px'}
                ),
            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'maxWidth': '1200px',
                'margin': 'auto'
            }),

            html.Div(
                dcc.Graph(figure=fig_Item_usd_df, style={'height': '350px', 'width': '100%'}),
                style={'maxWidth': '1200px', 'margin': '20px auto'}
            ),

        ], style={'padding': '10px', 'maxWidth': '1300px', 'margin': 'auto'})



    
if __name__=="__main__":
    print("Starting server...")
    app.run(host='127.0.0.1', port=8051, debug=True, use_reloader=True)







   #dcc.Graph(figure=fig_Gender_df),
   # dcc.Graph(figure=fig_Age_df),
    
    #dcc.Graph(figure=fig_Location_df),
    #dcc.Graph(figure=fig_Frequency_df),
    #dcc.Graph(figure=fig_Payment_df),
    #dcc.Graph(figure=fig_Season_item),
    #dcc.Graph(figure=fig_Color_df ),
    #dcc.Graph(figure=fig_Age_usd_df ),
    #dcc.Graph(figure=fig_Category_usd_df ),
    #dcc.Graph(figure=fig_Item_usd_df )
