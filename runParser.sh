#!/bin/bash

# Step 1: Remove existing .dat files to ensure a clean start
echo "Removing old .dat files..."
rm -f Item.dat User.dat Category.dat Item_Category.dat Bid.dat

# Step 2: Run the Python parser to generate sanitized .dat files
echo "Running Python parser..."
python3 skeleton_parser.py ebay_data/items-*.json

# Step 3: Recreate SQLite tables and import data using load.txt
echo "Recreating SQLite tables and importing data..."
sqlite3 auctionbase.db <<EOF
.read create.sql
.read load.txt
EOF

# Step 4: Confirm completion
echo "Data parsing and SQLite import complete."