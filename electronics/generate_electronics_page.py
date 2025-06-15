# python_electronics_html_generator.py
import http.server
import socketserver
import os

def generate_electronics_html():
    """
    Generates a string containing an HTML page for a sample electronics store,
    styled with Tailwind CSS for responsiveness and modern aesthetics.
    """
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ElectroShop - Your Tech Destination</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif; /* Using Inter font */
            background-color: #f8f8f8; /* Light grey background */
        }
        /* Custom styles for hover effects and shadows */
        .card-hover-effect:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header Section -->
    <header class="bg-gray-800 text-white p-4 shadow-lg">
        <div class="container mx-auto flex flex-col md:flex-row justify-between items-center">
            <a href="#" class="text-3xl font-extrabold text-indigo-400 rounded-lg p-2 hover:text-indigo-300 transition-colors duration-300">
                ElectroShop
            </a>
            <nav class="mt-4 md:mt-0">
                <ul class="flex space-x-6 text-lg">
                    <li><a href="#" class="hover:text-indigo-400 transition-colors duration-300 rounded-md p-2">Home</a></li>
                    <li><a href="#" class="hover:text-indigo-400 transition-colors duration-300 rounded-md p-2">Products</a></li>
                    <li><a href="#" class="hover:text-indigo-400 transition-colors duration-300 rounded-md p-2">About Us</a></li>
                    <li><a href="#" class="hover:text-indigo-400 transition-colors duration-300 rounded-md p-2">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Main Content Section -->
    <main class="flex-grow container mx-auto p-4 py-8">
        <h2 class="text-4xl font-bold text-gray-800 mb-8 text-center">Featured Products</h2>

        <!-- Product Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">

            <!-- Product Card 1 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover-effect transition-all duration-300 p-6 flex flex-col items-center text-center">
                <img src="https://placehold.co/300x200/4F46E5/FFFFFF?text=Laptop" alt="Laptop" class="w-full h-48 object-cover rounded-md mb-4">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">Powerful Laptop</h3>
                <p class="text-gray-600 mb-4 flex-grow">High-performance laptop for all your computing needs.</p>
                <div class="text-3xl font-bold text-indigo-600 mb-4">$1200.00</div>
                <button class="bg-indigo-600 text-white px-6 py-3 rounded-full text-lg font-medium hover:bg-indigo-700 transition-colors duration-300 shadow-md">
                    Add to Cart
                </button>
            </div>

            <!-- Product Card 2 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover-effect transition-all duration-300 p-6 flex flex-col items-center text-center">
                <img src="https://placehold.co/300x200/4F46E5/FFFFFF?text=Smartphone" alt="Smartphone" class="w-full h-48 object-cover rounded-md mb-4">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">Latest Smartphone</h3>
                <p class="text-gray-600 mb-4 flex-grow">Stay connected with the newest smartphone technology.</p>
                <div class="text-3xl font-bold text-indigo-600 mb-4">$800.00</div>
                <button class="bg-indigo-600 text-white px-6 py-3 rounded-full text-lg font-medium hover:bg-indigo-700 transition-colors duration-300 shadow-md">
                    Add to Cart
                </button>
            </div>

            <!-- Product Card 3 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover-effect transition-all duration-300 p-6 flex flex-col items-center text-center">
                <img src="https://placehold.co/300x200/4F46E5/FFFFFF?text=Headphones" alt="Headphones" class="w-full h-48 object-cover rounded-md mb-4">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">Wireless Headphones</h3>
                <p class="text-gray-600 mb-4 flex-grow">Immersive audio experience with noise cancellation.</p>
                <div class="text-3xl font-bold text-indigo-600 mb-4">$250.00</div>
                <button class="bg-indigo-600 text-white px-6 py-3 rounded-full text-lg font-medium hover:bg-indigo-700 transition-colors duration-300 shadow-md">
                    Add to Cart
                </button>
            </div>

            <!-- Product Card 4 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover-effect transition-all duration-300 p-6 flex flex-col items-center text-center">
                <img src="https://placehold.co/300x200/4F46E5/FFFFFF?text=Smartwatch" alt="Smartwatch" class="w-full h-48 object-cover rounded-md mb-4">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">Advanced Smartwatch</h3>
                <p class="text-gray-600 mb-4 flex-grow">Track your fitness and receive notifications on the go.</p>
                <div class="text-3xl font-bold text-indigo-600 mb-4">$350.00</div>
                <button class="bg-indigo-600 text-white px-6 py-3 rounded-full text-lg font-medium hover:bg-indigo-700 transition-colors duration-300 shadow-md">
                    Add to Cart
                </button>
            </div>

            <!-- Product Card 5 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover-effect transition-all duration-300 p-6 flex flex-col items-center text-center">
                <img src="https://placehold.co/300x200/4F46E5/FFFFFF?text=Tablet" alt="Tablet" class="w-full h-48 object-cover rounded-md mb-4">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">Portable Tablet</h3>
                <p class="text-gray-600 mb-4 flex-grow">Perfect for entertainment and productivity on the move.</p>
                <div class="text-3xl font-bold text-indigo-600 mb-4">$500.00</div>
                <button class="bg-indigo-600 text-white px-6 py-3 rounded-full text-lg font-medium hover:bg-indigo-700 transition-colors duration-300 shadow-md">
                    Add to Cart
                </button>
            </div>

            <!-- Product Card 6 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover-effect transition-all duration-300 p-6 flex flex-col items-center text-center">
                <img src="https://placehold.co/300x200/4F46E5/FFFFFF?text=Camera" alt="Camera" class="w-full h-48 object-cover rounded-md mb-4">
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">Digital Camera</h3>
                <p class="text-gray-600 mb-4 flex-grow">Capture stunning photos and videos with ease.</p>
                <div class="text-3xl font-bold text-indigo-600 mb-4">$700.00</div>
                <button class="bg-indigo-600 text-white px-6 py-3 rounded-full text-lg font-medium hover:bg-indigo-700 transition-colors duration-300 shadow-md">
                    Add to Cart
                </button>
            </div>

        </div>
    </main>

    <!-- Footer Section -->
    <footer class="bg-gray-800 text-white p-6 mt-8 shadow-inner">
        <div class="container mx-auto text-center text-sm md:text-base">
            <p>&copy; 2025 ElectroShop. All rights reserved.</p>
            <p class="mt-2">Designed with passion for technology lovers.</p>
        </div>
    </footer>

</body>
</html>
    """
    return html_content

if __name__ == "__main__":
    html_output = generate_electronics_html()

    # Create a directory for web content if it doesn't exist
    web_dir = "web"
    os.makedirs(web_dir, exist_ok=True)

    # Define the HTML file path within the web directory
    html_file_path = os.path.join(web_dir, "index.html")

    # Write the HTML content to the file
    try:
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"HTML content successfully written to '{html_file_path}'")
    except IOError as e:
        print(f"Error writing HTML file {html_file_path}: {e}")
        exit(1) # Exit if we can't even write the HTML file

    # Change current directory to the web_dir to serve files from there
    os.chdir(web_dir)

    PORT = 8000 # Standard HTTP port for development servers
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT} from directory '{os.getcwd()}'")
        print(f"Access the page at http://localhost:{PORT}")
        httpd.serve_forever()
