import matplotlib.pyplot as plt

# Example dataset of containers and users (latitude, longitude)
containers = {
    5001: {'lat': -37.29899224, 'lon': -13.08440157, 'color': 'r', 'label': 'Container 5001'},
    5002: {'lat': 71.71320308, 'lon': 172.8804655, 'color': 'b', 'label': 'Container 5002'},
    5003: {'lat': -76.53377713, 'lon': 39.55222037, 'color': 'g', 'label': 'Container 5003'},
    5004: {'lat': 55.7472584, 'lon': -175.754866, 'color': 'y', 'label': 'Container 5004'},
    5005: {'lat': 34.0852801, 'lon': 4.700085756, 'color': 'c', 'label': 'Container 5005'}
}

# Example dataset of users (User_ID, Latitude, Longitude, Assigned Container)
users = [
    {'User_ID': 1, 'lat': -37.29899224, 'lon': -13.08440157, 'container': 5001},
    {'User_ID': 2, 'lat': 71.71320308, 'lon': 172.8804655, 'container': 5002},
    {'User_ID': 3, 'lat': -76.53377713, 'lon': 39.55222037, 'container': 5003},
    {'User_ID': 4, 'lat': 55.7472584, 'lon': -175.754866, 'container': 5004},
    {'User_ID': 5, 'lat': 34.0852801, 'lon': 4.700085756, 'container': 5005},
]

# Plot containers on the map
for container_id, container_info in containers.items():
    plt.scatter(container_info['lon'], container_info['lat'], color=container_info['color'], label=container_info['label'], s=100, edgecolors='black')

# Plot users on the map with container-specific colors
for user in users:
    container_color = containers[user['container']]['color']
    plt.scatter(user['lon'], user['lat'], color=container_color, label=f"User {user['User_ID']}", marker='x', s=80)

# Customize the plot
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Container and User Visualization')
plt.legend(loc='upper left')
plt.grid(True)

# Show the plot
plt.show()
