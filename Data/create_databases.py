from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
import os

# Symbols to extract rates
symbol_array = ["US500", "US100", "US30"]

# Initialize the bounds between MetaTrader 5 and Python
mt5.initialize()

# create dictionary for timeframe constant to be used for appending filename while saving the files
timeframe_names = {
    mt5.TIMEFRAME_D1: "D1",
    mt5.TIMEFRAME_H1: "H1",
    mt5.TIMEFRAME_H4: "H4",
    mt5.TIMEFRAME_M15: "M15",
    mt5.TIMEFRAME_M5: "M5",
    mt5.TIMEFRAME_M30: "M30",
    mt5.TIMEFRAME_M1: "M1"
    # Add more constants as needed
}
def get_rates(symbol, number_of_data=10_000, timeframe=mt5.TIMEFRAME_D1):
    # Compute now date
    from_date = datetime.now()

    # Extract n rates before now
    rates = mt5.copy_rates_from(symbol, timeframe, from_date, number_of_data)

    # Transform array into a DataFrame
    df_rates = pd.DataFrame(rates)
    #print(df_rates)
    # Convert number format of the date into date format
    df_rates["time"] = pd.to_datetime(df_rates["time"], unit="s")
    df_rates = df_rates.set_index("time")
    return df_rates

for symbol in symbol_array:
    for name, value in timeframe_names.items():
        #print(value)
        df = get_rates(symbol, number_of_data=30_000, timeframe=name)
        # !! You can't import more than 99.999 rows in one request
        #df = get_rates("AUDUSD", number_of_data=30_000, timeframe=mt5.TIMEFRAME_D1)
        #df = get_rates("AUDUSD", number_of_data=30_000, timeframe=mt5.TIMEFRAME_H4)
        #df = get_rates("AUDUSD", number_of_data=30_000, timeframe=mt5.TIMEFRAME_H1)
        #df = get_rates("AUDUSD", number_of_data=30_000, timeframe=mt5.TIMEFRAME_M15)
        #df = get_rates("AUDUSD", number_of_data=99_000, timeframe=mt5.TIMEFRAME_M30)

        # Display the data
        #print(df)

        # Put where you want to save the database



#input("Write the path to store the file if you want to (if not, just press enter):")
        save_path = symbol+"-"+value
        # If the user provided a filename, save the DataFrame under the "Data" directory
        if save_path:
            data_dir = "Data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            # Ensure the trailing slash in the directory path
            if not data_dir.endswith('/'):
                data_dir += '/'

            # Save the DataFrame to the specified path
            df.to_csv(os.path.join(data_dir, save_path))




###### Exercise
#- Do the same thing, for one of the 3 other function (copy_rates_range, copy_ticks_from or copy_ticks_range)