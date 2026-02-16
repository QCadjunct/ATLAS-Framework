#!/bin/bash

# ATLAS Framework Website - Quick Deployment Script
# This script helps you deploy the ATLAS Framework website to various platforms

set -e

echo "🚀 ATLAS Framework Website Deployment"
echo "======================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to deploy to GitHub Pages
deploy_github() {
    echo "📦 Deploying to GitHub Pages..."
    
    if [ ! -d ".git" ]; then
        echo "Initializing Git repository..."
        git init
        git add .
        git commit -m "Initial commit: ATLAS Framework documentation"
    fi
    
    echo ""
    echo "Please create a repository on GitHub and run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/atlas-framework-docs.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
    echo "Then enable GitHub Pages in repository settings."
}

# Function to deploy to Netlify
deploy_netlify() {
    echo "📦 Deploying to Netlify..."
    
    if ! command_exists netlify; then
        echo "Installing Netlify CLI..."
        npm install -g netlify-cli
    fi
    
    echo "Building site..."
    mkdocs build
    
    echo "Deploying to Netlify..."
    netlify deploy --prod --dir=site
}

# Function to deploy to Vercel
deploy_vercel() {
    echo "📦 Deploying to Vercel..."
    
    if ! command_exists vercel; then
        echo "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    echo "Building site..."
    mkdocs build
    
    echo "Deploying to Vercel..."
    vercel --prod
}

# Function to build Docker image
deploy_docker() {
    echo "🐳 Building Docker image..."
    
    if ! command_exists docker; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    echo "Building image..."
    docker build -t atlas-framework-docs .
    
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the container:"
    echo "  docker run -d -p 8000:8000 --name atlas-docs atlas-framework-docs"
    echo ""
    echo "Access at: http://localhost:8000"
}

# Function to test locally
test_local() {
    echo "🧪 Testing locally..."
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo "Building site..."
    mkdocs build
    
    echo "Starting local server..."
    mkdocs serve
}

# Main menu
echo "Select deployment option:"
echo "1) GitHub Pages"
echo "2) Netlify"
echo "3) Vercel"
echo "4) Docker"
echo "5) Test locally"
echo "6) Exit"
echo ""
read -p "Enter option (1-6): " option

case $option in
    1)
        deploy_github
        ;;
    2)
        deploy_netlify
        ;;
    3)
        deploy_vercel
        ;;
    4)
        deploy_docker
        ;;
    5)
        test_local
        ;;
    6)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment process completed!"
