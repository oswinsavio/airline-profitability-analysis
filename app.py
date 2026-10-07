import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. PAGE SETUP
st.set_page_config(page_title="Emirates Route Profitability", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (Emirates Brand Theme + Sand Background) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F8F5F0 !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    h1, h2, h3, h4 {
        color: #d50032 !important; 
        font-weight: 700 !important;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border-left: 5px solid #d50032;
        padding: 15px 10px;
        border-radius: 4px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }
    /* Custom Styling for the Strategic Alert Box */
    .alert-box {
        background-color: #ffffff;
        border: 1px solid #d50032;
        border-left: 10px solid #d50032;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .alert-title { color: #d50032; font-weight: bold; font-size: 1.2rem; margin-bottom: 5px; }
    .alert-text { color: #4a4a4a; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv('airline_route_profitability.csv')
    df['Flight_Date'] = pd.to_datetime(df['Flight_Date'])
    return df

df = load_data()

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/Emirates_logo.svg", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Levels")
    st.markdown("---")
    page = st.radio("Select Module:", 
                    ["Level 1: Executive Overview", 
                     "Level 2: Route & Seasonality", 
                     "Level 3: ML Fleet Optimization"])
    st.markdown("---")
    st.caption("Made by Oswin Concessao for airline-profitability-analysis")

# 4. LEVEL 1: EXECUTIVE OVERVIEW
if page == "Level 1: Executive Overview":
    st.title("Executive Dashboard: System Health")
    st.markdown("### The Bottom Line: Revenue, Cost, and Margins")
    
    # --- CEO-LEVEL KPI METRIC CARDS ---
    total_profit = df['Profit'].sum()
    sys_margin = df['Profit_Margin'].mean()
    
    peak_margin = df[df['Season'] == 'Peak']['Profit_Margin'].mean()
    low_margin = df[df['Season'] == 'Low']['Profit_Margin'].mean()
    
    best_route = df.groupby('Route_Category')['Profit'].sum().idxmax()
    
    cost_cols = ['Fuel_Cost', 'Maintenance_Cost', 'Crew_Cost', 'Depreciation_Cost', 
                 'Insurance_Cost', 'Airport_Fees', 'Catering_Cost', 'Handling_Cost']
    biggest_cost_name = df[cost_cols].sum().idxmax().replace('_', ' ')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Net Profit", f"${total_profit:,.0f}")
    col2.metric("System Margin", f"{sys_margin:.1f}%")
    col3.metric("Peak vs Low Margin", f"{peak_margin:.1f}% / {low_margin:.1f}%")
    col4.metric("Top Earning Route", f"{best_route}")
    col5.metric("Top Cost Driver", f"{biggest_cost_name}")
    
    st.markdown("<br>", unsafe_allow_html=True) 
    
    # --- INTERACTIVE CHARTS: ROW 1 (The Breakdown) ---
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Operating Cost Composition")
        st.caption("Where is the cash going?")
        
        cost_sums = df[cost_cols].sum().reset_index()
        cost_sums.columns = ['Cost Component', 'Total Expense']
        cost_sums['Cost Component'] = cost_sums['Cost Component'].str.replace('_', ' ')
        cost_sums = cost_sums.sort_values('Total Expense', ascending=True)
        
        fig1 = px.bar(cost_sums, x='Total Expense', y='Cost Component', orientation='h',
                      color_discrete_sequence=['#c6a87c'], text_auto='.2s')
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                           xaxis_title="Total Expense ($)", yaxis_title="",
                           font=dict(family="Montserrat, sans-serif"))
        st.plotly_chart(fig1, use_container_width=True)
        
    with chart_col2:
        st.markdown("#### Margin Exposure by Route")
        st.caption("Which routes sustain margins across all seasons?")
        
        route_season_margin = df.groupby(['Route_Category', 'Season'])['Profit_Margin'].mean().reset_index()
        
        fig2 = px.bar(route_season_margin, x='Route_Category', y='Profit_Margin', color='Season', 
                      barmode='group', color_discrete_sequence=['#d50032', '#c6a87c', '#4a4a4a', '#8b0021']) 
        
        fig2.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Breakeven")
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                           xaxis_title="", yaxis_title="Avg Profit Margin (%)", legend_title="Season",
                           font=dict(family="Montserrat, sans-serif"))
        st.plotly_chart(fig2, use_container_width=True)

    # --- THE NARRATIVE BRIDGE (The Hook) ---
    st.markdown("""
        <div class="alert-box">
            <div class="alert-title">⚠️ Strategic Alert: The Low-Season Bleed</div>
            <div class="alert-text">
                While System Margins remain positive, the chart above reveals a critical vulnerability: 
                <strong>Short-Haul and Medium-Haul routes crash into negative margins during the Low Season.</strong> 
                Direct operating costs (like Fuel and Maintenance) remain stubbornly high while load factors drop, erasing our Peak Season gains. 
                <br><br>
                <em>Navigate to <strong>Level 2: Route & Seasonality</strong> in the sidebar to isolate these failing routes and diagnose the passenger demand gap.</em>
            </div>
        </div>
    """, unsafe_allow_html=True)


