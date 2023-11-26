#! python3
import json

# Service type options
service_types = ['hotel', 'spa', 'restaurant']

# Define the functions to create business and package data
def create_business():
    business_data = {
        'id': '',  # No longer asking for business ID
        'introduction': tr(
            input('Enter business introduction (Spanish): '),
            'serverData:vendor.marquis.introduction',
        ),
        'whyWeLoveIt': tr(
            input('Enter why we love this business (Spanish): '),
            'serverData:vendor.marquis.whyWeLoveIt',
        ),
        'isDemo': 'false',  # Always return 'false'
        'location': {
            'townOrCity': input('Enter town or city: '),
            'state': input('Enter state: '),
            'googlePlaceId': input('Enter Google Place ID: '),
        },
        'type': select_service_type(),
        'name': input('Enter business name: '),
        'packages': [],  # Packages will be added later
        'images': [],  # No longer asking for image URLs
        'categories': {},  # Always return 'categories': {}
        'amenities': {
            'included': [],
            'notIncluded': [],
            'allowed': [],
            'notAllowed': [],
            'available': [],
            ' notAvailable': [],
        },
    }
    return business_data

def select_service_type():
    print("\nSelect Service Type:")
    for i, service_type in enumerate(service_types):
        print(f"{i}. {service_type}")

    while True:
        try:
            index = int(input("Enter the index of the desired service type: "))
            selected_type = map_index_to_service_type(index)
            return selected_type
        except ValueError:
            print("Invalid input. Please enter a valid index.")

def map_index_to_service_type(index):
    return {
        0: SERVICE_TYPE_HOTEL,
        1: SERVICE_TYPE_SPA,
        2: SERVICE_TYPE_RESTAURANT
    }.get(index, SERVICE_TYPE_HOTEL)  # Default to hotel if index is invalid

def create_package():
    short_description = tr(
        input('Enter package short description (Spanish): '),
        'serverData:vendor.marquis.packages.masaje.shortDescription',
    )

    package_data = {
        'id': '',  # No longer asking for package ID
        'name': tr(
            input('Enter package name (Spanish): '),
            'serverData:vendor.marquis.packages.masaje.name',
        ),
        'type': select_service_type(),  # Using select_service_type for package type
        'shortDescription': short_description,
        'longDescription': short_description,  # Reusing short description for long description
        'images': [],  # No longer asking for image URLs
        'price': float(input('Enter package price: ')),
        'priceType': input('Enter price type (e.g., perPerson): '),
        'currency': 'MXN',  # Always set to MXN
        'categories': {},  # Always return 'categories': {}
        'amenities': {
            'included': [],
            'notIncluded': [],
            'allowed': [],
            'notAllowed': [],
            'available': [],
            'notAvailable': [],
        },
    }
    return package_data

def print_as_js_docstring(data, indent=2):
    print("\n```javascript")
    print(json.dumps(data, indent=indent))
    print("```")

# Function to generate the data structure
def generate_data():
    business = create_business()

    num_packages = int(input('How many packages do you want to add? '))
    packages = [create_package() for _ in range(num_packages)]

    # Print business data
    print("\nBusiness Data:")
    print_as_js_docstring(business)

    # Print package data
    print("\nPackage Data:")
    for package in packages:
        print_as_js_docstring(package)

# Dummy function for give_id
def give_id(value):
    return value

# Placeholder for tr function
def tr(text, server_key):
    return text

# Constants for service types
SERVICE_TYPE_HOTEL = 'hotel'
SERVICE_TYPE_SPA = 'spa'
SERVICE_TYPE_RESTAURANT = 'restaurant'

# Execute the script
if __name__ == "__main__":
    generate_data()
