import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Custom CSS styling
st.markdown("""
    <style>
    /* Clean white main area */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Dark navy sidebar */
    [data-testid="stSidebar"] {
        background-color: #1d3557;
    }
    
    /* White sidebar text */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 15px !important;
        padding: 5px 0px !important;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: white !important;
        font-size: 20px !important;
    }
    
    /* Main titles */
    h1 {
        color: #1d3557 !important;
        border-bottom: 3px solid #457b9d;
        padding-bottom: 10px;
    }
    
    /* Subheaders */
    h2, h3 {
        color: #457b9d !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #f0f4f8;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricValue"] {
        color: #1d3557 !important;
        font-weight: bold !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ============================================
# IRELAND HOUSING CRISIS DASHBOARD
# ============================================

# Page configuration
st.set_page_config(
    page_title="Ireland Housing Crisis Analysis",
    page_icon="",
    layout="wide"
)

# Load all data
@st.cache_data
def load_data():
    rent = pd.read_csv("data/cleaned/rtb_rent_clean.csv")
    cso = pd.read_csv("data/cleaned/cso_housing_clean.csv")
    hea = pd.read_csv("data/cleaned/hea_enrolment_clean.csv")
    census = pd.read_csv("data/raw/census_2022_population.csv")
    stress = pd.read_csv("data/cleaned/stress_index.csv")
    ip_nationality = pd.read_csv("data/raw/ip_nationality_2024.csv")
    ip_backlog = pd.read_csv("data/raw/ip_backlog_2024.csv")
    abp = pd.read_csv("data/raw/abp_national.csv")
    return rent, cso, hea, census, stress, ip_nationality, ip_backlog, abp

rent, cso, hea, census, stress, ip_nationality, ip_backlog, abp = load_data()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.title(" Ireland Housing Crisis")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["Overview",
     "Rent Analysis", 
     "Supply Gap",
     "Student Demand",
     "Migration Pressure",
     "Planning Failure",
     "Stress Index"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources:**")
st.sidebar.markdown("- RTB Rent Index")
st.sidebar.markdown("- CSO Housing Completions")
st.sidebar.markdown("- HEA Student Enrolment")
st.sidebar.markdown("- IPO International Protection")
st.sidebar.markdown("- An Bord Plánála Statistics")

# ============================================
# PAGE 1 — OVERVIEW
# ============================================
if page == "Overview":
    st.title("Ireland Housing Crisis - Multi-Pillar Analysis")
    st.markdown("### A 5-Pillar Data-Driven Investigation")
    st.markdown("*Analysing rent growth, supply failure, student demand, migration pressure and planning system collapse across all 26 Irish counties 2019-2024*")
    st.markdown("---")

    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Avg Annual Rent Growth",
            value="7.3%",
            delta="National average 2019-2024"
        )
    with col2:
        st.metric(
            label="Shadow Supply",
            value="53,148",
            delta="Approved but never built"
        )
    with col3:
        st.metric(
            label="IP Backlog",
            value="22,548",
            delta="People waiting 1.5 years"
        )
    with col4:
        st.metric(
            label="Planning Delays",
            value="48 weeks",
            delta="Up 60% since 2019"
        )
    with col5:
        st.metric(
            label="Student-Rent Correlation",
            value="0.789",
            delta="Statistically significant"
        )

    st.markdown("---")

    # Overview chart — rent over time for key counties
    st.subheader(" Rent Trends — Key Counties 2019-2024")

    key_counties = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Leitrim', 'Longford']
    rent_filtered = rent[rent['county'].isin(key_counties)]

    fig = px.line(
        rent_filtered,
        x='year',
        y='avg_monthly_rent',
        color='county',
        title='Average Monthly Rent by County',
        labels={
            'avg_monthly_rent': 'Average Monthly Rent (€)',
            'year': 'Year',
            'county': 'County'
        },
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(" Key Findings")

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Rent Growth**
        National average rent grew 7.3% annually 
        between 2019-2024. Rural counties like 
        Longford and Leitrim hit hardest proportionally.
        """)
        st.info("""
        **Supply Failure**
        53,148 housing units approved by An Bord 
        Plánála were never built — a systemic 
        delivery failure beyond planning itself.
        """)
    with col2:
        st.info("""
        **Student Demand**
        International student numbers show 0.789 
        correlation with rent — statistically 
        significant at p<0.0001.
        """)
        st.info("""
        **Migration Pressure**
        22,548 IP applicants waiting 1.5 years 
        require ~8,199 housing units — equivalent 
        to building an entire new town.
        """)

    st.markdown("---")
    st.subheader("Evidence-Based Policy Recommendations")
    st.markdown("*Based on our 5-pillar analysis, here are data-driven solutions:*")

    rec1, rec2, rec3 = st.columns(3)

    with rec1:
        st.success("""
        Fix Shadow Supply
        
        53,148 units approved but never built.
        
        Recommendation: Government viability 
        financing fund for approved developments 
        stuck on financing grounds. Target: 
        convert 50% of shadow supply within 3 years.
        """)

        st.success("""
        Fix Planning Delays
        
        Processing time up 60% to 48 weeks.
        
        Recommendation: Automatic approval 
        if ABP misses statutory deadline. 
        Remove appeals as a blocking tactic 
        by introducing financial penalties 
        for frivolous objections.
        """)

    with rec2:
        st.success("""
        Student Accommodation
        
        0.789 correlation between international 
        students and rent proven statistically.
        
        Recommendation: Mandatory purpose-built 
        student accommodation for all HEI 
        expansions. No new international student 
        intake without corresponding bed supply.
        """)

        st.success("""
        IP Processing Reform
        
        22,548 people waiting 1.5 years 
        needing 8,199 housing units.
        
        Recommendation: Fast-track processing 
        to under 6 months. Regional dispersal 
        strategy - spread IPAS accommodation 
        across all 26 counties not just Dublin.
        """)

    with rec3:
        st.success("""
        Rural Housing Targets
        
        Leitrim 10.28% and Longford 10.18% 
        annual rent growth - fastest in Ireland.
        
        Recommendation: Dedicated social 
        housing targets for high-stress rural 
        counties. Current policy focuses on 
        Dublin while rural Ireland is being 
        quietly squeezed.
        """)

        st.success("""
        Post-Brexit Policy Gap
        
        Dublin III collapse means UK-rejected 
        applicants now enter full Irish system.
        
        Recommendation: Bilateral returns 
        agreement with UK. Ireland and UK 
        should negotiate replacement for 
        Dublin III cooperation framework.
        """)

    st.markdown("---")
    st.info("""
    Data Confidence Note: 
    Rent growth, supply gap, student correlation and planning delay findings 
    are based on verified official datasets. IP and migration figures represent 
    lower bound estimates due to data collection limitations around irregular arrivals.
    All recommendations are proportionate responses to the scale of evidence found.
    """)

    st.markdown("---")
    st.subheader("On-The-Ground Reality - Beyond What Data Can Capture")
    st.markdown("*Qualitative insights from direct operational experience working at a refuge centre in Galway, Ireland*")

    st.warning("""
    Important Note: The following observations are based on direct 
    real-world experience and corroborated by policy literature - but cannot 
    be fully quantified with currently available public datasets. They represent 
    known gaps in the official data picture.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Irregular Arrivals and Self-Presentation**
        
        Official IP statistics only capture applicants 
        at point of registration. In practice, individuals 
        arrive by various means - road, sea, air - and 
        self-present directly to Garda stations with no 
        documentation, claiming protection immediately.
        
        These individuals are recorded identically to 
        port-of-entry applicants in official data - making 
        it impossible to distinguish irregular from regular 
        arrivals in any public dataset.
        
        Data gap: True irregular arrival figures are 
        unknown. Official IP numbers are a lower bound.
        """)

        st.markdown("""
        **Multi-Country Asylum Applications**
        
        Individuals rejected in other countries - 
        including post-Brexit UK - are entering the 
        full Irish system. Pre-Brexit, Dublin III allowed 
        returns to the country of first EU entry. 
        Post-Brexit, that mechanism collapsed entirely.
        
        From January 2021 to June 2025, only 38 people 
        were successfully removed from the UK under 
        inadmissibility rules - effectively zero enforcement.
        
        Data gap: Prior country applications are not 
        recorded in Irish IP datasets.
        """)

    with col2:
        st.markdown("""
        **Processing Backlog as Housing Demand**
        
        The 79.5 week median processing time creates 
        sustained housing demand - applicants receive 
        government-provided accommodation for the entire 
        duration of their case, regardless of outcome.
        
        With appeal processes adding further time, total 
        system residence can exceed 3-4 years before 
        final determination. During this entire period, 
        housing demand is generated on the state.
        
        Data gap: Total system duration including 
        appeals is not publicly tracked per applicant.
        """)

        st.markdown("""
        **Nationality Concentration Not Captured**
        
        Official data shows national-level nationality 
        breakdowns - Nigeria 21.7%, Jordan 15.5%, 
        Pakistan 7.5%, Somalia 7.0%, Bangladesh 5.4%.
        
        Ground reality shows significant concentration 
        in specific accommodation centres and counties - 
        creating localised housing pressure invisible 
        in county-level statistics.
        
        Data gap: County-level nationality breakdown 
        is not available in public IPAS data.
        """)

    st.markdown("---")
    st.error("""
    The Core Policy Failure: Ireland's housing system was not designed 
    to absorb simultaneous demand shocks from:
    
    - 100,000 Ukrainian arrivals under EU Temporary Protection Directive 2022
    - Growing non-EU IP applications from conflict zones
    - Post-Brexit collapse of UK-Ireland returns cooperation
    - International student sector expansion without accommodation planning
    - Planning system deterioration reducing new supply
    
    Each factor alone would be manageable. All five simultaneously - without 
    coordinated policy response - created the crisis our data documents.
    """)


        # ============================================
