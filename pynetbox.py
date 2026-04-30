import pynetbox

# Create API connection (Api class)
nb = pynetbox.api('http://netbox.example.com', token='your-token')

# Access an app (App class)
nb.dcim  # Returns an App instance

# Access an endpoint (Endpoint class)
nb.dcim.devices  # Returns an Endpoint instance

# Use endpoint methods
devices = nb.dcim.devices.all()
