"""A beginner-friendly example of interpolation and root finding.

The numbers below are made up for a class project. This program finds when
the modeled plane crosses a chosen altitude; it does not predict collisions.
"""

# Example flight measurements: time in minutes and altitude in meters.
times = [10, 20, 30, 40]
altitudes = [1500, 3500, 2800, 4000]
target_height = 3000


def interpolate(time, heights):
    """Estimate the altitude at a time using Lagrange interpolation."""
    answer = 0

    for i in range(len(times)):
        term = heights[i]

        for j in range(len(times)):
            if i != j:
                term = term * (time - times[j]) / (times[i] - times[j])

        answer = answer + term

    return answer


def find_crossing(start, end, heights):
    """Use bisection to find when altitude reaches the target height."""
    for step in range(40):
        middle = (start + end) / 2

        # Is the altitude above or below the target at each time?
        start_difference = interpolate(start, heights) - target_height
        middle_difference = interpolate(middle, heights) - target_height

        # Keep the half of the time range that contains the crossing.
        if start_difference * middle_difference > 0:
            start = middle
        else:
            end = middle

    return (start + end) / 2


# Find the crossing between minutes 20 and 30.
crossing_time = find_crossing(20, 30, altitudes)
print("Estimated target-height crossing:", round(crossing_time, 4), "minutes")


# Change each measurement by a small amount to show measurement error.
# These fixed changes make the example repeatable every time it runs.
small_changes = [2, -3, 1, -2]
changed_altitudes = []
for i in range(len(altitudes)):
    changed_altitudes.append(altitudes[i] + small_changes[i])

changed_crossing_time = find_crossing(20, 30, changed_altitudes)
time_shift_seconds = abs(changed_crossing_time - crossing_time) * 60

print("Crossing with slightly changed measurements:",
      round(changed_crossing_time, 4), "minutes")
print("Difference between crossing times:",
      round(time_shift_seconds, 4), "seconds")


# Print a small error table at a few times.
print("\nTime | Original altitude | Changed altitude | Difference")
for time in [20, crossing_time, 25, 30]:
    original = interpolate(time, altitudes)
    changed = interpolate(time, changed_altitudes)
    difference = abs(changed - original)
    print(round(time, 2), "|", round(original, 2), "|",
          round(changed, 2), "|", round(difference, 2))


# Show a simple text graph, so no extra plotting package is needed.
print("\nAltitude graph (each * is about 200 meters)")
for time in range(10, 41, 2):
    height = interpolate(time, altitudes)
    number_of_stars = int(height / 200)
    marker = "  <-- target crossing" if abs(time - crossing_time) < 1 else ""
    print(str(time).rjust(2), "|", "*" * number_of_stars, marker)
