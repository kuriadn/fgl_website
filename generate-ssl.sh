#!/bin/bash

# Generate localhost SSL certificate for testing

echo "🔐 Generating localhost SSL certificate..."

# Create ssl directory if it doesn't exist
mkdir -p ssl

# Generate private key
openssl genrsa -out ssl/localhost.key 2048

# Generate certificate signing request
openssl req -new -key ssl/localhost.key -out ssl/localhost.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -in ssl/localhost.csr -signkey ssl/localhost.key -out ssl/localhost.crt -days 365

# Clean up CSR file
rm ssl/localhost.csr

echo "✅ SSL certificate generated!"
echo "📁 Files created:"
echo "   - ssl/localhost.key"
echo "   - ssl/localhost.crt"