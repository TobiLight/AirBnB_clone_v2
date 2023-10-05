#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Check if Nginx is installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        This is a test page for web_static deployment.
    </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
link="/data/web_static/current"
if [ -L "$link" ]; then
    sudo rm "$link"
fi
sudo ln -s "/data/web_static/releases/test/" "$link"

# Give ownership of the /data/ directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content
nginx_config="/etc/nginx/sites-available/default"
if [ -f "$nginx_config" ]; then
    # Configure Nginx to serve the content using an alias
    echo "
server {
    listen 80;
    listen [::]:80 default_server;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    index index.html;
}
" | sudo tee "$nginx_config" > /dev/null

    # Restart Nginx to apply the configuration changes
    sudo service nginx restart
fi