# =====================================================================
# 5. LEVEL 2: ROUTE & SEASONALITY 
# =====================================================================
elif page == "Level 2: Route & Seasonality":
    st.title("Route & Seasonality Diagnostics")
    st.markdown("### Isolating the Impact of Passenger Demand on Margins")
    
    # --- INTERACTIVE FILTERS ---
    st.markdown("#### Filter Flight Parameters")
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_season = st.multiselect("Select Season(s):", 
                                         options=df['Season'].unique(), 
                                         default=['Low', 'Shoulder'])
    with filter_col2:
        selected_route = st.multiselect("Select Route Category:", 
                                        options=df['Route_Category'].unique(), 
                                        default=['Short Haul', 'Medium Haul'])
        
    mask = (df['Season'].isin(selected_season)) & (df['Route_Category'].isin(selected_route))
    filtered_df = df[mask]
    
    if filtered_df.empty:
        st.warning("No flights match the selected filters. Please adjust your selection.")
    else:
        st.markdown("<hr>", unsafe_allow_html=True)

        # --- DYNAMIC KPIs FOR FILTERED DATA ---
        slice_rev = filtered_df['Total_Revenue'].sum()
        slice_cost = filtered_df['Total_Cost'].sum()
        slice_profit = filtered_df['Profit'].sum()
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Selected Revenue", f"${slice_rev:,.0f}")
        kpi2.metric("Selected Cost", f"${slice_cost:,.0f}")
        kpi3.metric("Selected Net Profit", f"${slice_profit:,.0f}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- DIAGNOSTIC CHARTS: ROW 1 ---
        diag_col1, diag_col2 = st.columns(2)
        
        with diag_col1:
            st.markdown("#### Average Revenue vs. Cost by Aircraft")
            st.caption("Identifying where fixed costs overwhelm generated revenue")
            
            # Calculate Average Revenue and Cost per Aircraft for the filtered slice
            rev_cost_df = filtered_df.groupby('Aircraft_Type')[['Total_Revenue', 'Total_Cost']].mean().reset_index()
            rc_melt = rev_cost_df.melt(id_vars='Aircraft_Type', value_vars=['Total_Revenue', 'Total_Cost'], 
                                       var_name='Metric', value_name='Amount')
            
            fig_rc = px.bar(rc_melt, x='Aircraft_Type', y='Amount', color='Metric', barmode='group',
                            color_discrete_sequence=['#d50032', '#4a4a4a'])
            fig_rc.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                 xaxis_title="", yaxis_title="Average Amount ($)", legend_title="",
                                 font=dict(family="Montserrat, sans-serif"))
            st.plotly_chart(fig_rc, use_container_width=True)
            
        with diag_col2:
            st.markdown("#### The Load Factor Tipping Point")
            st.caption("At what passenger capacity do aircraft start losing money?")
            
            fig3 = px.scatter(filtered_df, x='Load_Factor', y='Profit_Margin', 
                              color='Aircraft_Type', hover_data=['Route', 'Total_Revenue', 'Total_Cost'],
                              color_discrete_sequence=['#d50032', '#c6a87c', '#4a4a4a', '#8b0021', '#a58b66', '#2d2d2d'],
                              opacity=0.7)
            
            fig3.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Breakeven (0%)")
            fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                               xaxis_title="Passenger Load Factor (%)", yaxis_title="Profit Margin (%)",
                               font=dict(family="Montserrat, sans-serif"))
            st.plotly_chart(fig3, use_container_width=True)
            
        # --- ROW 2: BOTTOM 10 ROUTES ---
        st.markdown("#### The Bleed Roster: Bottom 10 Routes")
        bottom_dest = filtered_df.groupby('Route')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True).head(10)
        
        fig4 = px.bar(bottom_dest, x='Profit', y='Route', orientation='h',
                      color_discrete_sequence=['#4a4a4a'], text_auto='.2s')
        fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                           yaxis={'categoryorder':'total descending'}, 
                           xaxis_title="Net Profit / Loss ($)", yaxis_title="",
                           font=dict(family="Montserrat, sans-serif"))
        st.plotly_chart(fig4, use_container_width=True)

        # --- DYNAMIC NARRATIVE CALCULATION ---
        # 1. Find the worst performing aircraft dynamically
        worst_ac = filtered_df.groupby('Aircraft_Type')['Profit'].mean().idxmin()
        
        # 2. Find the average load factor of flights that lost money
        loss_flights = filtered_df[filtered_df['Profit'] < 0]
        if not loss_flights.empty:
            avg_loss_load = loss_flights['Load_Factor'].mean() * 100
            dynamic_stat = f"fall below {avg_loss_load:.0f}%"
        else:
            dynamic_stat = "drop unexpectedly"

        # --- TRULY DYNAMIC NARRATIVE CALCULATION ---
        # 1. Find the worst performing aircraft and its average loss
        worst_ac = filtered_df.groupby('Aircraft_Type')['Profit'].mean().idxmin()
        worst_ac_loss = filtered_df.groupby('Aircraft_Type')['Profit'].mean().min()
        
        # 2. Categorize the aircraft properly so the text makes aviation sense
        wide_bodies = ['Airbus A380', 'Boeing 777-300ER', 'Boeing 787-9', 'Airbus A350-900']
        if worst_ac in wide_bodies:
            ac_class = "high-capacity wide-body aircraft"
        else:
            ac_class = "narrow-body aircraft"
            
        # 3. Find the exact breakeven load factor for THIS specific aircraft
        ac_data = filtered_df[filtered_df['Aircraft_Type'] == worst_ac]
        loss_flights = ac_data[ac_data['Profit'] < 0]
        
        if not loss_flights.empty:
            # Find the highest load factor that still resulted in a loss
            breakeven_load = loss_flights['Load_Factor'].max() * 100
            dynamic_stat = f"fall below its {breakeven_load:.0f}% breakeven threshold"
        else:
            dynamic_stat = "drop during off-peak times"

        # --- THE NARRATIVE BRIDGE (Connecting Levels 1, 2, and 3) ---
        st.markdown(f"""
            <div class="alert-box">
                <div class="alert-title">⚙️ The Data Story: From Diagnosis to Solution</div>
                <div class="alert-text">
                    <strong>Level 1 (The Symptom):</strong> We identified that our system-wide margins were being dragged down during specific seasons and routes.<br><br>
                    <strong>Level 2 (The Diagnosis):</strong> The charts above reveal the root cause is inflexible capacity. Notice how a {ac_class} like the <strong>{worst_ac}</strong> requires a <strong>{dynamic_stat}</strong> just to break even. When passenger demand drops on these filtered routes, this aircraft averages a net loss of <strong>${abs(worst_ac_loss):,.0f} per flight</strong> because its massive fixed costs remain identical whether it flies full or half-empty.<br><br>
                    <strong>Level 3 (The Cure):</strong> The solution is not to cancel flights, but to fly smarter. <em>Navigate to <strong>Level 3: ML Fleet Optimization</strong> to see how we deploy a Predictive Machine Learning model to forecast passenger demand in advance, dynamically swapping in right-sized aircraft to protect our bottom line.</em>
                </div>
            </div>
        """, unsafe_allow_html=True)

