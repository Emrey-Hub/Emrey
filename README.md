# CVM Fund Data Scraper and Visualizer

## Description
This Python script scrapes financial data for investment funds from the official CVM (Comissão de Valores Mobiliários) website. It currently focuses on a single fund and saves as database file but is designed to be expanded for multi-fund analysis and comparison. 

## Features
- Web scraping of fund data from the CVM portal
- Data storage in SQLite database
- Data visualization using matplotlib
- Handling of paginated web content
- Robust error handling and data cleaning

## Installation
1. Ensure you have Python 3.7+ installed
2. Clone this repository:
git clone https://github.com/Emrey-Hub/Webscrap-Funds-Brazil.git
cvm-fund-scraper
3. Install required packages:
pip install -r requirements.txt

## Usage
Run the main script:
python cvmweb-test.py

## Data Structure
The script collects the following data points for each fund:
- Month
- Day (Dia)
- Quota
- Daily Funding (Captacao_no_Dia)
- Daily Redemption (Resgate_no_Dia)
- Net Worth (Patrimonio_Liquido)
- Total Portfolio (Total_da_Carteira)
- Total Number of Shareholders (No_Total_de_Cotistas)
- Next Date (Data_da_Proxima)

## Visualization
Currently, the script only creates a database file. The data visualization will be implemented in the next stages

## Future Plans
- Implement user interface for fund selection
- Add functionality for comparing multiple funds
- Expand visualization options

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
