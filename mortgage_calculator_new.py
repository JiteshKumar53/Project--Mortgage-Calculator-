# STEP 1: Imports and Dependencies
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime
from ttkbootstrap import Style
from reportlab.lib import colors
from tkinter import filedialog

# STEP 2: Main Calculator Class
class MortgageCalculator:
    def __init__(self, root):
        """Initialize the calculator"""
        self.root = root
        self.root.title("Mortgage Calculator")
        
        # Apply ttkbootstrap style
        style = Style(theme="cosmo")
        self.root = style.master
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(expand=True, fill='both')
        
        # Create left and right frames
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Initialize variables
        self.initialize_variables()
        
        # Create input panels (left side)
        self.create_currency_panel(left_frame)
        self.create_loan_details_panel(left_frame)
        self.create_calculate_panel(left_frame)
        
        # Create results panel (right side)
        self.create_results_panel(right_frame)

    # STEP 3: Input Fields Creation
    def create_currency_panel(self, parent):
        """Create currency selection panel"""
        currency_frame = ttk.LabelFrame(parent, text="Currency", padding=5)
        currency_frame.pack(fill='x', pady=5)
        
        # Define currencies with their symbols
        currencies = [
            ("SEK (kr)", "kr"),
            ("USD ($)", "$"),
            ("EUR (€)", "€"),
            ("CAD (C$)", "C$"),
            ("AUD (A$)", "A$"),
            ("INR (₹)", "₹"),
            ("JPY (¥)", "¥"),
            ("GBP (£)", "£")
        ]
        
        # Create and pack the label
        ttk.Label(currency_frame, text="Select Currency:").pack(side='left', padx=5)
        
        # Create the dropdown menu
        currency_menu = ttk.Combobox(
            currency_frame, 
            textvariable=self.currency_var,
            values=[curr[1] for curr in currencies],
            state='readonly',
            width=10
        )
        currency_menu.pack(side='left', padx=5)
        
        # Set the default value
        currency_menu.set("kr")
        
        # Add a label to show the full currency name
        currency_label = ttk.Label(currency_frame, textvariable=self.currency_name_var)
        currency_label.pack(side='left', padx=5)
        
        # Create a dictionary for currency names
        self.currency_names = {
            "kr": "Swedish Krona (SEK)",
            "$": "US Dollar (USD)",
            "€": "Euro (EUR)",
            "C$": "Canadian Dollar (CAD)",
            "A$": "Australian Dollar (AUD)",
            "₹": "Indian Rupee (INR)",
            "¥": "Japanese Yen (JPY)",
            "£": "British Pound (GBP)"
        }
        
        # Bind the selection event to update the currency name
        def update_currency_name(event):
            selected_symbol = self.currency_var.get()
            self.currency_name_var.set(self.currency_names.get(selected_symbol, ""))
        
        currency_menu.bind('<<ComboboxSelected>>', update_currency_name)

    def create_loan_details_panel(self, parent):
        """Create loan details panel"""
        # Loan Details
        loan_frame = ttk.LabelFrame(parent, text="Step 2: Enter Loan Details", padding=10)
        loan_frame.pack(fill='x', padx=5, pady=5)

        # Loan Seeking
        loan_seeking_frame = ttk.Frame(loan_frame)
        loan_seeking_frame.pack(fill='x', expand=True)
        ttk.Label(loan_seeking_frame, text="Loan Seeking For:").pack(side='left')
        self.loan_seeking_entry = ttk.Entry(loan_seeking_frame, textvariable=self.loan_seeking_var)
        self.loan_seeking_entry.pack(side='right', fill='x', expand=True)
        # Bind the loan seeking entry to update when value changes
        self.loan_seeking_var.trace_add('write', self.update_on_loan_seeking_change)

        # Down Payment
        down_payment_frame = ttk.Frame(loan_frame)
        down_payment_frame.pack(fill='x', expand=True)
        ttk.Label(down_payment_frame, text="Down Payment:").pack(side='left')
        
        # Down Payment Mode Selection
        self.down_payment_mode = tk.StringVar(value="auto")
        mode_frame = ttk.Frame(down_payment_frame)
        mode_frame.pack(side='left', padx=5)
        ttk.Radiobutton(mode_frame, text="Auto (15%)", 
                       variable=self.down_payment_mode, value="auto",
                       command=self.toggle_down_payment_mode).pack(side='left')
        ttk.Radiobutton(mode_frame, text="Manual", 
                       variable=self.down_payment_mode, value="manual",
                       command=self.toggle_down_payment_mode).pack(side='left')
        
        # Down Payment Entry
        self.down_payment_entry = ttk.Entry(down_payment_frame, textvariable=self.down_payment_var)
        self.down_payment_entry.pack(side='right', fill='x', expand=True)
        self.down_payment_entry.configure(state='disabled')  # Initially disabled
        
        # Bind the down payment entry to update loan amount when value changes
        self.down_payment_var.trace_add('write', self.update_loan_amount)
        
        # Loan Amount (display only)
        loan_amount_frame = ttk.Frame(loan_frame)
        loan_amount_frame.pack(fill='x', expand=True)
        ttk.Label(loan_amount_frame, text="Loan Amount:").pack(side='left')
        ttk.Entry(loan_amount_frame, textvariable=self.loan_amount_var, state='readonly').pack(side='right', fill='x', expand=True)

        # Interest Rate
        interest_frame = ttk.Frame(loan_frame)
        interest_frame.pack(fill='x', expand=True)
        ttk.Label(interest_frame, text="Interest Rate (%):").pack(side='left')
        self.interest_rate_entry = ttk.Entry(interest_frame, textvariable=self.interest_rate_var)
        self.interest_rate_entry.pack(side='right', fill='x', expand=True)

        # Principal Payment
        principal_frame = ttk.Frame(loan_frame)
        principal_frame.pack(fill='x', expand=True)
        ttk.Label(principal_frame, text="Principal Payment:").pack(side='left')
        self.principal_payment_entry = ttk.Entry(principal_frame, textvariable=self.principal_payment_var)
        self.principal_payment_entry.pack(side='right', fill='x', expand=True)

        # Extra Payment
        extra_frame = ttk.Frame(loan_frame)
        extra_frame.pack(fill='x', expand=True)
        ttk.Label(extra_frame, text="Extra Payment:").pack(side='left')
        self.extra_payment_entry = ttk.Entry(extra_frame, textvariable=self.extra_payment_var)
        self.extra_payment_entry.pack(side='right', fill='x', expand=True)

        # Monthly House Fee
        fee_frame = ttk.Frame(loan_frame)
        fee_frame.pack(fill='x', expand=True)
        ttk.Label(fee_frame, text="Monthly House Fee:").pack(side='left')
        self.monthly_fee_entry = ttk.Entry(fee_frame, textvariable=self.monthly_fee_var)
        self.monthly_fee_entry.pack(side='right', fill='x', expand=True)

    def create_calculate_panel(self, parent):
        """Create calculate panel"""
        # Calculation Buttons
        button_frame = ttk.LabelFrame(parent, text="Step 3: Calculate and Export", padding=10)
        button_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(button_frame, text="Calculate", command=self.calculate, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side='left')

    # STEP 4: Results Panel Creation
    def create_results_panel(self, parent):
        """Create the results display panel"""
        # Step 4: View Results
        results_frame = ttk.LabelFrame(parent, text="Step 4: View Results", padding=10)
        results_frame.pack(fill='x', padx=5, pady=5)

        # Monthly Payment and Total Interest
        monthly_payment_frame = ttk.Frame(results_frame)
        monthly_payment_frame.pack(fill='x', expand=True)
        ttk.Label(monthly_payment_frame, text="Monthly Payment (incl. fees):", anchor='w').pack(side='left')
        ttk.Label(monthly_payment_frame, textvariable=self.monthly_payment_var, anchor='e').pack(side='right')

        total_interest_frame = ttk.Frame(results_frame)
        total_interest_frame.pack(fill='x', expand=True)
        ttk.Label(total_interest_frame, text="Total Interest:", anchor='w').pack(side='left')
        ttk.Label(total_interest_frame, textvariable=self.total_interest_var, anchor='e').pack(side='right')

        # Step 5: Export Results
        export_frame = ttk.LabelFrame(parent, text="Step 5: Export Results", padding=10)
        export_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(export_frame, text="Export PDF", command=self.export_pdf).pack(side='right')

        # Monthly Payment Breakdown
        breakdown_frame = ttk.LabelFrame(parent, text="Monthly Payment Breakdown", padding=10)
        breakdown_frame.pack(fill='x', padx=5, pady=5)

        # Principal Payment
        principal_frame = ttk.Frame(breakdown_frame)
        principal_frame.pack(fill='x', expand=True)
        ttk.Label(principal_frame, text="Principal Payment:", anchor='w').pack(side='left')
        ttk.Label(principal_frame, textvariable=self.monthly_principal_var, anchor='e').pack(side="right")  

        # Extra Payment
        extra_frame = ttk.Frame(breakdown_frame)
        extra_frame.pack(fill='x', expand=True)
        ttk.Label(extra_frame, text="Extra Payment:", anchor='w').pack(side='left')
        ttk.Label(extra_frame, textvariable=self.monthly_extra_var, anchor='e').pack(side='right')

        # Total Principal
        total_principal_frame = ttk.Frame(breakdown_frame)
        total_principal_frame.pack(fill='x', expand=True)
        ttk.Label(total_principal_frame, text="Total Principal:", anchor='w').pack(side='left')
        ttk.Label(total_principal_frame, textvariable=self.monthly_total_principal_var, anchor='e').pack(side='right')

        # Interest Payment
        interest_frame = ttk.Frame(breakdown_frame)
        interest_frame.pack(fill='x', expand=True)
        ttk.Label(interest_frame, text="Interest Payment:", anchor='w').pack(side='left')
        ttk.Label(interest_frame, textvariable=self.monthly_interest_var, anchor='e').pack(side='right')

        # Monthly House Fee
        fee_frame = ttk.Frame(breakdown_frame)
        fee_frame.pack(fill='x', expand=True)
        ttk.Label(fee_frame, text="Monthly House Fee:", anchor='w').pack(side='left')
        ttk.Label(fee_frame, textvariable=self.monthly_fee_var, anchor='e').pack(side='right')

        # Total Monthly Payment
        total_frame = ttk.Frame(breakdown_frame)
        total_frame.pack(fill='x', expand=True)
        ttk.Label(total_frame, text="Total Monthly Payment:", anchor='w').pack(side='left')
        ttk.Label(total_frame, textvariable=self.monthly_total_var, anchor='e').pack(side='right')

        # With Extra Payments
        extra_impact_frame = ttk.LabelFrame(parent, text="With Extra Payments", padding=10)
        extra_impact_frame.pack(fill='x', padx=5, pady=5)

        # Time Saved
        time_saved_frame = ttk.Frame(extra_impact_frame)
        time_saved_frame.pack(fill='x', expand=True)
        ttk.Label(time_saved_frame, text="Time Saved:", anchor='w').pack(side='left')
        ttk.Label(time_saved_frame, textvariable=self.time_saved_var, anchor='e').pack(side='right')

        # Interest Saved
        interest_saved_frame = ttk.Frame(extra_impact_frame)
        interest_saved_frame.pack(fill='x', expand=True)
        ttk.Label(interest_saved_frame, text="Interest Saved:", anchor='w').pack(side='left')
        ttk.Label(interest_saved_frame, textvariable=self.interest_saved_var, anchor='e').pack(side='right')

        # Loan Payoff Time
        payoff_frame = ttk.Frame(extra_impact_frame)
        payoff_frame.pack(fill='x', expand=True)
        ttk.Label(payoff_frame, text="Loan Payoff Time:", anchor='w').pack(side='left')
        ttk.Label(payoff_frame, textvariable=self.loan_payoff_time_var, anchor='e').pack(side='right')

    # STEP 5: Input Validation
    def validate_inputs(self):
        """Validate all input fields"""
        try:
            # Validate loan seeking amount
            loan_seeking = self.get_float_value(self.loan_seeking_var.get())
            if loan_seeking <= 0:
                messagebox.showerror("Error", "Loan seeking amount must be greater than 0")
                return False

            # Validate down payment
            down_payment = self.get_float_value(self.down_payment_var.get())
            if down_payment < 0:
                messagebox.showerror("Error", "Down payment cannot be negative")
                return False
            if down_payment >= loan_seeking:
                messagebox.showerror("Error", "Down payment must be less than loan seeking amount")
                return False

            # Validate interest rate
            interest_rate = self.get_float_value(self.interest_rate_var.get())
            if interest_rate <= 0 or interest_rate >= 100:
                messagebox.showerror("Error", "Interest rate must be between 0 and 100")
                return False

            # Validate principal payment
            principal_payment = self.get_float_value(self.principal_payment_var.get())
            if principal_payment < 0:
                messagebox.showerror("Error", "Principal payment cannot be negative")
                return False

            # Validate extra payment
            extra_payment = self.get_float_value(self.extra_payment_var.get())
            if extra_payment < 0:
                messagebox.showerror("Error", "Extra payment cannot be negative")
                return False

            # Validate monthly fee
            monthly_fee = self.get_float_value(self.monthly_fee_var.get())
            if monthly_fee < 0:
                messagebox.showerror("Error", "Monthly house fee cannot be negative")
                return False

            return True

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False

    # STEP 6: Calculation Logic
    def calculate(self):
        """Calculate mortgage payments and update display"""
        if not self.validate_inputs():
            return

        try:
            # Get values from inputs
            loan_seeking = self.get_float_value(self.loan_seeking_var.get())
            down_payment = self.get_float_value(self.down_payment_var.get())
            loan_amount = loan_seeking - down_payment
            interest_rate = self.get_float_value(self.interest_rate_var.get())
            principal_payment = self.get_float_value(self.principal_payment_var.get())
            extra_payment = self.get_float_value(self.extra_payment_var.get() or "0")
            monthly_fee = self.get_float_value(self.monthly_fee_var.get())

            # Calculate monthly rate and base payment
            monthly_rate = interest_rate / 100 / 12
            base_monthly = (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -360)
            
            # Calculate monthly interest
            monthly_interest = loan_amount * monthly_rate
            
            # Calculate total monthly payment (including principal, interest, extra payment, and fees)
            total_monthly = principal_payment + extra_payment + monthly_interest + monthly_fee
            
            # Calculate total interest over loan term
            total_interest = (base_monthly * 360) - loan_amount

            # Calculate base payoff time (without extra payments)
            base_months_to_payoff = int(loan_amount / principal_payment)
            
            # Calculate time and interest saved with extra payments
            if extra_payment > 0:
                # Calculate months to payoff with the simplified formula
                total_monthly_payment = principal_payment + extra_payment
                months_with_extra = int(loan_amount / total_monthly_payment)
                
                # Calculate interest for the shorter period
                total_interest_with_extra = 0
                remaining_balance = loan_amount
                for _ in range(months_with_extra):
                    interest = remaining_balance * monthly_rate
                    total_interest_with_extra += interest
                    remaining_balance -= total_monthly_payment
                
                # Calculate time saved by comparing with base payoff time
                time_saved = base_months_to_payoff - months_with_extra
                years_saved = time_saved // 12
                months_saved = time_saved % 12
                
                # Calculate interest saved
                interest_saved = total_interest - total_interest_with_extra
                
                # Calculate payoff time
                years_to_payoff = months_with_extra // 12
                months_to_payoff = months_with_extra % 12
            else:
                # Use base payoff time when no extra payments
                months_with_extra = base_months_to_payoff
                years_to_payoff = months_with_extra // 12
                months_to_payoff = months_with_extra % 12
                years_saved = months_saved = 0
                interest_saved = 0

            # Format currency based on selection
            currency = self.currency_var.get()
            
            # Step 4: Update View Results
            self.monthly_payment_var.set(f"{currency}{total_monthly:,.0f}")
            self.total_interest_var.set(f"{currency}{total_interest:,.0f}")
            
            # Step 5: Update Monthly Payment Breakdown
            self.monthly_principal_var.set(f"{currency}{principal_payment:,.0f}")
            self.monthly_extra_var.set(f"{currency}{extra_payment:,.0f}")
            self.monthly_total_principal_var.set(f"{currency}{(principal_payment + extra_payment):,.0f}")
            self.monthly_interest_var.set(f"{currency}{monthly_interest:,.0f}")
            # Monthly House Fee without currency symbol
            self.monthly_fee_var.set(f"{monthly_fee:,.0f}")
            self.monthly_total_var.set(f"{currency}{total_monthly:,.0f}")
            
            # Update Extra Payments Impact
            self.time_saved_var.set(f"{years_saved} years, {months_saved} months")
            self.interest_saved_var.set(f"{currency}{interest_saved:,.0f}")
            self.loan_payoff_time_var.set(f"{years_to_payoff} years, {months_to_payoff} months")

            # Store current values for PDF export
            self.current_values = {
                'loan_amount': loan_amount,
                'currency_symbol': currency,
                'monthly_payment': total_monthly,
                'total_interest': total_interest,
                'principal_payment': principal_payment,
                'extra_payment': extra_payment,
                'monthly_fee': monthly_fee,
                'time_saved': f"{years_saved} years, {months_saved} months",
                'interest_saved': interest_saved,
                'loan_payoff': f"{years_to_payoff} years, {months_to_payoff} months"
            }

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during calculation: {str(e)}")
            return False
        return True

    def get_float_value(self, value_str):
        """Convert string to float, handling commas and invalid input"""
        try:
            # Remove any currency symbols and commas
            cleaned_str = value_str.replace('kr', '').replace('$', '').replace(',', '').strip()
            if not cleaned_str:
                return 0.0
            return float(cleaned_str)
        except ValueError:
            raise ValueError(f"Invalid number format: {value_str}")

    def update_on_loan_seeking_change(self, *args):
        """Update loan amount when loan seeking amount changes"""
        try:
            loan_seeking = self.get_float_value(self.loan_seeking_var.get())
            if loan_seeking > 0:
                if self.down_payment_mode.get() == "auto":
                    # Calculate 15% down payment for auto mode
                    down_payment = loan_seeking * 0.15
                    self.down_payment_var.set(f"{down_payment:,.0f}")
                    self.down_payment_entry.configure(state='disabled')
                else:
                    # In manual mode, enable entry but keep current value
                    self.down_payment_entry.configure(state='normal')
                    if not self.down_payment_var.get():
                        self.down_payment_var.set("0")
                
                # Calculate and update loan amount
                try:
                    down_payment = self.get_float_value(self.down_payment_var.get())
                    loan_amount = loan_seeking - down_payment if down_payment <= loan_seeking else 0
                    self.loan_amount_var.set(f"{loan_amount:,.0f}")
                except ValueError:
                    self.loan_amount_var.set(f"{loan_seeking:,.0f}")
            else:
                self.down_payment_entry.configure(state='disabled')
                self.down_payment_var.set("")
                self.loan_amount_var.set("")

        except ValueError:
            self.down_payment_entry.configure(state='disabled')
            self.down_payment_var.set("")
            self.loan_amount_var.set("")

    def update_loan_amount(self, *args):
        """Update loan amount when down payment changes"""
        try:
            loan_seeking = self.get_float_value(self.loan_seeking_var.get())
            down_payment = self.get_float_value(self.down_payment_var.get())
            if loan_seeking > 0 and down_payment > 0:
                loan_amount = loan_seeking - down_payment if down_payment <= loan_seeking else 0
                self.loan_amount_var.set(f"{loan_amount:,.0f}")
        except ValueError:
            pass

    def toggle_down_payment_mode(self):
        """Toggle down payment mode between auto and manual"""
        if self.down_payment_mode.get() == "auto":
            self.down_payment_entry.configure(state='disabled')
        else:
            self.down_payment_entry.configure(state='normal')

    def initialize_variables(self):
        """Initialize all variables"""
        # Currency
        self.currency_var = tk.StringVar(value="kr")
        self.currency_name_var = tk.StringVar(value="Swedish Krona (SEK)")
        
        # Input variables
        self.loan_seeking_var = tk.StringVar(value="")
        self.down_payment_var = tk.StringVar(value="")
        self.loan_amount_var = tk.StringVar(value="")
        self.interest_rate_var = tk.StringVar(value="4.5")  # Set default to 4.5
        self.principal_payment_var = tk.StringVar(value="")
        self.extra_payment_var = tk.StringVar(value="")
        self.monthly_fee_var = tk.StringVar(value="")
        
        # Result variables
        self.monthly_payment_var = tk.StringVar(value="kr0")
        self.total_interest_var = tk.StringVar(value="kr0")
        self.monthly_principal_var = tk.StringVar(value="kr0")
        self.monthly_extra_var = tk.StringVar(value="kr0")
        self.monthly_total_principal_var = tk.StringVar(value="kr0")
        self.monthly_interest_var = tk.StringVar(value="kr0")
        self.monthly_fee_var = tk.StringVar(value="")  # Keep Monthly House Fee blank
        self.monthly_total_var = tk.StringVar(value="kr0")
        self.time_saved_var = tk.StringVar(value="0 years, 0 months")
        self.interest_saved_var = tk.StringVar(value="kr0")
        self.loan_payoff_time_var = tk.StringVar(value="30 years, 0 months")

        # Store current values for PDF export
        self.current_values = {
            'loan_amount': 0,
            'currency_symbol': 'kr',
            'monthly_payment': 0,
            'total_interest': 0,
            'principal_payment': 0,
            'extra_payment': 0,
            'monthly_fee': 0,
            'time_saved': '0 years, 0 months',
            'interest_saved': 0,
            'loan_payoff': '30 years, 0 months'
        }

    def initialize_display_variables(self):
        """Initialize display variables for results"""
        self.monthly_payment_var = tk.StringVar(value="kr0")
        self.total_interest_var = tk.StringVar(value="kr0")
        self.monthly_principal_var = tk.StringVar(value="kr0")
        self.monthly_extra_var = tk.StringVar(value="kr0")
        self.monthly_total_principal_var = tk.StringVar(value="kr0")
        self.monthly_interest_var = tk.StringVar(value="kr0")
        self.monthly_fee_var = tk.StringVar(value="")  # Keep Monthly House Fee blank
        self.monthly_total_var = tk.StringVar(value="kr0")
        self.time_saved_var = tk.StringVar(value="0 years, 0 months")
        self.interest_saved_var = tk.StringVar(value="kr0")
        self.loan_payoff_time_var = tk.StringVar(value="30 years, 0 months")

    def export_pdf(self):
        """Export results to PDF"""
        try:
            # Create exports directory if it doesn't exist
            export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exports')
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate timestamp for unique filename
            current_date = datetime.now()
            base_filename = f'mortgage_calculation_{current_date.strftime("%d-%m-%Y")}'
            
            # Check if file exists and create unique name
            counter = 1
            filename = os.path.join(export_dir, f'{base_filename}.pdf')
            while os.path.exists(filename):
                filename = os.path.join(export_dir, f'{base_filename}_{counter}.pdf')
                counter += 1
            
            # Create PDF
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            
            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Mortgage Calculator Results")
            
            # Add line under title
            c.line(50, height - 60, width - 50, height - 60)
            
            # Add subtitle with timestamp
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 80, f"Generated on: {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Add loan details
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 100, "Loan Details")
            
            c.setFont("Helvetica", 10)
            y = height - 120
            
            # Get values and handle potential empty strings
            loan_seeking = self.get_float_value(self.loan_seeking_var.get() or "0")
            down_payment = self.get_float_value(self.down_payment_var.get() or "0")
            loan_amount = self.get_float_value(self.loan_amount_var.get() or "0")
            
            details = [
                f"Loan Seeking For: {self.currency_var.get()}{loan_seeking:,.0f}",
                f"Down Payment: {self.currency_var.get()}{down_payment:,.0f}",
                f"Loan Amount: {self.currency_var.get()}{loan_amount:,.0f}",
                f"Interest Rate: {self.interest_rate_var.get()}%"
            ]
            
            for detail in details:
                y -= 20
                c.drawString(70, y, detail)
            
            # Add Monthly Payment Breakdown
            y -= 40
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Monthly Payment Breakdown")
            
            c.setFont("Helvetica", 10)
            y -= 20
            breakdown = [
                f"Principal Payment: {self.monthly_principal_var.get()}",
                f"Extra Payment: {self.monthly_extra_var.get()}",
                f"Total Principal: {self.monthly_total_principal_var.get()}",
                f"Interest Payment: {self.monthly_interest_var.get()}",
                f"Monthly House Fee: {self.monthly_fee_var.get() or ''}",
                f"Total Monthly Payment: {self.monthly_total_var.get()}"
            ]
            
            for item in breakdown:
                y -= 20
                c.drawString(70, y, item)
            
            # Add Extra Payments Impact
            y -= 40
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "With Extra Payments")
            
            c.setFont("Helvetica", 10)
            y -= 20
            extra_payments = [
                f"Time Saved: {self.time_saved_var.get()}",
                f"Interest Saved: {self.interest_saved_var.get()}",
                f"Loan Payoff Time: {self.loan_payoff_time_var.get()}"
            ]
            
            for item in extra_payments:
                y -= 20
                c.drawString(70, y, item)
            
            c.save()
            messagebox.showinfo("Success", f"PDF exported successfully to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")

    def update_extra_payments_info(self, time_saved, interest_saved):
        """Update the extra payments information display"""
        self.time_saved_var.set(str(time_saved))
        self.interest_saved_var.set(str(interest_saved))

    def clear_displays(self):
        """Clear all display fields"""
        currency = self.currency_var.get()
        self.monthly_payment_var.set(f"{currency}0")
        self.total_interest_var.set(f"{currency}0")
        self.monthly_principal_var.set(f"{currency}0")
        self.monthly_extra_var.set(f"{currency}0")
        self.monthly_total_principal_var.set(f"{currency}0")
        self.monthly_interest_var.set(f"{currency}0")
        self.monthly_fee_var.set("")  # Keep Monthly House Fee blank
        self.monthly_total_var.set(f"{currency}0")
        self.time_saved_var.set("0 years, 0 months")
        self.interest_saved_var.set(f"{currency}0")
        self.loan_payoff_time_var.set("30 years, 0 months")
        
    def clear_fields(self):
        """Clear all input fields and reset displays"""
        # Clear input fields
        self.loan_seeking_var.set("")
        self.down_payment_var.set("")
        self.interest_rate_var.set("4.5")  # Reset interest rate to default
        self.principal_payment_var.set("")
        self.extra_payment_var.set("")
        self.monthly_fee_var.set("")
        
        # Reset currency to default
        self.currency_var.set('kr')
        self.currency_name_var.set("Swedish Krona (SEK)")
        
        # Reset loan amount
        self.loan_amount_var.set("0")
        
        # Clear displays
        self.clear_displays()

    # STEP 13: Main Function
def main():
    root = tk.Tk()
    app = MortgageCalculator(root)
    root.mainloop()

# STEP 14: Entry Point
if __name__ == "__main__":
    main()
