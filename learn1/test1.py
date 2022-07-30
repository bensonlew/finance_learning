import numpy as np
import pandas as pd
import quandl as q

q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")

msft_data.resample("W").mean()


