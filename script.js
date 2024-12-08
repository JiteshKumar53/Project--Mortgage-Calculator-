// Currency exchange rates (example rates - should be updated with real-time data)
const exchangeRates = {
    USD: 1,
    SEK: 10.42,
    INR: 83.37,
    EUR: 0.93
};

// Currency symbols
const currencySymbols = {
    USD: '$',
    SEK: 'kr',
    INR: '₹',
    EUR: '€'
};

let loanCounter = 1;
let loans = [];

class Loan {
    constructor(id, principal, interestRate, term, extraPayment, monthlyPrincipal, currency) {
        this.id = id;
        this.principal = principal;
        this.interestRate = interestRate;
        this.term = term;
        this.extraPayment = extraPayment;
        this.monthlyPrincipal = monthlyPrincipal;
        this.currency = currency;
    }

    calculateMonthlyPayment() {
        // If monthly principal is set, return the total monthly payment
        if (this.monthlyPrincipal > 0) {
            const monthlyRate = this.interestRate / 100 / 12;
            const interestPayment = this.principal * monthlyRate;
            return this.monthlyPrincipal + interestPayment;
        }
        
        // Traditional amortization calculation
        const monthlyRate = this.interestRate / 100 / 12;
        const numberOfPayments = this.term * 12;
        if (monthlyRate === 0) {
            return this.principal / numberOfPayments;
        }
        const monthlyPayment = (this.principal * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) /
            (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
        return monthlyPayment;
    }

    calculateAmortizationSchedule() {
        const schedule = [];
        let balance = this.principal;
        const monthlyRate = this.interestRate / 100 / 12;

        while (balance > 0) {
            const interestPayment = balance * monthlyRate;
            let principalPayment;
            let monthlyPayment;

            if (this.monthlyPrincipal > 0) {
                // Fixed monthly principal payment
                principalPayment = Math.min(this.monthlyPrincipal, balance);
                monthlyPayment = principalPayment + interestPayment;
            } else {
                // Traditional amortization
                monthlyPayment = this.calculateMonthlyPayment();
                principalPayment = monthlyPayment - interestPayment;
            }

            let extraPayment = this.extraPayment;
            if (principalPayment + extraPayment > balance) {
                extraPayment = balance - principalPayment;
            }

            balance = Math.max(0, balance - principalPayment - extraPayment);

            schedule.push({
                month: schedule.length + 1,
                payment: monthlyPayment,
                principalPayment,
                interestPayment,
                extraPayment,
                remainingBalance: balance
            });

            if (balance === 0 || schedule.length > 360) { // Maximum 30 years
                break;
            }
        }

        return schedule;
    }
}

function initializeEventListeners() {
    // Add event listener for global currency selector
    document.getElementById('global-currency').addEventListener('change', (e) => {
        const newCurrency = e.target.value;
        // Update all loan forms with the new currency
        for (let i = 1; i <= loanCounter; i++) {
            const form = document.getElementById(`loan-form-${i}`);
            if (form) {
                updateLoanCurrency(i, newCurrency);
            }
        }
        updateCalculations();
    });

    // Add event listeners for the first loan form
    addLoanFormListeners(1);

    // Add loan button
    document.getElementById('add-loan').addEventListener('click', addNewLoan);

    // Clear button
    document.getElementById('clear').addEventListener('click', clearAllForms);

    // Calculate button
    document.getElementById('calculate').addEventListener('click', updateCalculations);

    // Initialize the first loan
    updateCalculations();
}

function updateLoanCurrency(id, currency) {
    const loan = loans.find(l => l.id === id);
    if (loan) {
        loan.currency = currency;
    }
}

function addLoanFormListeners(id) {
    const form = document.getElementById(`loan-form-${id}`);
    if (!form) return;

    // Add listeners for interest rate inputs
    const interestSlider = form.querySelector(`#interest-${id}`);
    const interestManual = form.querySelector(`#interest-manual-${id}`);
    const interestValue = document.getElementById(`interest-value-${id}`);

    if (interestSlider && interestManual && interestValue) {
        // Update manual input when slider changes
        interestSlider.addEventListener('input', () => {
            const value = parseFloat(interestSlider.value);
            interestManual.value = value;
            interestValue.textContent = `${value}%`;
            updateCalculations();
        });

        // Update slider when manual input changes
        interestManual.addEventListener('input', () => {
            let value = parseFloat(interestManual.value);
            
            // Clamp value between 0 and 100
            value = Math.max(0, Math.min(100, value));
            
            // Update manual input with clamped value
            interestManual.value = value;
            
            // Update slider if value is within its range
            if (value <= 20) {
                interestSlider.value = value;
            } else {
                interestSlider.value = 20; // Max slider value
            }
            
            interestValue.textContent = `${value}%`;
            updateCalculations();
        });
    }

    // Add listeners for other inputs
    ['principal', 'term', 'extra-payment', 'monthly-principal'].forEach(field => {
        const element = form.querySelector(`#${field}-${id}`);
        if (element) {
            element.addEventListener('input', () => {
                if (field === 'term') {
                    updateSliderValue(id, field);
                }
                
                // Only handle interest rate clearing for monthly principal
                if (field === 'monthly-principal' && parseFloat(element.value) > 0) {
                    const interestSlider = form.querySelector(`#interest-${id}`);
                    const interestManual = form.querySelector(`#interest-manual-${id}`);
                    const termInput = form.querySelector(`#term-${id}`);
                    if (interestSlider) interestSlider.value = '0';
                    if (interestManual) interestManual.value = '0';
                    if (termInput) termInput.value = '30';
                    updateSliderValue(id, 'term');
                }
                
                updateCalculations();
            });
        }
    });
}

function updateSliderValue(id, field) {
    const slider = document.getElementById(`${field}-${id}`);
    const valueSpan = document.getElementById(`${field}-value-${id}`);
    if (slider && valueSpan) {
        if (field === 'interest') {
            valueSpan.textContent = `${slider.value}%`;
        } else if (field === 'term') {
            valueSpan.textContent = `${slider.value} years`;
        }
    }
}

function addNewLoan() {
    loanCounter++;
    
    const loanForm = document.createElement('div');
    loanForm.className = 'loan-form';
    loanForm.id = `loan-form-${loanCounter}`;
    
    loanForm.innerHTML = `
        <h3>Loan ${loanCounter}</h3>
        <div class="form-group">
            <label for="principal-${loanCounter}">Loan Amount:</label>
            <input type="number" id="principal-${loanCounter}" class="principal" min="0" step="1000">
        </div>
        <div class="form-group">
            <label for="interest-${loanCounter}">Interest Rate (%):</label>
            <div class="interest-input-group">
                <input type="range" id="interest-${loanCounter}" class="interest-slider" min="0" max="20" step="0.1" value="5">
                <input type="number" id="interest-manual-${loanCounter}" class="interest-manual" min="0" max="100" step="0.1" value="5">
                <span id="interest-value-${loanCounter}">5%</span>
            </div>
        </div>
        <div class="form-group">
            <label for="term-${loanCounter}">Loan Term (years):</label>
            <input type="range" id="term-${loanCounter}" class="term" min="1" max="30" step="1" value="15">
            <span id="term-value-${loanCounter}">15 years</span>
        </div>
        <div class="form-group">
            <label for="monthly-principal-${loanCounter}">Monthly Principal Payment:</label>
            <input type="number" id="monthly-principal-${loanCounter}" class="monthly-principal" min="0" step="100">
        </div>
        <div class="form-group">
            <label for="extra-payment-${loanCounter}">Extra Monthly Payment:</label>
            <input type="number" id="extra-payment-${loanCounter}" class="extra-payment" min="0" step="100" value="0">
        </div>
    `;

    document.querySelector('.loan-inputs').insertBefore(loanForm, document.getElementById('add-loan'));
    addLoanFormListeners(loanCounter);
    updateCalculations();
}

function updateCalculations() {
    loans = [];
    const globalCurrency = document.getElementById('global-currency').value;
    
    // Collect all loan data
    for (let i = 1; i <= loanCounter; i++) {
        const form = document.getElementById(`loan-form-${i}`);
        if (!form) continue;

        const principal = parseFloat(form.querySelector(`#principal-${i}`).value) || 0;
        const interestManual = form.querySelector(`#interest-manual-${i}`);
        const interestRate = parseFloat(interestManual.value);  
        const term = parseInt(form.querySelector(`#term-${i}`).value) || 30;
        const extraPayment = parseFloat(form.querySelector(`#extra-payment-${i}`).value) || 0;
        const monthlyPrincipal = parseFloat(form.querySelector(`#monthly-principal-${i}`).value) || 0;

        if (principal > 0) {
            loans.push(new Loan(i, principal, interestRate, term, extraPayment, monthlyPrincipal, globalCurrency));
        }
    }

    updateSummary();
    updateCharts();
    updateAmortizationTable();
}

function clearAllForms() {
    // Reset all input fields
    document.querySelectorAll('input[type="number"], input[type="range"]').forEach(input => {
        if (input.classList.contains('interest') || input.classList.contains('interest-manual')) {
            input.value = '3.5';
        } else if (input.classList.contains('term')) {
            input.value = '30';
        } else {
            input.value = '';
        }
    });

    // Reset currency selectors
    document.querySelectorAll('select.currency').forEach(select => {
        select.value = 'USD';
    });

    // Update all displays
    document.querySelectorAll('[id^="interest-value-"]').forEach(span => {
        span.textContent = '3.5%';
    });
    document.querySelectorAll('[id^="term-value-"]').forEach(span => {
        span.textContent = '30 years';
    });

    // Clear results
    document.querySelector('.results-container').innerHTML = '';

    // Remove additional loan forms
    const forms = document.querySelectorAll('.loan-form');
    for (let i = 1; i < forms.length; i++) {
        forms[i].remove();
    }
    loanCounter = 1;
    loans = [];
}

function updateSummary() {
    const summarySection = document.querySelector('.summary-section');
    let totalMonthlyPayment = 0;
    let totalInterest = 0;
    let maxMonths = 0;

    loans.forEach(loan => {
        const schedule = loan.calculateAmortizationSchedule();
        const monthlyPayment = loan.calculateMonthlyPayment();
        
        totalMonthlyPayment += convertCurrency(monthlyPayment + loan.extraPayment, loan.currency, 'USD');
        
        const totalPaid = schedule.reduce((sum, month) => 
            sum + convertCurrency(month.payment + month.extraPayment, loan.currency, 'USD'), 0);
        totalInterest += totalPaid - convertCurrency(loan.principal, loan.currency, 'USD');
        
        maxMonths = Math.max(maxMonths, schedule.length);
    });

    const payoffDate = new Date();
    payoffDate.setMonth(payoffDate.getMonth() + maxMonths);

    summarySection.innerHTML = `
        <h2>Summary</h2>
        <div class="total-amount">Total Monthly Payment: ${formatCurrency(totalMonthlyPayment, 'USD')}</div>
        <div class="total-amount">Total Interest: ${formatCurrency(totalInterest, 'USD')}</div>
        <div>Final Payoff Date: ${payoffDate.toLocaleDateString()}</div>
    `;
}

function updateCharts() {
    updateAmortizationChart();
    updateInterestChart();
}

function updateAmortizationChart() {
    const ctx = document.getElementById('amortization-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.amortizationChart) {
        window.amortizationChart.destroy();
    }
    
    const datasets = [];
    
    loans.forEach((loan, index) => {
        const schedule = loan.calculateAmortizationSchedule();
        datasets.push({
            label: `Loan ${index + 1} Balance`,
            data: schedule.map(month => convertCurrency(month.remainingBalance, loan.currency, 'USD')),
            borderColor: `hsl(${index * 137.5}, 70%, 50%)`,
            fill: false
        });
    });

    window.amortizationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: Math.max(...datasets.map(d => d.data.length)) }, (_, i) => i + 1),
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Loan Balance Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => formatCurrency(value, 'USD', false)
                    }
                }
            }
        }
    });
}

