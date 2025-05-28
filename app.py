from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define car types and their daily rates
CAR_RATES = {
    "economy": {"name": "Economy", "rate": 30},
    "suv": {"name": "SUV", "rate": 75},
    "luxury": {"name": "Luxury", "rate": 100},
    "sport": {"name": "Sport", "rate": 150}
}

# Define a tax rate (e.g., 8.25%)
TAX_RATE = 0.0825 # 8.25% tax
app.config['TAX_RATE'] = TAX_RATE # Make TAX_RATE available globally to templates via config

@app.route('/', methods=['GET', 'POST'])
def rent_car():
    name_val = ""
    age_val = ""
    license_val = ""
    days_val = ""
    car_val = ""

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age_str = request.form.get('age', '').strip()
        license_valid = request.form.get('license', '').strip()
        days_str = request.form.get('days', '').strip()
        car_type_key = request.form.get('car', '').strip()

        errors = []

        name_val = name
        age_val = age_str
        license_val = license_valid
        days_val = days_str
        car_val = car_type_key

        # --- Input Validation ---
        if not name:
            errors.append("Please provide your full name.")
        elif len(name) < 2:
            errors.append("Name is too short. Please enter your full name.")

        age = None
        if not age_str:
            errors.append("Please provide your age.")
        else:
            try:
                age = int(age_str)
                if not (21 <= age <= 120):
                    errors.append("Renters must be at least 21 years old and a realistic age.")
            except ValueError:
                errors.append("Invalid age. Please enter a valid number.")

        if not license_valid:
            errors.append("Please confirm if you have a valid driver's license.")
        elif license_valid.lower() != "yes":
            errors.append("A valid driver's license is required to rent a car.")

        rental_days = None
        if not days_str:
            errors.append("Please provide the number of rental days.")
        else:
            try:
                rental_days = int(days_str)
                if not (1 <= rental_days <= 365):
                    errors.append("Rental days must be between 1 and 365.")
            except ValueError:
                errors.append("Invalid rental days. Please enter a valid number.")

        daily_rate = 0
        car_type_display = ""
        if not car_type_key or car_type_key not in CAR_RATES:
            errors.append("Please select a valid car type.")
        else:
            selected_car = CAR_RATES[car_type_key]
            car_type_display = selected_car["name"]
            daily_rate = selected_car["rate"]

        if errors:
            return render_template('error.html', errors=errors)

        total_cost = daily_rate * rental_days
        discount = 0

        if rental_days > 7:
            discount_amount_long_rental = total_cost * 0.10
            discount += discount_amount_long_rental

        current_cost_before_tax = total_cost - discount
        if current_cost_before_tax > 500:
            additional_discount_amount = current_cost_before_tax * 0.05
            discount += additional_discount_amount
            current_cost_before_tax = total_cost - discount # Recalculate after applying additional discount

        # Calculate tax
        tax_amount = current_cost_before_tax * TAX_RATE
        
        # Calculate final cost including tax
        final_cost_with_tax = current_cost_before_tax + tax_amount

        # Format costs
        total_cost_formatted = f"{total_cost:.2f}"
        discount_formatted = f"{discount:.2f}"
        # tax_formatted = f"{tax_amount:.2f}" # No longer need to pass separately
        final_cost_formatted = f"{final_cost_with_tax:.2f}"

        result = {
            "name": name,
            "car_type": car_type_display,
            "rental_days": rental_days,
            "base_cost": total_cost_formatted,
            "discount": discount_formatted,
            # "tax": tax_formatted, # Removed this line
            "final_cost": final_cost_formatted # This now includes tax
        }

        return render_template('summary.html', result=result)

    return render_template('index.html',
                           name_val=name_val,
                           age_val=age_val,
                           license_val=license_val,
                           days_val=days_val,
                           car_val=car_val)

if __name__ == "__main__":
    app.run(debug=True)