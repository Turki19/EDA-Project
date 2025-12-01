import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="US Cyber Attacks Dashboard", layout="wide")

# --- TITLE & INTRO ---
st.title("🛡️ US Cyber Attacks Dashboard (2014-2025)")
st.markdown("""
This interactive dashboard explores cybersecurity incidents targeting US institutions. 
Data is sourced from the **CISSM Cyber Events Database**.
""")

# --- DATA LOADING & CLEANING FUNCTION ---
@st.cache_data
def load_and_clean_data():
    # Load Data
    # Ensure the filename matches exactly what is in your folder
    try:
        entire_df = pd.read_excel('Cyber_Events_Database_2014_Oct_2025.xlsx')
    except FileNotFoundError:
        st.error("File not found! Please ensure 'Cyber_Events_Database_2014_Oct_2025.xlsx' is in the same directory.")
        return pd.DataFrame()

    # Filter for USA
    us_df = entire_df[entire_df['country'] == 'United States of America']

    # Select Features
    relevant_features = [
        'event_date', 'year', 'actor', 'actor_type',
        'organization', 'industry', 'motive', 'event_type',
        'country', 'actor_country', 'state'
    ]
    df = us_df[relevant_features].copy()

    # Drop Duplicates
    df.drop_duplicates(inplace=True)

    # --- CLEANING STEPS FROM NOTEBOOK ---
    
    # 1. Clean Actor Type Typos
    df['actor_type'] = df['actor_type'].str.title()
    
    # 2. Remove Rare Actors (Terrorist)
    df = df[~df['actor_type'].isin(['Terrorist'])]

    # 3. Clean Industry Names
    df['industry'] = df['industry'].str.title()
    rename_map = {
        'Professional, Scientific, And Technical Services': 'Tech/Science',
        'Administrative And Support And Waste Management And Remediation Services': 'Admin/Support',
        'Mining, Quarrying, And Oil And Gas Extraction': 'Oil and Gas',
        'Health Care And Social Assistance': 'Health Care',
        'Other Services (Except Public Administration)': 'Other Services',
        'Real Estate And Rental And Leasing': 'Real Estate',
        'Arts, Entertainment, And Recreation': 'Entertainment',
        'Accommodation And Food Services': 'Accommodation',
        'Transportation And Warehousing': 'Transportation',
        'Public Administration': 'Public Admin' 
    }
    df['industry'] = df['industry'].replace(rename_map)
    
    # Drop rare industries
    industries_to_drop = ['Agriculture, Forestry, Fishing And Hunting', 'Management Of Companies And Enterprises']
    df = df[~df['industry'].isin(industries_to_drop)]

    # 4. Clean Motives
    motives_to_drop = ['Political-espionage', 'Reputation', 'Protest,Political-Espionage']
    df = df[~df['motive'].isin(motives_to_drop)]
    
    # 5. Clean Event Types
    df['event_type'] = df['event_type'].str.strip()

    return df

# Load the data
df = load_and_clean_data()

