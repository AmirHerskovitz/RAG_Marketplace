import requests
import concurrent.futures

# Your API key
api_key = 'bcf8703e3056ad91937caa8968d9919822265e79f75076ca401c455a2223daee'

# Headers dictionary
headers = {
	'x-api-key': api_key
}

# Function to fetch product details
def fetch_product_details(product_id):
	product_url = f"https://catalogapi.azure.com/products/{product_id}?api-version=2023-05-01-preview&market=US&language=en"
	product_response = requests.get(product_url, headers=headers)
	if product_response.status_code == 200:
		product_data = product_response.json()
		return product_id, product_data.get('links', {})
	else:
		print(f"Failed to fetch product data for {product_id}, status code: {product_response.status_code}")
		return product_id, None

def fetch_and_dump_data(base_url, file_path, headers):
	# Initialize the URL for the first request
	url = base_url
	# Open the file in append mode
	with open(file_path, 'a', encoding='utf-8') as file:
		while url:
			# Send the GET request for the initial API
			response = requests.get(url, headers=headers)
			# Check if the request was successful
			if response.status_code == 200:
				data = response.json()
				items = data.get('items', [])
				product_ids = [item.get('productId') for item in items]

				# Use ThreadPoolExecutor to fetch product details in parallel
				with concurrent.futures.ThreadPoolExecutor() as executor:
					future_to_product_id = {executor.submit(fetch_product_details, pid): pid for pid in product_ids}
					for future in concurrent.futures.as_completed(future_to_product_id):
						product_id = future_to_product_id[future]
						try:
							product_id, links = future.result()
							if links is not None:
								# Find the corresponding item and add the links object
								for item in items:
									if item.get('productId') == product_id:
										item['links'] = links
										# Write the modified item to the file
										file.write(str(item) + '\n')
						except Exception as exc:
							print(f"Product {product_id} generated an exception: {exc}")

				# Check for nextPageLink and update the URL, or set it to None to end the loop
				url = data.get('nextPageLink', None)
				print(f"Processed {len(data.get('items', []))} items")
			else:
				print(f"Failed to fetch data, status code: {response.status_code}")
				break

# Define the initial API URL
base_url = "https://catalogapi.azure.com/products/?api-version=2023-05-01-preview&market=US&language=en&$select=productId,displayName,productType,description,publisherDisplayName"

# Specify the path to the output file
file_path = "Catalog.txt"

# Call the function to start the process
fetch_and_dump_data(base_url, file_path, headers)