# PAGE 2 — RENT ANALYSIS
# ============================================
elif page == "Rent Analysis":
    st.title(" Rent Analysis")
    st.markdown("### How have rents changed across Ireland?")
    st.markdown("---")

    # County selector
    selected_counties = st.multiselect(
        "Select counties to compare:",
        options=sorted(rent['county'].unique()),
        default=['Dublin', 'Cork', 'Galway', 'Leitrim', 'Longford']
    )

    if selected_counties:
        filtered = rent[rent['county'].isin(selected_counties)]

        # Line chart
        fig = px.line(
            filtered,
            x='year',
            y='avg_monthly_rent',
            color='county',
            title='Average Monthly Rent by County',
            labels={'avg_monthly_rent': 'Avg Monthly Rent (€)', 'year': 'Year'},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

        # Bar chart — latest year
        latest = rent[rent['year'] == rent['year'].max()]
        latest_filtered = latest[latest['county'].isin(selected_counties)]

        fig2 = px.bar(
            latest_filtered.sort_values('avg_monthly_rent', ascending=True),
            x='avg_monthly_rent',
            y='county',
            orientation='h',
            title=f'Rent Comparison {rent["year"].max()}',
            labels={'avg_monthly_rent': 'Avg Monthly Rent (€)', 'county': 'County'},
            color='avg_monthly_rent',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Growth table
        st.subheader(" Rent Growth Summary")
        rent_sorted = rent[rent['county'].isin(selected_counties)].sort_values(['county', 'year'])
        rent_sorted['growth'] = rent_sorted.groupby('county')['avg_monthly_rent'].pct_change() * 100
        growth_summary = rent_sorted.groupby('county').agg(
            avg_rent=('avg_monthly_rent', 'mean'),
            avg_growth=('growth', 'mean')
        ).round(2).reset_index()
        st.dataframe(growth_summary, use_container_width=True)

# ============================================
# PAGE 3 — SUPPLY GAP
# ============================================
elif page == "Supply Gap":
    st.title(" Housing Supply Gap")
    st.markdown("### Are we building enough homes?")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Built 2019-2024", "381,040", "Across all counties")
    with col2:
        st.metric("Shadow Supply", "53,148", "Approved but never built")
    with col3:
        st.metric("Build Rate", "29.3%", "Of approved units actually built")

    st.markdown("---")

    # Completions by county
    cso_total = cso.groupby('county')['housing_completions'].sum().reset_index()
    cso_total = cso_total.sort_values('housing_completions', ascending=True)

    fig = px.bar(
        cso_total,
        x='housing_completions',
        y='county',
        orientation='h',
        title='Total Housing Completions by County 2019-2024',
        labels={'housing_completions': 'Total Units Built', 'county': 'County'},
        color='housing_completions',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Completions over time
    fig2 = px.line(
        cso.groupby('year')['housing_completions'].sum().reset_index(),
        x='year',
        y='housing_completions',
        title='National Housing Completions Per Year',
        labels={'housing_completions': 'Units Built', 'year': 'Year'},
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Shadow supply
    st.subheader(" Shadow Supply — Approved But Never Built")
    abp_shadow = pd.read_csv("data/raw/abp_shadow_supply.csv")
    fig3 = px.bar(
        abp_shadow,
        x='year',
        y=['units_approved', 'units_built', 'shadow_supply'],
        title='Units Approved vs Built vs Shadow Supply',
        labels={'value': 'Units', 'year': 'Year'},
        barmode='group'
    )
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# PAGE 4 — STUDENT DEMAND
# ============================================
elif page == "Student Demand":
    st.title(" Student Demand Analysis")
    st.markdown("### Do international students drive rent increases?")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Int'l-Rent Correlation", "0.789", "Strong positive")
    with col2:
        st.metric("Statistical Significance", "p<0.0001", "Highly significant")

    st.markdown("---")

    # International vs domestic trend
    hea_national = hea.groupby('academic_year').agg(
        domestic=('domestic_students', 'sum'),
        international=('international_students', 'sum')
    ).reset_index()

    fig = px.line(
        hea_national,
        x='academic_year',
        y=['domestic', 'international'],
        title='National Student Enrolment Trends',
        labels={'value': 'Students', 'academic_year': 'Year'},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # By county
    st.subheader("International Students by County")
    hea_county = hea.groupby('county')['international_students'].mean().reset_index()
    hea_county = hea_county.sort_values('international_students', ascending=True)

    fig2 = px.bar(
        hea_county,
        x='international_students',
        y='county',
        orientation='h',
        title='Average International Students by County',
        labels={'international_students': 'Avg International Students', 'county': 'County'},
        color='international_students',
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 5 — MIGRATION PRESSURE
# ============================================

elif page == "Migration Pressure":
    st.title("Migration & International Protection")
    st.markdown("### The hidden housing demand from IP applicants")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pending Applications", "22,548", "As of Dec 2024")
    with col2:
        st.metric("Median Wait", "79.5 weeks", "1.5 years per person")
    with col3:
        st.metric("Housing Units Needed", "~8,199", "For current backlog")

    st.markdown("---")

    fig = px.bar(
        ip_nationality.sort_values('pct_2024', ascending=True),
        x='pct_2024',
        y='nationality',
        orientation='h',
        title='Top Nationalities - IP Applications 2024 (%)',
        labels={'pct_2024': 'Percentage (%)', 'nationality': 'Nationality'},
        color='pct_2024',
        color_continuous_scale='Blues',
        text='pct_2024'
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(plot_bgcolor='white', showlegend=False)
    st.plotly_chart(fig)

    st.subheader("System Backlog")
    st.dataframe(ip_backlog)

    st.warning("""
    Data Limitation: Official IP statistics record applicants at point 
    of registration. Irregular arrivals who self-present to Garda are recorded 
    identically to port-of-entry applicants - meaning these figures represent 
    a lower bound estimate of true housing demand.
    """)

    st.info("""
    Post-Brexit Impact: The collapse of Dublin III returns cooperation 
    between UK and Ireland means applicants previously managed through 
    UK-Ireland cooperation now enter the full Irish system - adding 
    sustained housing demand not anticipated in pre-2020 planning.
    """)



# ============================================
# PAGE 6 — PLANNING FAILURE
# ============================================
elif page == "Planning Failure":
    st.title(" Planning System Failure")
    st.markdown("### How planning delays are killing housing delivery")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Processing Time 2019", "30 weeks", "Baseline")
    with col2:
        st.metric("Processing Time 2023", "48 weeks", "+60% increase")
    with col3:
        st.metric("Statutory Compliance", "26%", "Down from 65%")

    st.markdown("---")

    # Processing time chart
    fig = px.line(
        abp,
        x='year',
        y='avg_weeks_to_decide',
        title='Average Planning Appeal Processing Time (Weeks)',
        labels={'avg_weeks_to_decide': 'Weeks', 'year': 'Year'},
        markers=True
    )
    fig.add_hline(y=18, line_dash="dash", 
                  annotation_text="Statutory Target (18 weeks)")
    st.plotly_chart(fig, use_container_width=True)

    # Compliance chart
    fig2 = px.bar(
        abp,
        x='year',
        y='pct_within_statutory_period',
        title='% Cases Resolved Within Statutory Period',
        labels={'pct_within_statutory_period': '% On Time', 'year': 'Year'},
        color='pct_within_statutory_period',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.error("""
     **Key Finding:** Planning appeal processing time increased 60% between 
    2019-2023. Only 26% of cases are now resolved within the statutory 
    objective period — down from 65%. Every week of delay costs developers 
    thousands in financing, making smaller developments unviable.
    """)

# ============================================
# PAGE 7 — STRESS INDEX
# ============================================
elif page == "Stress Index":
    st.title(" Housing Stress Index")
    st.markdown("### Which counties are under most housing pressure?")
    st.markdown("---")

    st.info("""
    **How the Stress Index is calculated:**
    Combines three metrics — rent level, rent growth rate, and supply pressure 
    — into a single composite score. Higher score = more stressed county.
    """)

    # Stress index bar chart
    stress_latest = stress[stress['year'] == stress['year'].max()]
    stress_latest = stress_latest.sort_values('stress_index', ascending=True)

    fig = px.bar(
        stress_latest,
        x='stress_index',
        y='county',
        orientation='h',
        title=f'Housing Stress Index by County ({stress["year"].max()})',
        labels={'stress_index': 'Stress Score', 'county': 'County'},
        color='stress_index',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Full stress table
    st.subheader(" Full Stress Index Data")
    st.dataframe(
        stress.sort_values('stress_index', ascending=False),
        use_container_width=True
    )