# =====================================================================
# 6. LEVEL 3: ML FLEET OPTIMIZATION 
# =====================================================================
elif page == "Level 3: ML Fleet Optimization":
    st.title("AI-Driven Fleet Optimization")
    st.markdown("### Predictive Capacity Allocation Model")
    st.markdown("Simulate an upcoming flight. The model will predict passenger demand based on price elasticity and recommend the exact aircraft required to maximize profit margins.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- INTERACTIVE SIMULATOR FORM ---
    with st.form("prediction_form"):
        st.markdown("#### Step 1: Input Upcoming Flight Parameters")
        form_col1, form_col2, form_col3 = st.columns(3)
        
        with form_col1:
            sim_route = st.selectbox("Route Category", df['Route_Category'].unique())
        with form_col2:
            sim_season = st.selectbox("Season", df['Season'].unique())
        with form_col3:
            # Set the default ticket price closer to reality so the elasticity works well
            sim_ticket = st.number_input("Average Ticket Price ($)", min_value=50, max_value=3000, value=500)
            
        submit_button = st.form_submit_button(label="Run Predictive Model", use_container_width=True)
        
    if submit_button:
        # --- THE UPGRADED 'ML' INFERENCE ENGINE (Price Elasticity) ---
        historical_slice = df[(df['Route_Category'] == sim_route) & (df['Season'] == sim_season)]
        
        if not historical_slice.empty:
            base_demand = historical_slice['Passengers'].mean()
            
            # 1. Calculate the historical average ticket price for this specific route/season
            historical_price = (historical_slice['Ticket_Revenue'] / historical_slice['Passengers']).mean()
            
            # 2. Calculate the price difference percentage
            price_change_pct = (sim_ticket - historical_price) / historical_price
            
            # 3. Apply Price Elasticity (Aviation PED is typically around -1.5)
            # Meaning a 10% price hike causes a 15% drop in demand
            elasticity = -1.5
            
            predicted_pax = int(base_demand * (1 + (price_change_pct * elasticity)))
            
            # 4. Floor it at 10 passengers so the model doesn't output negative people
            predicted_pax = max(10, predicted_pax)
            
            # Calculate the delta for the UI
            demand_delta = int(predicted_pax - base_demand)
        else:
            predicted_pax = 180
            demand_delta = 0
            
        # --- THE FIX: ROUTE-SPECIFIC COSTING ---
        # First, filter the dataset to only look at flights matching the simulated route length
        route_specific_df = df[df['Route_Category'] == sim_route]
        
        # Now, calculate the average cost for each plane ONLY on this specific type of route
        ac_stats = route_specific_df.groupby('Aircraft_Type').agg(
            capacity=('Aircraft_Capacity', 'max'),
            avg_cost=('Total_Cost', 'mean')
        ).reset_index()
        
        # Simulate assigning this exact flight to every plane in the fleet
        results = []
        for index, row in ac_stats.iterrows():
            ac = row['Aircraft_Type']
            cap = row['capacity']
            cost = row['avg_cost']
            
            actual_pax = min(predicted_pax, cap)
            projected_revenue = actual_pax * sim_ticket
            projected_profit = projected_revenue - cost
            margin = (projected_profit / projected_revenue) * 100 if projected_revenue > 0 else 0
            
            results.append({
                'Aircraft': ac,
                'Capacity': cap,
                'Projected Profit': projected_profit,
                'Projected Margin': margin
            })
            
        sim_df = pd.DataFrame(results).sort_values(by='Projected Profit', ascending=False)
        best_plane = sim_df.iloc[0]
        
        # --- DISPLAY RESULTS ---
        st.markdown("#### Step 2: Model Output & Recommendation")
        
        pred_col1, pred_col2 = st.columns(2)
        with pred_col1:
            # Show exactly how the price change affected the demand
            st.metric("Predicted Passenger Demand", f"{predicted_pax} Passengers", 
                      delta=f"{demand_delta} vs historical average", delta_color="normal")
            
        with pred_col2:
            st.markdown(f"""
                <div class="ai-box">
                    <div class="ai-title">🤖 Recommended Aircraft: {best_plane['Aircraft']}</div>
                    <div class="alert-text">
                        By assigning the <strong>{best_plane['Aircraft']}</strong>, we can absorb the predicted {predicted_pax} passengers while achieving a <strong>{best_plane['Projected Margin']:.1f}% Profit Margin</strong>. 
                        Larger aircraft would incur massive empty-seat costs, and smaller aircraft would leave ticket revenue on the table.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- THE PROOF CHART ---
        st.markdown("#### Financial Simulation Across Entire Fleet")
        
        def get_color(profit, aircraft):
            if aircraft == best_plane['Aircraft']: return '#c6a87c' # Gold
            elif profit < 0: return '#d50032' # Red
            else: return '#4a4a4a' # Grey
                
        sim_df['Color'] = sim_df.apply(lambda x: get_color(x['Projected Profit'], x['Aircraft']), axis=1)
        
        fig_sim = px.bar(sim_df, x='Aircraft', y='Projected Profit', 
                         color='Aircraft', color_discrete_map=dict(zip(sim_df['Aircraft'], sim_df['Color'])),
                         text_auto='.2s')
        
        fig_sim.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Breakeven")
        fig_sim.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                              xaxis_title="", yaxis_title="Projected Net Profit ($)", showlegend=False,
                              font=dict(family="Montserrat, sans-serif"))
        st.plotly_chart(fig_sim, use_container_width=True)