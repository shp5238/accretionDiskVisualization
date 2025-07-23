import matplotlib.pyplot as plt

# Example 1: Simple 1D Line Plot
data = [10, 20, 15, 30, 25]
plt.plot(data)               # Plot y-values (x is inferred as 0, 1, 2...)
plt.title("Sample Line Plot")
plt.xlabel("Index")
plt.ylabel("Value")
plt.grid(True)
plt.show()                   # Display the plot window

