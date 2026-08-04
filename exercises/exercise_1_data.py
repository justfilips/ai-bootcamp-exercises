"""
Exercise 1: Python & Data Handling
===================================

This exercise has three levels. Complete as far as you can.
Each level builds on the previous one.

- BASE: Pure Python (no libraries required)
- STANDARD: Use pandas for data analysis
- ADVANCED: Optimization and edge-case handling

Run: python exercises/exercise_1_data.py
"""

from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "support_tickets.csv"
OUTPUT_PATH = Path(__file__).parent.parent / "output"


# ============================================================
# BASE LEVEL — Pure Python (no external libraries needed)
# ============================================================

def load_csv_manual(filepath: str) -> list[dict]:
    import csv
    #creating a list type because thats what the function expects to return
    rows = []
    with open(filepath, mode='r') as file:
        #first loads fieldnames, then processes the rows of data
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

def count_by_status(rows: list[dict]) -> dict:
    status_counts = {}
    for row in rows:
        #get the status column value
        status = row.get('status', 'unknown')
        #counts every instance of each status in dict
        status_counts[status] = status_counts.get(status, 0) + 1
    return status_counts

def filter_by_priority(rows: list[dict], priority: str) -> list[dict]:
    filtered = []
    
    for row in rows:
        #get priority column value
        row_priority = row.get('priority', '')
        if row_priority.lower() == priority.lower():
            #if matches the needed priority then add row to list
            filtered.append(row)
    return filtered

def find_missing_descriptions(rows: list[dict]) -> list[str]:
    missing_ids = []
    
    for row in rows:
        desc = row.get('description', '')
        if desc.strip() == '':
            missing_ids.append(row.get('ticket_id', 'unknown'))
    return missing_ids

# ============================================================
# STANDARD LEVEL — Pandas-based analysis
# ============================================================

def load_data(filepath: str):
    """Load the CSV file and return a pandas DataFrame."""
    import pandas as pd
    return pd.read_csv(filepath)


def clean_data(df):
    """
    Clean the dataset:
    1. Remove rows where 'description' is empty or null.
    2. Normalize 'priority' column to lowercase: low, medium, high, critical.
    3. Parse 'created_at' into datetime format.

    Return the cleaned DataFrame.
    """
    import pandas as pd

    df = df.copy()

    # 1. Remove rows where 'description' is empty or null
    #takes only the non empty rows
    df = df[df["description"].notna() & (df["description"].astype(str).str.strip() != "")]

    # 2. Normalize 'priority' to lowercase
    df["priority"] = df["priority"].astype(str).str.strip().str.lower()

    # 3. Parse 'created_at' into datetime format
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    return df


def tickets_per_month(df) -> dict:
    """Return the number of tickets created per month (as a dict or Series)."""
    months = df["created_at"].dropna().dt.to_period("M")
    counts = months.value_counts().sort_index()

    result = {}
    for month, count in counts.items():
        result[str(month)] = int(count)
    return result


def avg_resolution_time_by_priority(df) -> dict:
    """
    Return the average resolution time (in hours) per priority level.
    Resolution time = resolved_at - created_at
    """
    import pandas as pd

    df = df.copy()
    df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce")

    resolved = df.dropna(subset=["created_at", "resolved_at"])
    resolved["resolution_hours"] = (resolved["resolved_at"] - resolved["created_at"]).dt.total_seconds() / 3600

    result = resolved.groupby("priority")["resolution_hours"].mean().round(2)
    return result.to_dict()


def open_share(statuses) -> float:
    open_count = 0
    for status in statuses:
        if status == "open":
            open_count = open_count + 1
    return open_count / len(statuses)


def highest_unresolved_category(df) -> str:
    """Return the category with the highest percentage of unresolved tickets."""
    #for each category, run open_share() on its statuses
    unresolved_share = df.groupby("category")["status"].apply(open_share)
    return unresolved_share.idxmax()


# ============================================================
# ADVANCED LEVEL — Optimization, edge cases, and design
# ============================================================

def load_data_chunked(filepath: str, chunk_size: int = 1000):
    """
    Load data in chunks for memory efficiency.
    Simulate handling a file that doesn't fit in memory.
    Return the fully processed DataFrame.
    """
    # TODO: Implement chunked reading
    pass


def detect_anomalies(df) -> list[dict]:
    """
    Find tickets with suspicious data:
    - resolved_at earlier than created_at
    - resolution time over 30 days
    - duplicate ticket titles from the same customer

    Return a list of dicts describing each anomaly found:
    [{"ticket_id": ..., "issue": "resolved before created"}, ...]
    """
    # TODO: Implement anomaly detection
    pass


def generate_summary_report(df) -> str:
    """
    Generate a formatted text report including:
    - Total tickets, open vs resolved
    - Busiest month
    - Slowest category to resolve
    - Top 3 customers by ticket count
    - Data quality score (% of rows with no issues)

    Return as a formatted string.
    """
    # TODO: Implement report generation
    pass


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Exercise 1: Python & Data Handling")
    print("=" * 60)

    # --- BASE ---
    print("\n--- BASE LEVEL ---")
    rows = load_csv_manual(DATA_PATH)
    if rows:
        print(f"Loaded {len(rows)} rows")
        print(f"Status counts: {count_by_status(rows)}")
        print(f"High priority tickets: {len(filter_by_priority(rows, 'high'))}")
        print(f"Missing descriptions: {find_missing_descriptions(rows)}")
    else:
        print("load_csv_manual() not implemented yet")

    # --- STANDARD ---
    print("\n--- STANDARD LEVEL ---")
    try:
        df = load_data(DATA_PATH)
    except ImportError:
        print("pandas not installed — skip with: pip install pandas")
        df = None
    if df is not None:
        df_clean = clean_data(df)
        print(f"Rows after cleaning: {len(df_clean)}")
        print(f"Tickets per month: {tickets_per_month(df_clean)}")
        print(f"Avg resolution time: {avg_resolution_time_by_priority(df_clean)}")
        print(f"Worst category: {highest_unresolved_category(df_clean)}")

        # Export
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(OUTPUT_PATH / "cleaned_tickets.csv", index=False)
        print(f"Exported to {OUTPUT_PATH}/cleaned_tickets.csv")
    else:
        print("load_data() not implemented yet")

    # --- ADVANCED ---
    print("\n--- ADVANCED LEVEL ---")
    if df is not None:
        anomalies = detect_anomalies(df_clean) if df_clean is not None else None
        if anomalies is not None:
            print(f"Anomalies found: {len(anomalies)}")
            for a in anomalies[:5]:
                print(f"  - Ticket {a.get('ticket_id')}: {a.get('issue')}")

        report = generate_summary_report(df_clean) if df_clean is not None else None
        if report:
            print(f"\n{report}")
        else:
            print("generate_summary_report() not implemented yet")
    else:
        print("Requires STANDARD level to be completed first")
