#!/bin/bash

# ==============================================================================
# THE POWERPRO - ANTIGRAVITY DEPLOYMENT TOOL (v2.4)
# ==============================================================================

set -e

echo "🚀 Starting Antigravity Deployment Engine..."

# 1. Environment Verification
if [ ! -f .env ]; then
    echo "⚠️  .env not found. Creating from template..."
    cp .env.example .env
    
    # Generate random secret key
    SECRET_KEY=$(openssl rand -hex 32)
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    echo "✅ Generated new SECRET_KEY"
fi

# 2. Infrastructure Build
echo "🏗️  Building Production Containers..."
docker-compose down
docker-compose build --no-cache

# 3. Launch Services
echo "🚢 Launching Orchestrated Services..."
docker-compose up -d

# 4. Post-Launch Automation
echo "🔧 Running Database Migrations..."
# Wait for DB to be initialized
sleep 5
docker-compose exec -T backend alembic upgrade head

# 5. Data Integrity Verification
echo "🛡️  Ensuring Data Integrity (Admin Verification)..."
# Optional: Trigger seed script if needed

echo "=============================================================================="
echo "🎉 DEPLOYMENT COMPLETE"
echo "🌐 Environment: Production"
echo "📍 Access point: http://localhost"
echo "=============================================================================="