function updateInterestChart() {
    const ctx = document.getElementById('interest-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.interestChart) {
        window.interestChart.destroy();
    }
    
    const datasets = [];
    
    loans.forEach((loan, index) => {
        const schedule = loan.calculateAmortizationSchedule();
        let cumulativeInterest = 0;
        datasets.push({
            label: `Loan ${index + 1} Cumulative Interest`,
            data: schedule.map(month => {
                cumulativeInterest += convertCurrency(month.interestPayment, loan.currency, 'USD');
                return cumulativeInterest;
            }),
            borderColor: `hsl(${index * 137.5}, 70%, 50%)`,
            fill: false
        });
    });

    window.interestChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: Math.max(...datasets.map(d => d.data.length)) }, (_, i) => i + 1),
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Cumulative Interest Paid Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => formatCurrency(value, 'USD', false)
                    }
                }
            }
        }
    });
}

function updateAmortizationTable() {
    const tableBody = document.querySelector('#amortization-table tbody');
    tableBody.innerHTML = '';

    loans.forEach((loan, loanIndex) => {
        const schedule = loan.calculateAmortizationSchedule();
        
        schedule.forEach((month, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>Loan ${loanIndex + 1} - Month ${month.month}</td>
                <td>${formatCurrency(month.payment, loan.currency)}</td>
                <td>${formatCurrency(month.principalPayment, loan.currency)}</td>
                <td>${formatCurrency(month.interestPayment, loan.currency)}</td>
                <td>${formatCurrency(month.extraPayment, loan.currency)}</td>
                <td>${formatCurrency(month.remainingBalance, loan.currency)}</td>
            `;
            tableBody.appendChild(row);
        });
    });
}

function convertCurrency(amount, fromCurrency, toCurrency) {
    return amount * exchangeRates[toCurrency] / exchangeRates[fromCurrency];
}

function formatCurrency(amount, currency, includeSymbol = true) {
    const formatter = new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    
    const formattedAmount = formatter.format(amount);
    return includeSymbol ? `${currencySymbols[currency]}${formattedAmount}` : formattedAmount;
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', initializeEventListeners);
