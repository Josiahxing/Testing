import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Define functions for calculations
def get_sku(scanned_lpn, inventory_df):
    if scanned_lpn == "":
        return ""
    result = inventory_df[inventory_df['LPN'] == scanned_lpn]['Sku']
    return result.values[0] if not result.empty else "Incorrect"

def loc_check(scanned_loc, scanned_lpn, inventory_df):
    if scanned_loc == "" or scanned_lpn == "":
        return ""
    if not inventory_df[(inventory_df['Location'] == scanned_loc) & (inventory_df['LPN'] == scanned_lpn)].empty:
        return "Correct"
    elif not inventory_df[inventory_df['LPN'] == scanned_lpn].empty:
        correct_loc = inventory_df[inventory_df['LPN'] == scanned_lpn]['Location'].values[0]
        return f"Incorrect - Should be at {correct_loc}"
    else:
        return "Incorrect"

def qty_remaining_lpn(scanned_loc, scanned_lpn, loc_check_result, inventory_df, cycle_count_df):
    if scanned_loc == "" or scanned_lpn == "":
        return ""
    if loc_check_result == "Incorrect":
        return "Incorrect"
    inventory_qty = inventory_df[inventory_df['LPN'] == scanned_lpn]['Qty'].sum()
    scanned_qty = cycle_count_df[cycle_count_df['Scanned LPN'] == scanned_lpn]['QTY Scanned'].sum()
    return inventory_qty - scanned_qty

def qty_remaining_loc(scanned_loc, inventory_df, cycle_count_df):
    if scanned_loc == "":
        return ""
    inventory_qty = inventory_df[inventory_df['Location'] == scanned_loc]['Qty'].sum()
    scanned_qty = cycle_count_df[cycle_count_df['Scanned LOC'] == scanned_loc]['QTY Scanned'].sum()
    return inventory_qty - scanned_qty

def location_in_picking(scanned_loc, carton_billing_df):
    if scanned_loc == "":
        return ""
    return "In Picking" if scanned_loc in carton_billing_df['Location'].values else "Not In Picking"

# Streamlit app layout
st.title('Cycle Count Auditing Tool')

uploaded_file = st.file_uploader("Choose a file", type="xlsx")
if uploaded_file is not None:
    cisco_inventory_df = pd.read_excel(uploaded_file, sheet_name='CiscoInventorySnapshot')
    
    # Create a DataFrame to simulate the CycleCount sheet
    cycle_count_df = pd.DataFrame(columns=[
        'Scanned LOC', 'Scanned LPN', 'QTY Scanned', 'Short Comment', 'Comment', 'Timestamp', 
        'SKU', 'LOC Check', 'QTY Remaining LPN', 'QTY Remaining in LOC', 'Location In Picking?', 
        'Missing LPN\'s By LOC'
    ])
    
    # Perform calculations
    cycle_count_df['SKU'] = cycle_count_df['Scanned LPN'].apply(lambda x: get_sku(x, cisco_inventory_df))
    cycle_count_df['LOC Check'] = cycle_count_df.apply(lambda row: loc_check(row['Scanned LOC'], row['Scanned LPN'], cisco_inventory_df), axis=1)
    cycle_count_df['QTY Remaining LPN'] = cycle_count_df.apply(lambda row: qty_remaining_lpn(row['Scanned LOC'], row['Scanned LPN'], row['LOC Check'], cisco_inventory_df, cycle_count_df), axis=1)
    cycle_count_df['QTY Remaining in LOC'] = cycle_count_df['Scanned LOC'].apply(lambda x: qty_remaining_loc(x, cisco_inventory_df, cycle_count_df))
    cycle_count_df['Location In Picking?'] = cycle_count_df['Scanned LOC'].apply(lambda x: location_in_picking(x, cisco_inventory_df))
    
    st.dataframe(cycle_count_df)