if not df.empty:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Data")

    # Year Filter
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

    # Actor Type Filter
    all_actor_types = sorted(df['actor_type'].unique())
    selected_actors = st.sidebar.multiselect("Actor Type", all_actor_types, default=all_actor_types)

    # Industry Filter
    all_industries = sorted(df['industry'].unique())
    default_industries = ['Health Care', 'Public Admin', 'Tech/Science', 'Finance And Insurance'] # Top ones by default
    selected_industries = st.sidebar.multiselect("Target Industry", all_industries, default=[i for i in default_industries if i in all_industries])

    # APPLY FILTERS
    filtered_df = df[
        (df['year'] >= selected_years[0]) & 
        (df['year'] <= selected_years[1]) &
        (df['actor_type'].isin(selected_actors)) &
        (df['industry'].isin(selected_industries))
    ]

    # --- KPI ROW ---
    st.markdown("### Key Metrics")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Attacks", f"{len(filtered_df):,}")
    with c2:
        if not filtered_df.empty:
            top_actor = filtered_df['actor_type'].mode()[0]
            st.metric("Top Actor Type", top_actor)
    with c3:
        if not filtered_df.empty:
            top_target = filtered_df['industry'].mode()[0]
            st.metric("Most Targeted Industry", top_target)
    with c4:
        if not filtered_df.empty:
            top_motive = filtered_df['motive'].mode()[0]
            st.metric("Dominant Motive", top_motive)

    st.markdown("---")

    # --- TABS FOR VISUALIZATION ---
    tab1, tab2, tab3 = st.tabs(["📈 Trends over Time", "🕵️ The Attackers", "🎯 The Targets"])

    # ==========================
    # TAB 1: TRENDS
    # ==========================
    with tab1:
        st.subheader("Attack Volume and Motives Over Time")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Yearly Trend
            st.markdown("**Total Attacks per Year**")
            yearly_counts = filtered_df['year'].value_counts().sort_index()
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', ax=ax1, color='tab:blue')
            ax1.set_ylabel("Count")
            ax1.grid(True, alpha=0.3)
            st.pyplot(fig1)

        with col2:
            # 2. Motives Trend (Multi-line)
            st.markdown("**Evolution of Motives**")
            motive_trend = filtered_df.groupby(['year', 'motive']).size().reset_index(name='counts')
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            sns.lineplot(data=motive_trend, x='year', y='counts', hue='motive', marker='o', ax=ax2)
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)

    # ==========================
    # TAB 2: THE ATTACKERS
    # ==========================
    with tab2:
        st.subheader("Actor Profiles & Behavior")
        
        col3, col4 = st.columns([1, 1])

        with col3:
            # 3. Actor Count Bar Chart
            st.markdown("**Who is attacking?**")
            actor_counts = filtered_df['actor_type'].value_counts()
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            sns.barplot(x=actor_counts.values, y=actor_counts.index, palette='viridis', ax=ax3)
            ax3.set_xlabel("Count")
            st.pyplot(fig3)
            
            # Explanation Box
            st.info("💡 **Insight:** Criminals are the 'Noise' (High volume, opportunistic). Nation-States are the 'Signal' (Low volume, highly targeted).")

        with col4:
            # 4. The "Business Model Shift" (Criminals Only)
            st.markdown("**Deep Dive: Criminal Groups Shift (Exploitive vs Disruptive)**")
            
            # Logic from our previous conversation
            crim_df = df[(df['actor_type'] == 'Criminal') & (df['year'] >= 2017)].copy()
            if not crim_df.empty:
                evolution_data = pd.crosstab(crim_df['year'], crim_df['event_type'], normalize='index')
                
                fig4, ax4 = plt.subplots(figsize=(8, 5))
                evolution_data.plot.area(stacked=True, alpha=0.8, colormap='coolwarm', ax=ax4)
                ax4.set_title("Criminals: Shift from Disruption to Data Theft")
                ax4.set_ylabel("Proportion")
                ax4.axhline(0.5, color='white', linestyle='--', alpha=0.5)
                st.pyplot(fig4)
            else:
                st.write("Insufficient data for Criminal analysis in selected range.")

    # ==========================
    # TAB 3: THE TARGETS
    # ==========================
    with tab3:
        st.subheader("Industry Victimology")
        
        # 5. Horizontal Bar (Top Industries)
        st.markdown("**Most Targeted Industries**")
        fig5, ax5 = plt.subplots(figsize=(10, 5))
        sns.countplot(data=filtered_df, y='industry', order=filtered_df['industry'].value_counts().index[:10], palette='magma', ax=ax5)
        st.pyplot(fig5)

        st.markdown("---")

        # 6. Heatmap (Who targets Whom?)
        st.markdown("**Heatmap: Actor Type vs. Industry**")
        
        # Pivot table for heatmap
        if not filtered_df.empty:
            heatmap_data = pd.crosstab(filtered_df['actor_type'], filtered_df['industry'])
            
            fig6, ax6 = plt.subplots(figsize=(12, 6))
            sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Reds', linewidths=.5, ax=ax6)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig6)
        else:
            st.warning("No data available for heatmap with current filters.")

else:
    st.warning("Dataframe is empty. Please check the Excel file path.")