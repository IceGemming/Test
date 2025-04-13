import http.server
import socketserver
import json
import time
import threading
import random
import os
import socket
import hashlib
from urllib.parse import urlparse, parse_qs

# Configuration
PORT = 8080
HOST = "localhost"

# In-memory database to store data
database = {
    "users": [],
    "posts": []
}

# CPU intensive operations
def cpu_intensive_task():
    """Performs CPU intensive calculations to simulate heavy workload"""
    result = 0
    for _ in range(10000000):  # Adjust this number to control CPU usage
        result += random.random() ** 2 * random.random()
    return result

def generate_large_prime():
    """Generate large numbers and test primality - CPU intensive"""
    num = random.randint(10000000, 100000000)
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Create a large memory footprint
memory_hog = []

class HeavyRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
    
    def parse_body(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
    def do_GET(self):
        # Start a CPU intensive task in the background
        threading.Thread(target=cpu_intensive_task).start()
        
        # Create memory pressure
        global memory_hog
        memory_hog.extend([os.urandom(1024) for _ in range(1000)])
        
        # Parse URL and query parameters
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Route handling
        if path == '/api/users':
            # Get all users
            response = {'users': database['users'], 'status': 'success'}
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        
        elif path.startswith('/api/users/'):
            # Get specific user
            user_id = path.split('/')[-1]
            
            # Inefficiently search for user - O(n) lookup
            found_user = None
            for user in database['users']:
                if str(user.get('id')) == user_id:
                    # Perform unnecessary computation
                    for _ in range(1000000):
                        hash_value = hashlib.sha256(str(random.random()).encode()).hexdigest()
                    
                    found_user = user
                    break
            
            if found_user:
                self._set_headers()
                self.wfile.write(json.dumps(found_user).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'User not found'}).encode())
        
        elif path == '/api/posts':
            # Get all posts
            response = {'posts': database['posts'], 'status': 'success'}
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        
        elif path == '/api/status':
            # CPU intensive operation for status
            start_time = time.time()
            for _ in range(5):
                generate_large_prime()
            
            # Create additional memory pressure
            temp_memory = [os.urandom(1024) for _ in range(5000)]
            
            uptime = time.time() - start_time
            response = {
                'status': 'running',
                'uptime': uptime,
                'memory_usage': len(memory_hog),
                'cpu_load': 'high',
                'server_time': time.ctime()
            }
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        
        else:
            # Default route - still do heavy computation
            cpu_intensive_task()
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        # Start CPU intensive tasks in background
        threading.Thread(target=cpu_intensive_task).start()
        threading.Thread(target=generate_large_prime).start()
        
        # Create memory pressure
        global memory_hog
        memory_hog.extend([os.urandom(1024) for _ in range(2000)])

        try:
            if self.path == '/api/users':
                # Create new user
                body = self.parse_body()
                
                # Validate all fields with inefficient validation
                required_fields = ['name', 'email']
                for field in required_fields:
                    if field not in body:
                        self._set_headers(400)
                        self.wfile.write(json.dumps({'error': f'Missing field: {field}'}).encode())
                        return
                
                # Generate ID inefficiently
                user_id = len(database['users']) + 1
                for _ in range(500000):
                    user_id = (user_id * random.randint(1, 100)) % 10000000
                
                new_user = {
                    'id': user_id,
                    'name': body['name'],
                    'email': body['email'],
                    'created_at': time.ctime()
                }
                
                database['users'].append(new_user)
                
                self._set_headers(201)
                self.wfile.write(json.dumps(new_user).encode())
            
            elif self.path == '/api/posts':
                # Create new post
                body = self.parse_body()
                
                required_fields = ['title', 'content', 'user_id']
                for field in required_fields:
                    if field not in body:
                        self._set_headers(400)
                        self.wfile.write(json.dumps({'error': f'Missing field: {field}'}).encode())
                        return
                
                # Check if user exists (inefficiently)
                user_exists = False
                for user in database['users']:
                    if user['id'] == body['user_id']:
                        user_exists = True
                        # Do more unnecessary work
                        for _ in range(100000):
                            _ = hashlib.sha256(str(random.random()).encode()).hexdigest()
                        break
                
                if not user_exists:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': 'User does not exist'}).encode())
                    return
                
                # Generate post ID inefficiently
                post_id = len(database['posts']) + 1
                for _ in range(300000):
                    post_id = (post_id * random.randint(1, 100)) % 10000000
                
                new_post = {
                    'id': post_id,
                    'title': body['title'],
                    'content': body['content'],
                    'user_id': body['user_id'],
                    'created_at': time.ctime()
                }
                
                database['posts'].append(new_post)
                
                self._set_headers(201)
                self.wfile.write(json.dumps(new_post).encode())
            
            elif self.path == '/api/compute':
                # Pure computation endpoint
                body = self.parse_body()
                iterations = body.get('iterations', 1)
                
                result = 0
                for _ in range(min(iterations, 10)):  # Limit to 10 max for safety
                    result += cpu_intensive_task()
                    generate_large_prime()
                
                self._set_headers()
                self.wfile.write(json.dumps({'result': str(result)}).encode())
            
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        
        except Exception as e:
            # Even in error handling, do heavy computation
            cpu_intensive_task()
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_PUT(self):
        # Similar inefficient approach as POST
        threading.Thread(target=cpu_intensive_task).start()
        global memory_hog
        memory_hog.extend([os.urandom(1024) for _ in range(1500)])

        try:
            if self.path.startswith('/api/users/'):
                user_id = self.path.split('/')[-1]
                body = self.parse_body()
                
                # Find user inefficiently
                found_index = -1
                for i, user in enumerate(database['users']):
                    if str(user.get('id')) == user_id:
                        found_index = i
                        # Do extra work
                        for _ in range(200000):
                            _ = hashlib.sha256(str(random.random()).encode()).hexdigest()
                        break
                
                if found_index >= 0:
                    # Update user inefficiently
                    updated_user = database['users'][found_index].copy()
                    for key, value in body.items():
                        if key != 'id':  # Don't allow changing ID
                            updated_user[key] = value
                    
                    # Add updated timestamp with heavy computation
                    updated_user['updated_at'] = time.ctime()
                    database['users'][found_index] = updated_user
                    
                    self._set_headers()
                    self.wfile.write(json.dumps(updated_user).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'User not found'}).encode())
            
            elif self.path.startswith('/api/posts/'):
                post_id = self.path.split('/')[-1]
                body = self.parse_body()
                
                # Find post inefficiently
                found_index = -1
                for i, post in enumerate(database['posts']):
                    if str(post.get('id')) == post_id:
                        found_index = i
                        # Do extra work
                        for _ in range(250000):
                            _ = hashlib.sha256(str(random.random()).encode()).hexdigest()
                        break
                
                if found_index >= 0:
                    # Update post inefficiently
                    updated_post = database['posts'][found_index].copy()
                    for key, value in body.items():
                        if key not in ['id', 'user_id']:  # Don't allow changing ID or user_id
                            updated_post[key] = value
                    
                    updated_post['updated_at'] = time.ctime()
                    database['posts'][found_index] = updated_post
                    
                    self._set_headers()
                    self.wfile.write(json.dumps(updated_post).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Post not found'}).encode())
            
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        
        except Exception as e:
            cpu_intensive_task()
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_DELETE(self):
        # Resource-intensive delete operations
        threading.Thread(target=cpu_intensive_task).start()
        global memory_hog
        memory_hog.extend([os.urandom(1024) for _ in range(1000)])
        
        try:
            if self.path.startswith('/api/users/'):
                user_id = self.path.split('/')[-1]
                
                # Find and delete user inefficiently
                found_index = -1
                for i, user in enumerate(database['users']):
                    if str(user.get('id')) == user_id:
                        found_index = i
                        break
                
                if found_index >= 0:
                    # Instead of efficient O(1) deletion, rebuild the entire array O(n)
                    deleted_user = database['users'][found_index]
                    new_users = []
                    for i, user in enumerate(database['users']):
                        if i != found_index:
                            # Do unnecessary work for each item
                            for _ in range(10000):
                                _ = random.random() ** 2
                            new_users.append(user)
                    
                    database['users'] = new_users
                    
                    # Delete related posts inefficiently
                    new_posts = []
                    for post in database['posts']:
                        if post.get('user_id') != deleted_user['id']:
                            # More unnecessary work
                            for _ in range(5000):
                                _ = random.random() ** 2
                            new_posts.append(post)
                    
                    database['posts'] = new_posts
                    
                    self._set_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'deleted': deleted_user}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'User not found'}).encode())
            
            elif self.path.startswith('/api/posts/'):
                post_id = self.path.split('/')[-1]
                
                # Find and delete post inefficiently
                found_index = -1
                for i, post in enumerate(database['posts']):
                    if str(post.get('id')) == post_id:
                        found_index = i
                        break
                
                if found_index >= 0:
                    deleted_post = database['posts'][found_index]
                    # Rebuild the entire array inefficiently
                    new_posts = []
                    for i, post in enumerate(database['posts']):
                        if i != found_index:
                            # Do unnecessary work for each item
                            for _ in range(10000):
                                _ = random.random() ** 2
                            new_posts.append(post)
                    
                    database['posts'] = new_posts
                    
                    self._set_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'deleted': deleted_post}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Post not found'}).encode())
            
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        
        except Exception as e:
            cpu_intensive_task()
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def start_background_tasks():
    """Start background tasks that consume CPU and memory"""
    def memory_consumer():
        global memory_hog
        while True:
            # Add random data to memory_hog list
            memory_hog.extend([os.urandom(2048) for _ in range(500)])
            # Keep the list from growing infinitely
            if len(memory_hog) > 100000:
                memory_hog = memory_hog[-100000:]
            time.sleep(5)
    
    def cpu_consumer():
        while True:
            # Perform CPU intensive operations periodically
            cpu_intensive_task()
            generate_large_prime()
            time.sleep(3)
    
    threading.Thread(target=memory_consumer, daemon=True).start()
    threading.Thread(target=cpu_consumer, daemon=True).start()

def run_server():
    print(f"Starting server on {HOST}:{PORT}")
    
    # Start background resource-consuming tasks
    start_background_tasks()
    
    # Create and configure the server
    server = socketserver.ThreadingTCPServer((HOST, PORT), HeavyRequestHandler)
    
    # Run the server indefinitely
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopping...")
    finally:
        server.server_close()

if __name__ == "__main__":
    print("Heavy Python Backend Server")
    print("WARNING: This server is designed to use significant CPU and memory resources.")
    print("Use only for testing purposes.")
    print("-" * 50)
    run_server()