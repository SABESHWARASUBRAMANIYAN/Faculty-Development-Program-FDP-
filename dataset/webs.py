import requests
from bs4 import BeautifulSoup

# Function to scrape university details
def scrape_university_details(uni):
    # You can add the URL of the website you want to scrape here
    url = 'https://example.com/university/' + uni

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant information from the page
        university_name = soup.find('h1', class_='university-name').text.strip()
        location = soup.find('span', class_='location').text.strip()
        description = soup.find('div', class_='description').text.strip()

        # Create a dictionary with the scraped information
        university_details = {
            'university_name': university_name,
            'location': location,
            'description': description
        }

        return university_details

    else:
        return None  # Return None if the request was not successful

# Function to handle the "Scrape University Details" button click
def scrape_university():
    # Retrieve the entered university from the text field
    university = text_university.get()

    # Scrape additional details about the university
    university_details = scrape_university_details(university)

    if university_details:
        tk.messagebox.showinfo("University Details",
                               f"University Name: {university_details['university_name']}\n"
                               f"Location: {university_details['location']}\n"
                               f"Description: {university_details['description']}")
    else:
        tk.messagebox.showinfo("University Details", "No details found.")
