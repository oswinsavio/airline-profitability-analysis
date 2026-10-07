\#Emirates Route Profitability \& ML Fleet Optimization



\*\*Live Dashboard:\*\* https://oswin-airline-profitability-analysis.streamlit.app



\## Business Problem

Airlines operate on razor-thin margins. While wide-body aircraft generate massive revenue during peak seasons, their high fixed operating costs cause severe financial bleeding when passenger load factors drop during off-peak months. 



\## The Solution

I built an end-to-end Machine Learning simulation dashboard in Python and Streamlit to diagnose seasonal margin exposure and dynamically optimize fleet allocation.



\### Tier 1: Executive Overview

\* Analyzes global operations, system-wide financial health, and cost composition (fuel, maintenance, crew).

\* Identifies vulnerability points where operating costs outpace revenue generation.



\### Tier 2: Route \& Seasonality Diagnostics

\* Interactive filtering to isolate the specific passenger load factor breaking points for different aircraft classes.

\* Identifies exactly where narrow-body vs. wide-body aircraft transition from profitable to loss-making.



\### Tier 3: ML Fleet Optimization Simulator

\* A predictive inference engine that simulates upcoming flights.

\* Utilizes \*\*Price Elasticity of Demand (-1.5 PED)\*\* to adjust passenger forecasts based on ticket pricing.

\* Iterates through the entire fleet's route-specific operating costs to recommend the exact aircraft that maximizes net profit margin.



\## Tech Stack

\* \*\*Python\*\* (Pandas, NumPy)

\* \*\*Streamlit\*\* (UI/UX, Web Deployment)

\* \*\*Plotly\*\* (Interactive Data Visualization)

