companies20_ticker = ["AAPL",
"AMZN",
"GOOGL",
"MSFT",
"TSLA",
"FB",
"BRK.B",
"JNJ",
"V",
"JPM",
"PG",
"WMT",
"KO",
"NFLX",
"PFE",
"DIS",
"NVDA",
"BABA",
"ADBE",
"MA"]

companies20_keywords = [
'organizations-Apple', 'AAPL',
'organizations-Amazon', 'Amazon.com', 'AMZN',
'organizations-Alphabet', 'organizations-google', 'google', 'GOOGL',
'organizations-Microsoft', 'Microsoft', 'MSFT',
'organizations-Tesla', 'Tesla', 'TSLA',
'organizations-Facebook', 'Facebook', 'organizations-Meta', 'Meta', 'FB',
'organizations-Berkshire', 'Berkshire', 'Berkshire Hathaway', 'BRK.B',
'organizations-Johnson & Johnson', 'organizations-Johnson and Johnson', 'Johnson and Johnson',  'JNJ',
'organizations-visa', 'Visa inc',
'organizations-JPMorgan', 'JPMorgan', 'Chase', 'JPM',
'organizations-Procter', 'Procter', 'PG',
'organizations-Walmart', 'Walmart', 'WMT',
'organizations-The Coca-Cola', 'organizations-Coca', 'Coca Cola', 'KO',
'organizations-Netflix', 'Netflix', 'NFLX',
'organizations-Pfizer', 'Pfizer', 'PFE',
'organizations-Walt', 'Walt Disney',
'organizations-Nvidia', 'Nvidia' 'NVDA',
'organizations-Alibaba', 'Alibaba',
'organizations-Adobe', 'Adobe Inc', 'ADBE',
'organizations-Mastercard', 'Mastercard']

companies20_keyword_dict = {
'apple': ['organizations-Apple', 'AAPL'],
'amazon': ['organizations-Amazon', 'Amazon.com', 'AMZN'],
'google': ['organizations-Alphabet', 'organizations-google', 'google', 'GOOGL'],
'microsoft': ['organizations-Microsoft', 'Microsoft', 'MSFT'],
'tesla': ['organizations-Tesla', 'Tesla', 'TSLA'],
'facebook': ['organizations-Facebook', 'Facebook', 'organizations-Meta', 'Meta', 'FB'],
'berkshire': ['organizations-Berkshire', 'Berkshire', 'Berkshire Hathaway', 'BRK.B'],
'johnson': ['organizations-Johnson & Johnson', 'organizations-Johnson and Johnson', 'Johnson and Johnson',  'JNJ'],
'visa': ['organizations-Visa', 'Visa inc'],
'jpmorgan': ['organizations-JPMorgan', 'JPMorgan', 'Chase', 'JPM'],
'procter': ['organizations-Procter', 'Procter', 'PG'],
'walmart': ['organizations-Walmart', 'Walmart', 'WMT'],
'coca': ['organizations-The Coca-Cola', 'organizations-Coca', 'Coca Cola', 'KO'],
'netflix': ['organizations-Netflix', 'Netflix', 'NFLX'],
'pfizer': ['organizations-Pfizer', 'Pfizer', 'PFE'],
'disney': ['organizations-Walt', 'Walt Disney'],
'nvidia': ['organizations-Nvidia', 'Nvidia' 'NVDA'],
'alibaba': ['organizations-Alibaba', 'Alibaba'],
'adobe': ['organizations-Adobe', 'Adobe Inc', 'ADBE'],
'mastercard': ['organizations-Mastercard', 'Mastercard']}

