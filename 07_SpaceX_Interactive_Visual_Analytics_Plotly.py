{"payload":{"allShortcutsEnabled":true,"fileTree":{"":{"items":[{"name":"00_SpaceX_Final Presentation_JF.pdf","path":"00_SpaceX_Final Presentation_JF.pdf","contentType":"file"},{"name":"01_SpaceX_Data_Collection_API.ipynb","path":"01_SpaceX_Data_Collection_API.ipynb","contentType":"file"},{"name":"02_SpaceX_Web_Scraping.ipynb","path":"02_SpaceX_Web_Scraping.ipynb","contentType":"file"},{"name":"03_SpaceX_Data_Wrangling.ipynb","path":"03_SpaceX_Data_Wrangling.ipynb","contentType":"file"},{"name":"04_SpaceX_EDA_SQL.ipynb","path":"04_SpaceX_EDA_SQL.ipynb","contentType":"file"},{"name":"05_SpaceX_EDA_Data_Visualization.ipynb","path":"05_SpaceX_EDA_Data_Visualization.ipynb","contentType":"file"},{"name":"06_SpaceX_Interactive_Visual_Analytics_Folium.ipynb","path":"06_SpaceX_Interactive_Visual_Analytics_Folium.ipynb","contentType":"file"},{"name":"07_SpaceX_Interactive_Visual_Analytics_Plotly.py","path":"07_SpaceX_Interactive_Visual_Analytics_Plotly.py","contentType":"file"},{"name":"08_SpaceX_Predictive_Analytics.ipynb","path":"08_SpaceX_Predictive_Analytics.ipynb","contentType":"file"},{"name":"README.md","path":"README.md","contentType":"file"}],"totalCount":10}},"fileTreeProcessingTime":1.9751560000000001,"foldersToFetch":[],"repo":{"id":597485523,"defaultBranch":"main","name":"IBM-Data-Science-Capstone-SpaceX","ownerLogin":"jonrfoss","currentUserCanPush":false,"isFork":false,"isEmpty":false,"createdAt":"2023-02-04T18:42:49.000+01:00","ownerAvatar":"https://avatars.githubusercontent.com/u/123580688?v=4","public":true,"private":false,"isOrgOwned":false},"symbolsExpanded":false,"treeExpanded":true,"refInfo":{"name":"main","listCacheKey":"v0:1675541529.53391","canEdit":true,"refType":"branch","currentOid":"12c747fe0bd6bab10075dff1ff81edc7c7619376"},"path":"07_SpaceX_Interactive_Visual_Analytics_Plotly.py","currentUser":{"id":139018749,"login":"pablorcordoves","userEmail":"pablorodriguez@sloan.mit.edu"},"blob":{"rawLines":["# Import required libraries","import pandas as pd","import dash","import dash_html_components as html","import dash_core_components as dcc","from dash.dependencies import Input, Output","import plotly.express as px","","# Read the airline data into pandas dataframe","spacex_df = pd.read_csv(\"spacex_launch_dash.csv\")","max_payload = spacex_df['Payload Mass (kg)'].max()","min_payload = spacex_df['Payload Mass (kg)'].min()","","# Create a dash application","app = dash.Dash(__name__)","","# Create an app layout","app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',","                                        style={'textAlign': 'center', 'color': '#503D36',","                                               'font-size': 40}),","                                # TASK 1: Add a dropdown list to enable Launch Site selection","                                # The default select value is for ALL sites","                                # dcc.Dropdown(id='site-dropdown',...)","                                ","                                dcc.Dropdown(id='site-dropdown',","                                options=[","                                    {'label': 'All Sites', 'value': 'All Sites'},","                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},","                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},","                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},","                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}","                                ],","                                placeholder='Select a Launch Site Here',","                                value='All Sites',","                                searchable=True","                                ),","                                html.Br(),","","                            ","","                                # TASK 2: Add a pie chart to show the total successful launches count for all sites","                                # If a specific launch site was selected, show the Success vs. Failed counts for the site","                                html.Div(dcc.Graph(id='success-pie-chart')),","                                html.Br(),","","                                html.P(\"Payload range (Kg):\"),","","","                                # TASK 3: Add a slider to select payload range","                                #dcc.RangeSlider(id='payload-slider',...)","                                dcc.RangeSlider(id='payload-slider',","                                min=0,","                                max=10000,","                                step=1000,","                                marks={i: '{}'.format(i) for i in range(0, 10001, 1000)},","                                value=[min_payload, max_payload]),","","","                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success","                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),","                                ])","                                ","","","# TASK 2:","# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output","@app.callback( Output(component_id='success-pie-chart', component_property='figure'),","               Input(component_id='site-dropdown', component_property='value'))","def get_pie_chart(launch_site):","    if launch_site == 'All Sites':","        fig = px.pie(values=spacex_df.groupby('Launch Site')['class'].mean(), ","                     names=spacex_df.groupby('Launch Site')['Launch Site'].first(),","                     title='Total Success Launches by Site')","    else:","        fig = px.pie(values=spacex_df[spacex_df['Launch Site']==str(launch_site)]['class'].value_counts(normalize=True), ","                     names=spacex_df['class'].unique(), ","                     title='Total Success Launches for Site {}'.format(launch_site))","    return(fig)","","# TASK 4:","# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output","@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),","              [Input(component_id='site-dropdown', component_property='value'),","               Input(component_id='payload-slider',component_property='value')])","def get_payload_chart(launch_site, payload_mass):","    if launch_site == 'All Sites':","        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], ","                x=\"Payload Mass (kg)\",","                y=\"class\",","                color=\"Booster Version Category\",","                hover_data=['Launch Site'],","                title='Correlation Between Payload and Success for All Sites')","    else:","        df = spacex_df[spacex_df['Launch Site']==str(launch_site)]","        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], ","                x=\"Payload Mass (kg)\",","                y=\"class\",","                color=\"Booster Version Category\",","                hover_data=['Launch Site'],","                title='Correlation Between Payload and Success for Site {}'.format(launch_site))","    return(fig)","","","# Run the app","if __name__ == '__main__':","    app.run_server()"],"stylingDirectives":[[{"start":0,"end":27,"cssClass":"pl-c"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":13,"cssClass":"pl-s1"},{"start":14,"end":16,"cssClass":"pl-k"},{"start":17,"end":19,"cssClass":"pl-s1"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":11,"cssClass":"pl-s1"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":27,"cssClass":"pl-s1"},{"start":28,"end":30,"cssClass":"pl-k"},{"start":31,"end":35,"cssClass":"pl-s1"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":27,"cssClass":"pl-s1"},{"start":28,"end":30,"cssClass":"pl-k"},{"start":31,"end":34,"cssClass":"pl-s1"}],[{"start":0,"end":4,"cssClass":"pl-k"},{"start":5,"end":9,"cssClass":"pl-s1"},{"start":10,"end":22,"cssClass":"pl-s1"},{"start":23,"end":29,"cssClass":"pl-k"},{"start":30,"end":35,"cssClass":"pl-v"},{"start":37,"end":43,"cssClass":"pl-v"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":13,"cssClass":"pl-s1"},{"start":14,"end":21,"cssClass":"pl-s1"},{"start":22,"end":24,"cssClass":"pl-k"},{"start":25,"end":27,"cssClass":"pl-s1"}],[],[{"start":0,"end":45,"cssClass":"pl-c"}],[{"start":0,"end":9,"cssClass":"pl-s1"},{"start":10,"end":11,"cssClass":"pl-c1"},{"start":12,"end":14,"cssClass":"pl-s1"},{"start":15,"end":23,"cssClass":"pl-en"},{"start":24,"end":48,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":23,"cssClass":"pl-s1"},{"start":24,"end":43,"cssClass":"pl-s"},{"start":45,"end":48,"cssClass":"pl-en"}],[{"start":0,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":23,"cssClass":"pl-s1"},{"start":24,"end":43,"cssClass":"pl-s"},{"start":45,"end":48,"cssClass":"pl-en"}],[],[{"start":0,"end":27,"cssClass":"pl-c"}],[{"start":0,"end":3,"cssClass":"pl-s1"},{"start":4,"end":5,"cssClass":"pl-c1"},{"start":6,"end":10,"cssClass":"pl-s1"},{"start":11,"end":15,"cssClass":"pl-v"},{"start":16,"end":24,"cssClass":"pl-s1"}],[],[{"start":0,"end":22,"cssClass":"pl-c"}],[{"start":0,"end":3,"cssClass":"pl-s1"},{"start":4,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":17,"cssClass":"pl-s1"},{"start":18,"end":21,"cssClass":"pl-v"},{"start":22,"end":30,"cssClass":"pl-s1"},{"start":30,"end":31,"cssClass":"pl-c1"},{"start":32,"end":36,"cssClass":"pl-s1"},{"start":37,"end":39,"cssClass":"pl-v"},{"start":40,"end":73,"cssClass":"pl-s"}],[{"start":40,"end":45,"cssClass":"pl-s1"},{"start":45,"end":46,"cssClass":"pl-c1"},{"start":47,"end":58,"cssClass":"pl-s"},{"start":60,"end":68,"cssClass":"pl-s"},{"start":70,"end":77,"cssClass":"pl-s"},{"start":79,"end":88,"cssClass":"pl-s"}],[{"start":47,"end":58,"cssClass":"pl-s"},{"start":60,"end":62,"cssClass":"pl-c1"}],[{"start":32,"end":93,"cssClass":"pl-c"}],[{"start":32,"end":75,"cssClass":"pl-c"}],[{"start":32,"end":70,"cssClass":"pl-c"}],[],[{"start":32,"end":35,"cssClass":"pl-s1"},{"start":36,"end":44,"cssClass":"pl-v"},{"start":45,"end":47,"cssClass":"pl-s1"},{"start":47,"end":48,"cssClass":"pl-c1"},{"start":48,"end":63,"cssClass":"pl-s"}],[{"start":32,"end":39,"cssClass":"pl-s1"},{"start":39,"end":40,"cssClass":"pl-c1"}],[{"start":37,"end":44,"cssClass":"pl-s"},{"start":46,"end":57,"cssClass":"pl-s"},{"start":59,"end":66,"cssClass":"pl-s"},{"start":68,"end":79,"cssClass":"pl-s"}],[{"start":37,"end":44,"cssClass":"pl-s"},{"start":46,"end":59,"cssClass":"pl-s"},{"start":61,"end":68,"cssClass":"pl-s"},{"start":70,"end":83,"cssClass":"pl-s"}],[{"start":37,"end":44,"cssClass":"pl-s"},{"start":46,"end":59,"cssClass":"pl-s"},{"start":61,"end":68,"cssClass":"pl-s"},{"start":70,"end":83,"cssClass":"pl-s"}],[{"start":37,"end":44,"cssClass":"pl-s"},{"start":46,"end":58,"cssClass":"pl-s"},{"start":60,"end":67,"cssClass":"pl-s"},{"start":69,"end":81,"cssClass":"pl-s"}],[{"start":37,"end":44,"cssClass":"pl-s"},{"start":46,"end":60,"cssClass":"pl-s"},{"start":62,"end":69,"cssClass":"pl-s"},{"start":71,"end":85,"cssClass":"pl-s"}],[],[{"start":32,"end":43,"cssClass":"pl-s1"},{"start":43,"end":44,"cssClass":"pl-c1"},{"start":44,"end":71,"cssClass":"pl-s"}],[{"start":32,"end":37,"cssClass":"pl-s1"},{"start":37,"end":38,"cssClass":"pl-c1"},{"start":38,"end":49,"cssClass":"pl-s"}],[{"start":32,"end":42,"cssClass":"pl-s1"},{"start":42,"end":43,"cssClass":"pl-c1"},{"start":43,"end":47,"cssClass":"pl-c1"}],[],[{"start":32,"end":36,"cssClass":"pl-s1"},{"start":37,"end":39,"cssClass":"pl-v"}],[],[],[],[{"start":32,"end":115,"cssClass":"pl-c"}],[{"start":32,"end":121,"cssClass":"pl-c"}],[{"start":32,"end":36,"cssClass":"pl-s1"},{"start":37,"end":40,"cssClass":"pl-v"},{"start":41,"end":44,"cssClass":"pl-s1"},{"start":45,"end":50,"cssClass":"pl-v"},{"start":51,"end":53,"cssClass":"pl-s1"},{"start":53,"end":54,"cssClass":"pl-c1"},{"start":54,"end":73,"cssClass":"pl-s"}],[{"start":32,"end":36,"cssClass":"pl-s1"},{"start":37,"end":39,"cssClass":"pl-v"}],[],[{"start":32,"end":36,"cssClass":"pl-s1"},{"start":37,"end":38,"cssClass":"pl-v"},{"start":39,"end":60,"cssClass":"pl-s"}],[],[],[{"start":32,"end":78,"cssClass":"pl-c"}],[{"start":32,"end":73,"cssClass":"pl-c"}],[{"start":32,"end":35,"cssClass":"pl-s1"},{"start":36,"end":47,"cssClass":"pl-v"},{"start":48,"end":50,"cssClass":"pl-s1"},{"start":50,"end":51,"cssClass":"pl-c1"},{"start":51,"end":67,"cssClass":"pl-s"}],[{"start":32,"end":35,"cssClass":"pl-s1"},{"start":35,"end":36,"cssClass":"pl-c1"},{"start":36,"end":37,"cssClass":"pl-c1"}],[{"start":32,"end":35,"cssClass":"pl-s1"},{"start":35,"end":36,"cssClass":"pl-c1"},{"start":36,"end":41,"cssClass":"pl-c1"}],[{"start":32,"end":36,"cssClass":"pl-s1"},{"start":36,"end":37,"cssClass":"pl-c1"},{"start":37,"end":41,"cssClass":"pl-c1"}],[{"start":32,"end":37,"cssClass":"pl-s1"},{"start":37,"end":38,"cssClass":"pl-c1"},{"start":39,"end":40,"cssClass":"pl-s1"},{"start":42,"end":46,"cssClass":"pl-s"},{"start":47,"end":53,"cssClass":"pl-en"},{"start":54,"end":55,"cssClass":"pl-s1"},{"start":57,"end":60,"cssClass":"pl-k"},{"start":61,"end":62,"cssClass":"pl-s1"},{"start":63,"end":65,"cssClass":"pl-c1"},{"start":66,"end":71,"cssClass":"pl-en"},{"start":72,"end":73,"cssClass":"pl-c1"},{"start":75,"end":80,"cssClass":"pl-c1"},{"start":82,"end":86,"cssClass":"pl-c1"}],[{"start":32,"end":37,"cssClass":"pl-s1"},{"start":37,"end":38,"cssClass":"pl-c1"},{"start":39,"end":50,"cssClass":"pl-s1"},{"start":52,"end":63,"cssClass":"pl-s1"}],[],[],[{"start":32,"end":120,"cssClass":"pl-c"}],[{"start":32,"end":36,"cssClass":"pl-s1"},{"start":37,"end":40,"cssClass":"pl-v"},{"start":41,"end":44,"cssClass":"pl-s1"},{"start":45,"end":50,"cssClass":"pl-v"},{"start":51,"end":53,"cssClass":"pl-s1"},{"start":53,"end":54,"cssClass":"pl-c1"},{"start":54,"end":85,"cssClass":"pl-s"}],[],[],[],[],[{"start":0,"end":9,"cssClass":"pl-c"}],[{"start":0,"end":85,"cssClass":"pl-c"}],[{"start":0,"end":85,"cssClass":"pl-en"},{"start":1,"end":4,"cssClass":"pl-s1"},{"start":5,"end":13,"cssClass":"pl-en"},{"start":15,"end":21,"cssClass":"pl-v"},{"start":22,"end":34,"cssClass":"pl-s1"},{"start":34,"end":35,"cssClass":"pl-c1"},{"start":35,"end":54,"cssClass":"pl-s"},{"start":56,"end":74,"cssClass":"pl-s1"},{"start":74,"end":75,"cssClass":"pl-c1"},{"start":75,"end":83,"cssClass":"pl-s"}],[{"start":0,"end":79,"cssClass":"pl-en"},{"start":15,"end":20,"cssClass":"pl-v"},{"start":21,"end":33,"cssClass":"pl-s1"},{"start":33,"end":34,"cssClass":"pl-c1"},{"start":34,"end":49,"cssClass":"pl-s"},{"start":51,"end":69,"cssClass":"pl-s1"},{"start":69,"end":70,"cssClass":"pl-c1"},{"start":70,"end":77,"cssClass":"pl-s"}],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":17,"cssClass":"pl-en"},{"start":18,"end":29,"cssClass":"pl-s1"}],[{"start":4,"end":6,"cssClass":"pl-k"},{"start":7,"end":18,"cssClass":"pl-s1"},{"start":19,"end":21,"cssClass":"pl-c1"},{"start":22,"end":33,"cssClass":"pl-s"}],[{"start":8,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":16,"cssClass":"pl-s1"},{"start":17,"end":20,"cssClass":"pl-en"},{"start":21,"end":27,"cssClass":"pl-s1"},{"start":27,"end":28,"cssClass":"pl-c1"},{"start":28,"end":37,"cssClass":"pl-s1"},{"start":38,"end":45,"cssClass":"pl-en"},{"start":46,"end":59,"cssClass":"pl-s"},{"start":61,"end":68,"cssClass":"pl-s"},{"start":70,"end":74,"cssClass":"pl-en"}],[{"start":21,"end":26,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":27,"end":36,"cssClass":"pl-s1"},{"start":37,"end":44,"cssClass":"pl-en"},{"start":45,"end":58,"cssClass":"pl-s"},{"start":60,"end":73,"cssClass":"pl-s"},{"start":75,"end":80,"cssClass":"pl-en"}],[{"start":21,"end":26,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":27,"end":59,"cssClass":"pl-s"}],[{"start":4,"end":8,"cssClass":"pl-k"}],[{"start":8,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":16,"cssClass":"pl-s1"},{"start":17,"end":20,"cssClass":"pl-en"},{"start":21,"end":27,"cssClass":"pl-s1"},{"start":27,"end":28,"cssClass":"pl-c1"},{"start":28,"end":37,"cssClass":"pl-s1"},{"start":38,"end":47,"cssClass":"pl-s1"},{"start":48,"end":61,"cssClass":"pl-s"},{"start":62,"end":64,"cssClass":"pl-c1"},{"start":64,"end":67,"cssClass":"pl-en"},{"start":68,"end":79,"cssClass":"pl-s1"},{"start":82,"end":89,"cssClass":"pl-s"},{"start":91,"end":103,"cssClass":"pl-en"},{"start":104,"end":113,"cssClass":"pl-s1"},{"start":113,"end":114,"cssClass":"pl-c1"},{"start":114,"end":118,"cssClass":"pl-c1"}],[{"start":21,"end":26,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":27,"end":36,"cssClass":"pl-s1"},{"start":37,"end":44,"cssClass":"pl-s"},{"start":46,"end":52,"cssClass":"pl-en"}],[{"start":21,"end":26,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":27,"end":63,"cssClass":"pl-s"},{"start":64,"end":70,"cssClass":"pl-en"},{"start":71,"end":82,"cssClass":"pl-s1"}],[{"start":4,"end":10,"cssClass":"pl-k"},{"start":11,"end":14,"cssClass":"pl-s1"}],[],[{"start":0,"end":9,"cssClass":"pl-c"}],[{"start":0,"end":119,"cssClass":"pl-c"}],[{"start":0,"end":97,"cssClass":"pl-en"},{"start":1,"end":4,"cssClass":"pl-s1"},{"start":5,"end":13,"cssClass":"pl-en"},{"start":15,"end":21,"cssClass":"pl-v"},{"start":22,"end":34,"cssClass":"pl-s1"},{"start":34,"end":35,"cssClass":"pl-c1"},{"start":35,"end":66,"cssClass":"pl-s"},{"start":68,"end":86,"cssClass":"pl-s1"},{"start":86,"end":87,"cssClass":"pl-c1"},{"start":87,"end":95,"cssClass":"pl-s"}],[{"start":0,"end":79,"cssClass":"pl-en"},{"start":15,"end":20,"cssClass":"pl-v"},{"start":21,"end":33,"cssClass":"pl-s1"},{"start":33,"end":34,"cssClass":"pl-c1"},{"start":34,"end":49,"cssClass":"pl-s"},{"start":51,"end":69,"cssClass":"pl-s1"},{"start":69,"end":70,"cssClass":"pl-c1"},{"start":70,"end":77,"cssClass":"pl-s"}],[{"start":0,"end":80,"cssClass":"pl-en"},{"start":15,"end":20,"cssClass":"pl-v"},{"start":21,"end":33,"cssClass":"pl-s1"},{"start":33,"end":34,"cssClass":"pl-c1"},{"start":34,"end":50,"cssClass":"pl-s"},{"start":51,"end":69,"cssClass":"pl-s1"},{"start":69,"end":70,"cssClass":"pl-c1"},{"start":70,"end":77,"cssClass":"pl-s"}],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":21,"cssClass":"pl-en"},{"start":22,"end":33,"cssClass":"pl-s1"},{"start":35,"end":47,"cssClass":"pl-s1"}],[{"start":4,"end":6,"cssClass":"pl-k"},{"start":7,"end":18,"cssClass":"pl-s1"},{"start":19,"end":21,"cssClass":"pl-c1"},{"start":22,"end":33,"cssClass":"pl-s"}],[{"start":8,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":16,"cssClass":"pl-s1"},{"start":17,"end":24,"cssClass":"pl-en"},{"start":25,"end":34,"cssClass":"pl-s1"},{"start":35,"end":44,"cssClass":"pl-s1"},{"start":45,"end":64,"cssClass":"pl-s"},{"start":66,"end":73,"cssClass":"pl-en"},{"start":74,"end":86,"cssClass":"pl-s1"},{"start":87,"end":88,"cssClass":"pl-c1"},{"start":91,"end":103,"cssClass":"pl-s1"},{"start":104,"end":105,"cssClass":"pl-c1"}],[{"start":16,"end":17,"cssClass":"pl-s1"},{"start":17,"end":18,"cssClass":"pl-c1"},{"start":18,"end":37,"cssClass":"pl-s"}],[{"start":16,"end":17,"cssClass":"pl-s1"},{"start":17,"end":18,"cssClass":"pl-c1"},{"start":18,"end":25,"cssClass":"pl-s"}],[{"start":16,"end":21,"cssClass":"pl-s1"},{"start":21,"end":22,"cssClass":"pl-c1"},{"start":22,"end":48,"cssClass":"pl-s"}],[{"start":16,"end":26,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":28,"end":41,"cssClass":"pl-s"}],[{"start":16,"end":21,"cssClass":"pl-s1"},{"start":21,"end":22,"cssClass":"pl-c1"},{"start":22,"end":77,"cssClass":"pl-s"}],[{"start":4,"end":8,"cssClass":"pl-k"}],[{"start":8,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":22,"cssClass":"pl-s1"},{"start":23,"end":32,"cssClass":"pl-s1"},{"start":33,"end":46,"cssClass":"pl-s"},{"start":47,"end":49,"cssClass":"pl-c1"},{"start":49,"end":52,"cssClass":"pl-en"},{"start":53,"end":64,"cssClass":"pl-s1"}],[{"start":8,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":16,"cssClass":"pl-s1"},{"start":17,"end":24,"cssClass":"pl-en"},{"start":25,"end":27,"cssClass":"pl-s1"},{"start":28,"end":30,"cssClass":"pl-s1"},{"start":31,"end":50,"cssClass":"pl-s"},{"start":52,"end":59,"cssClass":"pl-en"},{"start":60,"end":72,"cssClass":"pl-s1"},{"start":73,"end":74,"cssClass":"pl-c1"},{"start":77,"end":89,"cssClass":"pl-s1"},{"start":90,"end":91,"cssClass":"pl-c1"}],[{"start":16,"end":17,"cssClass":"pl-s1"},{"start":17,"end":18,"cssClass":"pl-c1"},{"start":18,"end":37,"cssClass":"pl-s"}],[{"start":16,"end":17,"cssClass":"pl-s1"},{"start":17,"end":18,"cssClass":"pl-c1"},{"start":18,"end":25,"cssClass":"pl-s"}],[{"start":16,"end":21,"cssClass":"pl-s1"},{"start":21,"end":22,"cssClass":"pl-c1"},{"start":22,"end":48,"cssClass":"pl-s"}],[{"start":16,"end":26,"cssClass":"pl-s1"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":28,"end":41,"cssClass":"pl-s"}],[{"start":16,"end":21,"cssClass":"pl-s1"},{"start":21,"end":22,"cssClass":"pl-c1"},{"start":22,"end":75,"cssClass":"pl-s"},{"start":76,"end":82,"cssClass":"pl-en"},{"start":83,"end":94,"cssClass":"pl-s1"}],[{"start":4,"end":10,"cssClass":"pl-k"},{"start":11,"end":14,"cssClass":"pl-s1"}],[],[],[{"start":0,"end":13,"cssClass":"pl-c"}],[{"start":0,"end":2,"cssClass":"pl-k"},{"start":3,"end":11,"cssClass":"pl-s1"},{"start":12,"end":14,"cssClass":"pl-c1"},{"start":15,"end":25,"cssClass":"pl-s"}],[{"start":4,"end":7,"cssClass":"pl-s1"},{"start":8,"end":18,"cssClass":"pl-en"}]],"csv":null,"csvError":null,"dependabotInfo":{"showConfigurationBanner":false,"configFilePath":null,"networkDependabotPath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/network/updates","dismissConfigurationNoticePath":"/settings/dismiss-notice/dependabot_configuration_notice","configurationNoticeDismissed":false,"repoAlertsPath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/security/dependabot","repoSecurityAndAnalysisPath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/settings/security_analysis","repoOwnerIsOrg":false,"currentUserCanAdminRepo":false},"displayName":"07_SpaceX_Interactive_Visual_Analytics_Plotly.py","displayUrl":"https://github.com/jonrfoss/IBM-Data-Science-Capstone-SpaceX/blob/main/07_SpaceX_Interactive_Visual_Analytics_Plotly.py?raw=true","headerInfo":{"blobSize":"5.1 KB","deleteInfo":{"deleteTooltip":"Fork this repository and delete the file"},"editInfo":{"editTooltip":"Fork this repository and edit the file"},"ghDesktopPath":"https://desktop.github.com","gitLfsPath":null,"onBranch":true,"shortPath":"5f3f6e4","siteNavLoginPath":"/login?return_to=https%3A%2F%2Fgithub.com%2Fjonrfoss%2FIBM-Data-Science-Capstone-SpaceX%2Fblob%2Fmain%2F07_SpaceX_Interactive_Visual_Analytics_Plotly.py","isCSV":false,"isRichtext":false,"toc":null,"lineInfo":{"truncatedLoc":"106","truncatedSloc":"88"},"mode":"file"},"image":false,"isCodeownersFile":null,"isPlain":false,"isValidLegacyIssueTemplate":false,"issueTemplateHelpUrl":"https://docs.github.com/articles/about-issue-and-pull-request-templates","issueTemplate":null,"discussionTemplate":null,"language":"Python","languageID":303,"large":false,"loggedIn":true,"newDiscussionPath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/discussions/new","newIssuePath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/issues/new","planSupportInfo":{"repoIsFork":null,"repoOwnedByCurrentUser":null,"requestFullPath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/blob/main/07_SpaceX_Interactive_Visual_Analytics_Plotly.py","showFreeOrgGatedFeatureMessage":null,"showPlanSupportBanner":null,"upgradeDataAttributes":null,"upgradePath":null},"publishBannersInfo":{"dismissActionNoticePath":"/settings/dismiss-notice/publish_action_from_dockerfile","releasePath":"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/releases/new?marketplace=true","showPublishActionBanner":false},"rawBlobUrl":"https://github.com/jonrfoss/IBM-Data-Science-Capstone-SpaceX/raw/main/07_SpaceX_Interactive_Visual_Analytics_Plotly.py","renderImageOrRaw":false,"richText":null,"renderedFileInfo":null,"shortPath":null,"symbolsEnabled":true,"tabSize":8,"topBannersInfo":{"overridingGlobalFundingFile":false,"globalPreferredFundingPath":null,"repoOwner":"jonrfoss","repoName":"IBM-Data-Science-Capstone-SpaceX","showInvalidCitationWarning":false,"citationHelpUrl":"https://docs.github.com/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files","showDependabotConfigurationBanner":false,"actionsOnboardingTip":null},"truncated":false,"viewable":true,"workflowRedirectUrl":null,"symbols":{"timed_out":false,"not_analyzed":false,"symbols":[{"name":"spacex_df","kind":"constant","ident_start":250,"ident_end":259,"extent_start":250,"extent_end":299,"fully_qualified_name":"spacex_df","ident_utf16":{"start":{"line_number":9,"utf16_col":0},"end":{"line_number":9,"utf16_col":9}},"extent_utf16":{"start":{"line_number":9,"utf16_col":0},"end":{"line_number":9,"utf16_col":49}}},{"name":"max_payload","kind":"constant","ident_start":300,"ident_end":311,"extent_start":300,"extent_end":350,"fully_qualified_name":"max_payload","ident_utf16":{"start":{"line_number":10,"utf16_col":0},"end":{"line_number":10,"utf16_col":11}},"extent_utf16":{"start":{"line_number":10,"utf16_col":0},"end":{"line_number":10,"utf16_col":50}}},{"name":"min_payload","kind":"constant","ident_start":351,"ident_end":362,"extent_start":351,"extent_end":401,"fully_qualified_name":"min_payload","ident_utf16":{"start":{"line_number":11,"utf16_col":0},"end":{"line_number":11,"utf16_col":11}},"extent_utf16":{"start":{"line_number":11,"utf16_col":0},"end":{"line_number":11,"utf16_col":50}}},{"name":"app","kind":"constant","ident_start":431,"ident_end":434,"extent_start":431,"extent_end":456,"fully_qualified_name":"app","ident_utf16":{"start":{"line_number":14,"utf16_col":0},"end":{"line_number":14,"utf16_col":3}},"extent_utf16":{"start":{"line_number":14,"utf16_col":0},"end":{"line_number":14,"utf16_col":25}}},{"name":"get_pie_chart","kind":"function","ident_start":3310,"ident_end":3323,"extent_start":3306,"extent_end":3886,"fully_qualified_name":"get_pie_chart","ident_utf16":{"start":{"line_number":68,"utf16_col":4},"end":{"line_number":68,"utf16_col":17}},"extent_utf16":{"start":{"line_number":68,"utf16_col":0},"end":{"line_number":77,"utf16_col":15}}},{"name":"get_payload_chart","kind":"function","ident_start":4281,"ident_end":4298,"extent_start":4277,"extent_end":5158,"fully_qualified_name":"get_payload_chart","ident_utf16":{"start":{"line_number":84,"utf16_col":4},"end":{"line_number":84,"utf16_col":21}},"extent_utf16":{"start":{"line_number":84,"utf16_col":0},"end":{"line_number":100,"utf16_col":15}}}]}},"copilotInfo":{"documentationUrl":"https://docs.github.com/copilot/overview-of-github-copilot/about-github-copilot-for-individuals","notices":{"codeViewPopover":{"dismissed":false,"dismissPath":"/settings/dismiss-notice/code_view_copilot_popover"}},"userAccess":{"accessAllowed":false,"hasSubscriptionEnded":false,"orgHasCFBAccess":false,"userHasCFIAccess":false,"userHasOrgs":false,"userIsOrgAdmin":false,"userIsOrgMember":false,"business":null,"featureRequestInfo":null}},"copilotAccessAllowed":false,"csrf_tokens":{"/jonrfoss/IBM-Data-Science-Capstone-SpaceX/branches":{"post":"DmDec1GPLjdbHyAg9C5A6JFBNP8aDo30TcSeBB_MiEw3aTi1dFUiia1qvpBi1wYcZBN7cv5OcdX4X1yBwlvjSg"},"/repos/preferences":{"post":"nxcbi8HvkfyIAYR8ADNLiCflCZeZwk6fN5N1Y7QofajcEL3YPkEedydQKX2ARmr532R76U2LproNUa5OGbL3fw"}}},"title":"IBM-Data-Science-Capstone-SpaceX/07_SpaceX_Interactive_Visual_Analytics_Plotly.py at main · jonrfoss/IBM-Data-Science-Capstone-SpaceX"}