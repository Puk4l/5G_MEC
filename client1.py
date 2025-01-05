import requests
import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.offsetbox as offsetbox

# Load your dataset
df = pd.read_csv('user_input.csv')

if 'User_Id' not in df.columns:
    df['User_Id'] = df.index  

# Define the latitude and longitude ranges for each container
container_ranges = {
    5001: {'lat_min': -90, 'lat_max': -60, 'lon_min': -180, 'lon_max': 180},
    5002: {'lat_min': -60, 'lat_max': -30, 'lon_min': -180, 'lon_max': 180},
    5003: {'lat_min': -30, 'lat_max': 0, 'lon_min': -180, 'lon_max': 180},
    5004: {'lat_min': 0, 'lat_max': 30, 'lon_min': -180, 'lon_max': 180},
    5005: {'lat_min': 30, 'lat_max': 60, 'lon_min': -180, 'lon_max': 180}
}


# Extract Latitude and Longitude for clustering
coordinates = df[['Latitude', 'Longitude']].values

# Apply DBSCAN clustering
db = DBSCAN(eps=0.5, min_samples=5)  # Adjust eps and min_samples based on your data
df['Cluster'] = db.fit_predict(coordinates)

# Function to check which container the user belongs to based on latitude and longitude
def find_nearest_container(lat, lon):
    for port, bounds in container_ranges.items():
        if bounds['lat_min'] <= lat <= bounds['lat_max'] and bounds['lon_min'] <= lon <= bounds['lon_max']:
            return port
    return None  # In case no container range matches, though this should not happen

# Function to send data to the appropriate container
def send_data_to_container(user_data, container_port):
    url = f'http://localhost:{container_port}/predict'  # Assuming containers have a /predict endpoint
    try:
        response = requests.post(url, json=user_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the container returns JSON
    except requests.exceptions.RequestException as e:
        print(f"Error while sending data to container {container_port}: {e}")
        return None

# Define the input columns to send to the container
input_columns = ['Application_Type', 'Signal_Strength', 'Latency', 'Required_Bandwidth', 'Allocated_Bandwidth']

# Setup for visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
ax.set_title("Real-time User and Container Visualization")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Load images for visualization
container_img = mpimg.imread('edge.png')  # Placeholder image for containers
user_img = mpimg.imread('user.png')      # Placeholder image for users

# Resize images to a smaller size
container_img = offsetbox.OffsetImage(container_img, zoom=0.05)  # Reduced zoom for container
user_img = offsetbox.OffsetImage(user_img, zoom=0.05)            # Reduced zoom for user

# Initialize CSV storage for each container
for port in container_ranges.keys():
    csv_file = f'container_{port}_data.csv'
    # Create or clear the file with headers
    pd.DataFrame(columns=input_columns + ['Prediction']).to_csv(csv_file, index=False)

# Track which user ids have already been added to the legend
added_labels = set()

# Function to place an image at a specific coordinate
def place_image(ax, image, x, y, image_size=(1, 1)):
    imagebox = offsetbox.AnnotationBbox(image, (x, y), frameon=False)
    ax.add_artist(imagebox)

# Plot initial positions of containers based on their bounds
for port, bounds in container_ranges.items():
    lat = (bounds['lat_min'] + bounds['lat_max']) / 2
    lon = (bounds['lon_min'] + bounds['lon_max']) / 2
    place_image(ax, container_img, lon, lat)
    ax.text(lon, lat, f"Edge {port - 5000}", color="black", fontsize=10, ha='center', va='center')

def update(frame):
    user = df.iloc[frame]
    lat, lon = user['Latitude'], user['Longitude']
    user_id = user['User_Id']
    
    # Find the nearest container
    container_port = find_nearest_container(lat, lon)
    
    if container_port:
        # Send the user data to the appropriate container
        user_data = user[input_columns].to_dict()
        prediction = send_data_to_container(user_data, container_port)
        
        # Plot the user position using image
        place_image(ax, user_img, lon, lat)
        if f"User {user_id}" not in added_labels:
            ax.scatter(lon, lat, c='blue', label=f'User {user_id}')
            added_labels.add(f"User {user_id}")
        
        # Draw a line connecting the user to the container
        container_bounds = container_ranges[container_port]
        container_lat = (container_bounds['lat_min'] + container_bounds['lat_max']) / 2
        container_lon = (container_bounds['lon_min'] + container_bounds['lon_max']) / 2
        ax.plot([lon, container_lon], [lat, container_lat], 'g-')
        
        # Store input and prediction in the container's CSV file
        result_data = user_data.copy()
        if prediction:
            result_data['Prediction'] = prediction.get('prediction', 'No Prediction')
        else:
            result_data['Prediction'] = 'Error'
        
        csv_file = f'container_{container_port}_data.csv'
        pd.DataFrame([result_data]).to_csv(csv_file, mode='a', header=False, index=False)

# Add zoom functionality
def zoom(event):
    if event.key == "up":
        # Zoom in
        ax.set_xlim(ax.get_xlim()[0] * 0.9, ax.get_xlim()[1] * 0.9)
        ax.set_ylim(ax.get_ylim()[0] * 0.9, ax.get_ylim()[1] * 0.9)
    elif event.key == "down":
        # Zoom out
        ax.set_xlim(ax.get_xlim()[0] * 1.1, ax.get_xlim()[1] * 1.1)
        ax.set_ylim(ax.get_ylim()[0] * 1.1, ax.get_ylim()[1] * 1.1)
    fig.canvas.draw_idle()  # Redraw the plot with updated limits

# Connect the zoom function to key press events
fig.canvas.mpl_connect('key_press_event', zoom)

ani = animation.FuncAnimation(fig, update, frames=len(df), repeat=False)
plt.legend(loc="best")
plt.show()
