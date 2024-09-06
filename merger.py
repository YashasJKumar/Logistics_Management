import csv

# Helper function to read CSV file
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Helper function to write CSV file
def write_csv_file(file_path, data):
    fieldnames = data[0].keys()
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Helper function to normalize city names
def normalize_city_name(city_name):
    return city_name.lower().replace(' ', '')


def parser(customer_data):
    # Read the distance CSV file
    distance_data = read_csv_file('distances_data.csv')

    # Read the customer delivery CSV file
    customer_data = read_csv_file(customer_data)
    distance_dict = {}
    for row in distance_data:
        source = normalize_city_name(row['source_city'])
        destination = normalize_city_name(row['destination_city'])
        distance = row['distance']
        distance_dict[(source, destination)] = distance

    # Merge distance information into customer data
    merged_data = []
    for customer in customer_data:
        source = normalize_city_name(customer['Source'].capitalize())
        destination = normalize_city_name(customer['Destination'].capitalize())
        distance = distance_dict.get((source, destination), '-1')
        customer['Distance'] = distance + " km."
        merged_data.append(customer)

# Write the merged data to a new CSV file
    write_csv_file('../merged_data.csv', merged_data)
