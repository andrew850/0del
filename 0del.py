import streamlit as st
import pandas as pd
import io
from datetime import datetime

def main():
    st.title("AdLib Critical Pacing Tracker")
    st.write("Upload a CSV file to find all campaigns where 'Spend Yesterday' equals 0")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.write(f"**Total rows in file:** {len(df)}")
            
            if 'Spend Yesterday' in df.columns:
                zero_spend_rows = df[df['Spend Yesterday'] == 0]
                
                # Categorize zero spend campaigns
                active_zero_spend = zero_spend_rows.copy()
                off_campaigns = pd.DataFrame()
                expired_campaigns = pd.DataFrame()
                future_start_campaigns = pd.DataFrame()
                critical_campaigns = pd.DataFrame()
                
                if 'Campaign Status' in df.columns:
                    off_campaigns = zero_spend_rows[zero_spend_rows['Campaign Status'] == 'Off']
                    active_zero_spend = zero_spend_rows[zero_spend_rows['Campaign Status'] != 'Off']
                
                if 'Campaign End Date' in df.columns:
                    df['Campaign End Date'] = pd.to_datetime(df['Campaign End Date'], errors='coerce')
                    today = datetime.now().date()
                    expired_mask = df['Campaign End Date'].dt.date < today
                    expired_campaigns = zero_spend_rows[zero_spend_rows.index.isin(df[expired_mask].index)]
                    active_zero_spend = active_zero_spend[~active_zero_spend.index.isin(expired_campaigns.index)]

                if 'Campaign Start Date' in df.columns:
                    df['Campaign Start Date'] = pd.to_datetime(df['Campaign Start Date'], errors='coerce')
                    future_start_mask = df['Campaign Start Date'].dt.date >= today
                    future_start_campaigns = zero_spend_rows[zero_spend_rows.index.isin(df[future_start_mask].index)]
                    active_zero_spend = active_zero_spend[~active_zero_spend.index.isin(future_start_campaigns.index)]

                # Find critical campaigns from remaining active campaigns: running >2 days with zero total spend
                from datetime import timedelta
                two_days_ago = today - timedelta(days=2)

                if 'Campaign Start Date' in df.columns:
                    # Check for total spend column (try common variants)
                    spend_columns = ['Spend', 'Total Spend', 'Lifetime Spend', 'Campaign Spend']
                    spend_col = None
                    for col in spend_columns:
                        if col in df.columns:
                            spend_col = col
                            break

                    if spend_col is not None:
                        old_start_mask = df['Campaign Start Date'].dt.date < two_days_ago
                        zero_total_spend_mask = df[spend_col] == 0
                        # Only consider campaigns from active_zero_spend (which already excludes Off/expired/future)
                        critical_mask = old_start_mask & zero_total_spend_mask
                        critical_campaigns = active_zero_spend[active_zero_spend.index.isin(df[critical_mask].index)]
                        active_zero_spend = active_zero_spend[~active_zero_spend.index.isin(critical_campaigns.index)]
                
                st.write(f"**Total rows with Spend Yesterday = 0:** {len(zero_spend_rows)}")
                st.write(f"**🚨 CRITICAL: Old campaigns with zero total spend:** {len(critical_campaigns)}")
                st.write(f"**Active campaigns with zero spend:** {len(active_zero_spend)}")
                st.write(f"**Campaigns with status 'Off':** {len(off_campaigns)}")
                st.write(f"**Expired campaigns:** {len(expired_campaigns)}")
                st.write(f"**Campaigns with future start dates:** {len(future_start_campaigns)}")
                
                if len(zero_spend_rows) > 0:
                    if len(critical_campaigns) > 0:
                        st.subheader("🚨 CRITICAL: Campaigns Running >2 Days with Zero Total Spend")
                        if 'Agency Name' in critical_campaigns.columns:
                            critical_agency_counts = critical_campaigns['Agency Name'].value_counts()
                            st.dataframe(critical_agency_counts.reset_index().rename(columns={'index': 'Agency Name', 'Agency Name': 'Critical Zero Spend Count'}))
                        st.dataframe(critical_campaigns)

                    if len(active_zero_spend) > 0:
                        st.subheader("⚠️ Active Campaigns with Zero Spend (Needs Attention)")
                        if 'Agency Name' in active_zero_spend.columns:
                            agency_counts = active_zero_spend['Agency Name'].value_counts()
                            st.dataframe(agency_counts.reset_index().rename(columns={'index': 'Agency Name', 'Agency Name': 'Active Zero Spend Count'}))
                        st.dataframe(active_zero_spend)
                    
                    if len(off_campaigns) > 0:
                        st.subheader("📴 Campaigns with Status 'Off' (Expected Zero Spend)")
                        st.dataframe(off_campaigns)
                    
                    if len(expired_campaigns) > 0:
                        st.subheader("📅 Expired Campaigns (Expected Zero Spend)")
                        st.dataframe(expired_campaigns)

                    if len(future_start_campaigns) > 0:
                        st.subheader("🚀 Campaigns with Future Start Dates (Expected Zero Spend)")
                        st.dataframe(future_start_campaigns)
                    
                    csv_buffer = io.StringIO()
                    zero_spend_rows.to_csv(csv_buffer, index=False)
                    csv_string = csv_buffer.getvalue()
                    
                    st.download_button(
                        label="Download All Zero Spend Results as CSV",
                        data=csv_string,
                        file_name="zero_spend_campaigns.csv",
                        mime="text/csv"
                    )
                    
                    if len(active_zero_spend) > 0:
                        active_csv_buffer = io.StringIO()
                        active_zero_spend.to_csv(active_csv_buffer, index=False)
                        active_csv_string = active_csv_buffer.getvalue()
                        
                        st.download_button(
                            label="Download Active Zero Spend Campaigns Only",
                            data=active_csv_string,
                            file_name="active_zero_spend_campaigns.csv",
                            mime="text/csv"
                        )
                else:
                    st.success("No campaigns found with zero spend yesterday!")
                    
            else:
                st.error("'Spend Yesterday' column not found in the uploaded file.")
                st.write("Available columns:", list(df.columns))
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()