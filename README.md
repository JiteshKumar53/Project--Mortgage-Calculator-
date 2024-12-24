# Mortgage Calculator

A modern, user-friendly mortgage calculator built with Python and Tkinter. This application helps users calculate mortgage payments with support for multiple currencies, automatic/manual down payment options, and PDF export functionality. The calculator specially focuses on demonstrating the significant benefits of making extra mortgage payments, helping users make informed financial decisions.

## Features

### Currency Support
- Default: Swedish Krona (SEK)
- Multiple Currency Options:
  - SEK (kr) - Swedish Krona
  - USD ($) - US Dollar
  - EUR (€) - Euro
  - CAD (C$) - Canadian Dollar
  - AUD (A$) - Australian Dollar
  - INR (₹) - Indian Rupee
  - JPY (¥) - Japanese Yen
  - GBP (£) - British Pound

### Loan Calculation Features
- **Down Payment Options**
  - Auto (15% calculation)
  - Manual input
  - Dynamic loan amount updates

- **Interest and Terms**
  - Default interest rate: 4.5%
  - Customizable loan term
  - Monthly house fee option
  - Extra payment analysis

- **Payment Breakdown**
  - Principal payment
  - Interest payment
  - Total monthly payment
  - Extra payment impact

### Extra Payment Analysis
- Time saved calculation
- Interest saved computation
- Updated loan payoff time

### PDF Export
- Detailed payment breakdown
- Loan details summary
- Extra payment impact analysis
- Automatic file naming with date
- Exports saved in dedicated folder

## Benefits of Extra Mortgage Payments

This calculator helps you understand how extra payments can significantly impact your mortgage:

### Financial Benefits Visualization
- **Reduced Loan Term**: See exactly how many years and months you can save off your mortgage
- **Interest Savings**: Calculate the total amount saved in interest payments
- **Early Payoff**: Visualize your new loan payoff date with extra payments
- **Monthly Breakdown**: Compare regular vs. extra payment scenarios

### Real-Time Impact Analysis
- Instantly see how different extra payment amounts affect your mortgage
- Compare multiple scenarios to find the optimal extra payment amount
- Understand the long-term financial impact of your decisions
- View side-by-side comparisons of payment strategies

### Strategic Planning Tools
- **Payoff Timeline**: Track how extra payments accelerate your mortgage payoff
- **Savings Calculator**: Monitor accumulated interest savings over time
- **Payment Flexibility**: Test different extra payment amounts to fit your budget
- **Long-term Benefits**: Understand the compound effect of consistent extra payments

### Example Scenarios
1. **Small Extra Payments**
   - Even an extra $100/month can save years off your mortgage
   - See reduced total interest paid
   - Track accelerated equity building

2. **Lump Sum Contributions**
   - Calculate the impact of annual bonuses
   - Analyze tax refund applications
   - Plan strategic extra payments

3. **Bi-Weekly Payments**
   - Understand the impact of more frequent payments
   - See how payment timing affects total interest
   - Calculate accelerated payment benefits

## Installation

1. **Prerequisites**
   - Python 3.8 or higher
   - pip (Python package installer)

2. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd Project-(Mortgage-Calculator)
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Application**
   ```bash
   python mortgage_calculator_new.py
   ```

2. **Calculate Mortgage**
   - Select your preferred currency
   - Enter loan seeking amount
   - Choose down payment method (Auto 15% or Manual)
   - Set interest rate (default 4.5%)
   - Enter loan term in years
   - Add monthly house fee (optional)
   - Include extra monthly payment (optional)
   - Click "Calculate"

3. **View Results**
   - Monthly payment breakdown
   - Interest and principal portions
   - Impact of extra payments
   - Total interest saved
   - Time saved on loan term

4. **Export Results**
   - Click "Export PDF"
   - PDF saved in 'exports' folder
   - Filename includes current date
   - Multiple saves supported

## File Structure
```
Project-(Mortgage-Calculator)/
├── mortgage_calculator_new.py    # Main application file
├── requirements.txt              # Python dependencies
├── README.md                     # Documentation
└── exports/                      # PDF export directory
    └── mortgage_calculation_*.pdf
```

## Key Features in Detail

### Down Payment Calculation
- **Auto Mode (15%)**
  - Automatically calculates 15% of loan seeking amount
  - Updates dynamically with loan amount changes
  
- **Manual Mode**
  - Free input of down payment amount
  - Real-time loan amount updates

### Payment Analysis
- **Monthly Breakdown**
  - Principal payment amount
  - Interest payment amount
  - Extra payment amount
  - Monthly house fee
  - Total monthly payment

- **Extra Payment Impact**
  - Reduced loan term calculation
  - Interest savings computation
  - Updated payoff timeline

### Currency Handling
- Dropdown menu for currency selection
- Full currency names displayed
- Proper symbol formatting
- Automatic value updates on currency change

### Loan Payoff Calculation
- **Simple Formula Approach**
  - Base payoff time = Loan Amount / Principal Payment
  - With extra payments = Loan Amount / (Principal + Extra Payment)
  - Provides clear, straightforward estimation of loan term

### Time Saved Calculation
- **Comparative Analysis**
  - Calculates base payoff time without extra payments
  - Computes accelerated payoff time with extra payments
  - Time saved = Base payoff time - Accelerated payoff time
  - Shows exact years and months saved

### Example Calculations
1. **Without Extra Payments**
   - Loan Amount: 1,200,000
   - Principal Payment: 10,000/month
   - Payoff Time = 1,200,000/10,000 = 120 months (10 years)

2. **With Extra Payments**
   - Extra Payment: 2,000/month
   - Total Monthly Payment: 12,000
   - New Payoff Time = 1,200,000/12,000 = 100 months (8 years, 4 months)
   - Time Saved = 20 months (1 year, 8 months)

## Contributing

Feel free to contribute to this project:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is open source and available under the MIT License.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
