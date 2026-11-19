import random

# --- Econophysics: Probabilistic State Modeling ---
# Define market states and their characteristics (mean daily return, volatility multiplier).
# These parameters influence the simulated asset price movements, reflecting different market regimes.
MARKET_STATES = {
    "Bullish": {"mean_return": 0.0015, "volatility_mult": 1.0},  # Positive drift, normal volatility
    "Bearish": {"mean_return": -0.001, "volatility_mult": 1.5}, # Negative drift, higher volatility
    "Sideways": {"mean_return": 0.0001, "volatility_mult": 0.7} # Small drift, lower volatility
}

# Define transition probabilities between states (a simple Markov Chain).
# The sum of probabilities for each current state should be 1.0.
TRANSITION_MATRIX = {
    "Bullish": {"Bullish": 0.7, "Bearish": 0.1, "Sideways": 0.2},
    "Bearish": {"Bullish": 0.15, "Bearish": 0.6, "Sideways": 0.25},
    "Sideways": {"Bullish": 0.3, "Bearish": 0.2, "Sideways": 0.5}
}

# Initial market state for the simulation
current_market_state = "Sideways"

def get_next_state(current_state):
    """Probabilistically transitions to the next market state based on the transition matrix."""
    global current_market_state
    probabilities = TRANSITION_MATRIX[current_state]
    states = list(probabilities.keys())
    weights = list(probabilities.values())
    current_market_state = random.choices(states, weights, k=1)[0]
    return current_market_state

def generate_asset_return(state_params, base_volatility=0.01):
    """Generates a daily return for an asset using a Gaussian distribution,
    influenced by the current market state's mean return and volatility."""
    mean = state_params["mean_return"]
    std_dev = base_volatility * state_params["volatility_mult"]
    return random.gauss(mean, std_dev)

# --- Portfolio Level Control ---
# Initial portfolio setup for multiple assets
NUM_ASSETS = 3
INITIAL_ASSET_PRICE = 100.0
INITIAL_ASSET_UNITS = 10
portfolio_assets = [{"price": INITIAL_ASSET_PRICE, "units": INITIAL_ASSET_UNITS} for _ in range(NUM_ASSETS)]
initial_portfolio_value = sum(asset["price"] * asset["units"] for asset in portfolio_assets)

print(f"Initial Portfolio Value: ${initial_portfolio_value:.2f}\n")

# Simulation parameters
NUM_DAYS = 100

for day in range(1, NUM_DAYS + 1):
    print(f"--- Day {day} ---")
    prev_state = current_market_state
    current_market_state = get_next_state(prev_state) # Update market state probabilistically
    state_params = MARKET_STATES[current_market_state]

    print(f"Market State: {current_market_state}")

    # Apply portfolio control based on the current market state.
    # This demonstrates making portfolio-level decisions influenced by the probabilistic state model.
    if current_market_state == "Bearish":
        # In a bearish state, reduce exposure to mitigate risk across all assets.
        for asset in portfolio_assets:
            sell_units = asset["units"] * 0.1 # Sell 10% of units
            asset["units"] -= sell_units
            print(f"  Action: Sold {sell_units:.2f} units from an asset due to Bearish state.")
    elif current_market_state == "Bullish":
        # In a bullish state, increase exposure to capture potential upside across all assets.
        for asset in portfolio_assets:
            buy_units = asset["units"] * 0.05 # Buy 5% more units
            asset["units"] += buy_units
            print(f"  Action: Bought {buy_units:.2f} units for an asset due to Bullish state.")
    # If Sideways, no specific portfolio action is taken for simplicity.

    # Simulate asset price movements for all assets based on the current market state
    current_portfolio_value = 0
    for i, asset in enumerate(portfolio_assets):
        daily_return = generate_asset_return(state_params)
        asset["price"] *= (1 + daily_return)
        current_portfolio_value += asset["price"] * asset["units"]

    print(f"  End of Day Portfolio Value: ${current_portfolio_value:.2f}")
    print("-" * 20)

print(f"\nSimulation finished after {NUM_DAYS} days.")
final_portfolio_value = sum(asset["price"] * asset["units"] for asset in portfolio_assets)
print(f"Final Portfolio Value: ${final_portfolio_value:.2f}")
print(f"Initial Portfolio Value: ${initial_portfolio_value:.2f}")
print(f"Total Return: {((final_portfolio_value - initial_portfolio_value) / initial_portfolio_value * 100):.2f}%")
