
import pandas as pd
# Was used to get inflation adjusted price

# 1. Load your files
prices = pd.read_csv("content_libraries/prices/streaming_prices.csv")
cpi = pd.read_csv("content_libraries/prices/cpi_data.csv")

# 2. Clean column names and whitespace
prices.columns = prices.columns.str.strip()
cpi.columns = cpi.columns.str.strip()

for col in cpi.select_dtypes(include="object").columns:
    cpi[col] = cpi[col].str.strip()

# 3. Parse subscription dates, e.g. Jul-2011
prices["date"] = pd.to_datetime(
    prices["date"], format="%b-%Y"
)

prices["year"] = prices["date"].dt.year
prices["period"] = (
    "M" + prices["date"].dt.month.astype(str).str.zfill(2)
)

prices["price"] = pd.to_numeric(prices["price"])

# 4. Select the correct CPI series
series_id = "CUUR0000SA0"

cpi = cpi[cpi["series_id"] == series_id].copy()

if cpi.empty:
    raise ValueError(
        f"No rows found for {series_id}. "
        "Check which series IDs are in your CPI file."
    )

cpi["year"] = pd.to_numeric(cpi["year"])
cpi["value"] = pd.to_numeric(cpi["value"], errors="coerce")

# Keep monthly observations only
cpi = cpi[cpi["period"].str.fullmatch(r"M\d{2}")].copy()
cpi = cpi.dropna(subset=["value"])

# 5. Determine the latest available CPI month
latest = cpi.sort_values(["year", "period"]).iloc[-1]
target_cpi = latest["value"]

# 6. Match each subscription to its historical CPI
prices = prices.merge(
    cpi[["year", "period", "value"]].rename(
        columns={"value": "historical_cpi"}
    ),
    on=["year", "period"],
    how="left",
    validate="many_to_one"
)

# 7. Calculate inflation-adjusted prices
prices["inflation_adjusted_price"] = (
    prices["price"] * target_cpi / prices["historical_cpi"]
).round(2)

# 8. Save the result
prices = prices.drop(columns=["year", "period"])

prices.to_csv("streaming_prices_adjusted.csv", index=False)

print(f"Prices expressed in {latest['period']} {int(latest['year'])} dollars")
print(prices.head())
print("Saved: streaming_prices_adjusted.csv")
