import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def train_model(story_points, costs):
	"""Train a linear regression model and return the fitted model and score."""
	x = story_points.reshape(-1, 1)
	model = LinearRegression()
	model.fit(x, costs)
	score = model.score(x, costs)
	return model, score


def print_predictions(model, points):
	"""Print predicted costs for a list of story-point values."""
	for point in points:
		predicted_cost = model.predict(np.array([[point]]))[0]
		print(f"Predicted cost for {point} story points: ${predicted_cost:.2f}k")


def plot_regression(story_points, costs, model, title, output_file):
	"""Plot scatter data and regression line, then save the figure."""
	x_plot = np.linspace(story_points.min(), story_points.max(), 100).reshape(-1, 1)
	y_plot = model.predict(x_plot)

	plt.figure(figsize=(8, 5))
	plt.scatter(story_points, costs, color="steelblue", label="Historical Projects")
	plt.plot(x_plot, y_plot, color="crimson", linewidth=2, label="Regression Line")
	plt.title(title)
	plt.xlabel("Story Points")
	plt.ylabel("Cost ($1000s)")
	plt.grid(alpha=0.3)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_file, dpi=150)


def main():
	# Baseline mock data from the activity prompt.
	story_points = np.array([20, 35, 50, 65], dtype=float)
	costs = np.array([50, 75, 100, 130], dtype=float)

	print("=== Software Cost Prediction (Linear Regression) ===")
	print("Baseline data:")
	for sp, cost in zip(story_points, costs):
		print(f"Story points: {int(sp):>3} -> Cost: ${cost:.0f}k")

	baseline_model, baseline_r2 = train_model(story_points, costs)
	baseline_slope = baseline_model.coef_[0]
	baseline_intercept = baseline_model.intercept_

	print("\nBaseline model details:")
	print(f"Equation: cost = {baseline_slope:.3f} * story_points + {baseline_intercept:.3f}")
	print(f"R^2 score: {baseline_r2:.4f}")

	print("\nRequired predictions:")
	print_predictions(baseline_model, [40, 25])

	base_dir = os.path.dirname(os.path.abspath(__file__))
	baseline_plot_path = os.path.join(base_dir, "cost_regression_baseline.png")
	plot_regression(
		story_points,
		costs,
		baseline_model,
		"Software Cost vs Story Points (Baseline)",
		baseline_plot_path,
	)
	print(f"\nBaseline plot saved to: {baseline_plot_path}")

	# Extended scenario: add one project with 100 story points.
	extended_story_points = np.append(story_points, 100.0)
	extended_costs = np.append(costs, 190.0)
	extended_model, extended_r2 = train_model(extended_story_points, extended_costs)
	extended_slope = extended_model.coef_[0]
	extended_intercept = extended_model.intercept_

	print("\n=== Extended Dataset Scenario ===")
	print("Added project: 100 story points -> $190k")
	print(f"New equation: cost = {extended_slope:.3f} * story_points + {extended_intercept:.3f}")
	print(f"New R^2 score: {extended_r2:.4f}")

	print("\nPredictions after extending dataset:")
	print_predictions(extended_model, [40, 25, 100])

	extended_plot_path = os.path.join(base_dir, "cost_regression_extended.png")
	plot_regression(
		extended_story_points,
		extended_costs,
		extended_model,
		"Software Cost vs Story Points (Extended with 100 SP)",
		extended_plot_path,
	)
	print(f"Extended plot saved to: {extended_plot_path}")

	linear_note = "Yes" if baseline_r2 >= 0.95 else "Not strongly"
	print("\n=== Discussion Prompts ===")
	print(f"1. Does cost increase appear linear? {linear_note}, based on baseline R^2 = {baseline_r2:.4f}.")
	print("2. How did adding 100 story points change the slope and predictions?")
	print("3. Real-world use: supports budgeting, early effort estimates, and planning discussions.")
	print("4. Limitations: ignores team experience, complexity, requirement volatility, and non-linear effort.")

	# Show plots only when using an interactive backend.
	backend = plt.get_backend().lower()
	if "agg" not in backend:
		plt.show()


if __name__ == "__main__":
	main()