company100_name = ['Apple Inc.', 'Alibaba Group Holding Ltd.', 'Chevron Corporation', 'Exelon Corporation', 'McDonald Corporation', 'PepsiCo Inc.', 'Sherwin-Williams Company', 'Unilever PLC', 'AbbVie Inc.', 'Bank of America Corporation', 'Dominion Energy, Inc.', 'Meta Platforms, Inc.', '3M Company', 'Pfizer Inc.', 'Snap Inc.', 'UnitedHealth Group Incorporated', 'Abbott Laboratories', 'BHP Group Ltd.', 'DuPont de Nemours, Inc.', 'Freeport-McMoRan Inc.', 'Morgan Stanley', 'The Procter & Gamble Company', 'China Petroleum & Chemical Corporation', 'Union Pacific Corporation', 'Accenture plc', 'BHP Group Ltd.', 'Deere & Company', 'General Electric Company', 'Microsoft Corporation', 'Prologis, Inc.', 'The Southern Company', 'United Parcel Service, Inc.', 'Adobe Inc.', 'BP plc', 'Diageo plc', 'Alphabet Inc.', 'NextEra Energy, Inc.', 'Philip Morris International Inc.', 'Simon Property Group, Inc.', 'Visa Inc.', 'Automatic Data Processing, Inc.', 'Berkshire Hathaway Inc.', 'Danaher Corporation', 'The Home Depot, Inc.', 'Newmont Corporation', 'Public Storage', 'Sempra Energy', 'Vale S.A.', 'American Electric Power Company, Inc.', 'Citigroup Inc.', 'The Walt Disney Company', 'Honeywell International Inc.', 'Netflix, Inc.', 'PetroChina Company Limited', 'AT&T Inc.', 'Verizon Communications Inc.', 'American Tower Corporation', 'Caterpillar Inc.', 'Digital Realty Trust, Inc.', 'JD.com, Inc.', 'National Grid plc', 'PayPal Holdings, Inc.', 'Target Corporation', 'Welltower Inc.', 'Amazon.com, Inc.', 'Crown Castle International Corp.', 'Duke Energy Corporation', 'Johnson & Johnson', 'NIKE, Inc.', 'Royal Dutch Shell plc', 'Toyota Motor Corporation', 'Wells Fargo & Company', 'Air Products and Chemicals, Inc.', 'Charter Communications, Inc.', 'Ecolab Inc.', 'JPMorgan Chase & Co.', 'NVIDIA Corporation', 'Rio Tinto Group', 'Thermo Fisher Scientific Inc.', 'Walmart Inc.', 'ASML Holding N.V.', 'Comcast Corporation', 'The Estée Lauder Companies Inc.', 'The Coca-Cola Company', 'Novo Nordisk A/S', 'Raytheon Technologies Corporation', 'T-Mobile US, Inc.', 'Xcel Energy Inc.', 'Broadcom Inc.', 'ConocoPhillips', 'Enbridge Inc.', 'Eli Lilly and Company', 'Novartis AG', 'SBA Communications Corporation', 'Tesla, Inc.', 'Exxon Mobil Corporation', 'American Water Works Company, Inc.', 'Costco Wholesale Corporation', 'Equinix, Inc.', 'Lowe\'s Companies, Inc.', 'Realty Income Corporation', 'Starbucks Corporation', 'Taiwan Semiconductor Manufacturing Company Limited', 'The Boeing Company', 'Cisco Systems, Inc.', 'Equinor ASA', 'Mastercard Incorporated', 'Oracle Corporation', 'The Charles Schwab Corporation', 'TotalEnergies SE']
company100_name_shorten = ['Apple', 'Alibaba', 'Chevron', 'Exelon', 'McDonald', 'PepsiCo', 'Sherwin-Williams', 'Unilever', 'AbbVie', 'bank of America', 'Dominion', 'facebook', '3M', 'Pfizer', 'Snap', 'UnitedHealth', 'Abbott', 'BHP', 'DuPont', 'Freeport-McMoRan', 'Stanley', 'Procter', 'China Petroleum', 'Union Pacific', 'Accenture', 'BHP', 'Deere', 'General Electric', 'Microsoft', 'Prologis', 'Southern company', 'United Parcel', 'Adobe', 'BP plc', 'Diageo', 'Alphabet', 'NextEra', 'Philip Morris', 'Simon Property', 'Visa Inc', 'Automatic Data', 'Berkshire', 'Danaher', 'Home Depot', 'Newmont', 'Public Storage', 'Sempra Energy', 'Vale', 'American Electric', 'Citigroup', 'Disney', 'Honeywell', 'Netflix', 'PetroChina', 'AT&T', 'Verizon', 'American Tower', 'Caterpillar', 'Digital Realty Trust', 'JD.com', 'National Grid', 'PayPal', 'Target', 'Welltower', 'Amazon', 'Crown Castle', 'Duke Energy', 'Johnson & Johnson', 'NIKE', 'Royal Dutch', 'Toyota', 'Wells Fargo', 'Air Products and Chemicals', 'Charter Communications', 'Ecolab', 'JPMorgan', 'NVIDIA', 'Rio Tinto', 'Thermo Fisher', 'Walmart', 'ASML', 'Comcast', 'Estee', 'Coca', 'Novo', 'Raytheon', 'T-Mobile', 'Xcel', 'Broadcom', 'ConocoPhillips', 'Enbridge', 'Eli Lilly', 'Novartis', 'SBA', 'Tesla', 'Exxon', 'Water Works', 'Costco', 'Equinix', 'Lowe\'s Companies', 'Realty Income', 'Starbucks', 'Taiwan Semiconductor', 'The Boeing Company', 'Cisco', 'Equinor', 'Mastercard', 'Oracle', 'Charles Schwab', 'TotalEnergies']

company100_ticker = ['AAPL', 'BABA', 'CVX', 'EXC', 'MCD', 'PEP', 'SHW', 'UL', 'ABBV', 'BAC', 'D', 'FB', 'MMM', 'PFE', 'SNAP', 'UNH', 'ABT', 'BBL', 'DD', 'FCX', 'MS', 'PG', 'SNPMF', 'UNP', 'ACN', 'BHP', 'DE', 'GE', 'MSFT', 'PLD', 'SO', 'UPS', 'ADBE', 'BP', 'DEO', 'GOOG', 'NEE', 'PM', 'SPG', 'V', 'ADP', 'BRK-A', 'DHR', 'HD', 'NEM', 'PSA', 'SRE', 'VALE', 'AEP', 'C', 'DIS', 'HON', 'NFLX', 'PTR', 'T', 'VZ', 'AMT', 'CAT', 'DLR', 'JD', 'NGG', 'PYPL', 'TGT', 'WELL', 'AMZN', 'CCI', 'DUK', 'JNJ', 'NKE', 'RDS-B', 'TM', 'WFC', 'APD', 'CHTR', 'ECL', 'JPM', 'NVDA', 'RIO', 'TMO', 'WMT', 'ASML', 'CMCSA', 'EL', 'KO', 'NVO', 'RTX', 'TMUS', 'XEL', 'AVGO', 'COP', 'ENB', 'LLY', 'NVS', 'SBAC', 'TSLA', 'XOM', 'AWK', 'COST', 'EQIX', 'LOW', 'O', 'SBUX', 'TSM', 'BA', 'CSCO', 'EQNR', 'MA', 'ORCL', 'SCHW', 'TTE']



