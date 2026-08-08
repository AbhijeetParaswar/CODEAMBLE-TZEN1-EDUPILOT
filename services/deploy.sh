#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# EduPilot — EC2 Deployment Script (Ubuntu 22.04/24.04, no Docker)
#
# Usage:
#   1. SSH into your EC2:  ssh -i edupilot-prod-key.pem ubuntu@13.212.58.39
#   2. Upload your code:
#        scp -i edupilot-prod-key.pem -r ./services ubuntu@13.212.58.39:/home/ubuntu/edupilot/
#        scp -i edupilot-prod-key.pem .env.production ubuntu@13.212.58.39:/home/ubuntu/edupilot/services/.env
#        scp -i edupilot-prod-key.pem deploy.sh ubuntu@13.212.58.39:~
#   3. Run:  chmod +x deploy.sh && ./deploy.sh
# ═══════════════════════════════════════════════════════════════════════════════

set -e
set -o pipefail

echo "════════════════════════════════════════════"
echo " EduPilot EC2 Deploy — $(date)"
echo "════════════════════════════════════════════"

# ── 1. System packages ────────────────────────────────────────────────────────
echo ""
echo "→ Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    postgresql \
    postgresql-contrib \
    redis-server \
    nginx \
    tesseract-ocr \
    tesseract-ocr-eng \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    git \
    curl \
    unzip
echo "✓ System packages installed"

# ── 2. PostgreSQL setup ───────────────────────────────────────────────────────
echo ""
echo "→ Setting up PostgreSQL..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

if [ -f "/home/ubuntu/edupilot/services/.env" ]; then
    POSTGRES_PASSWORD=$(grep "^POSTGRES_PASSWORD=" /home/ubuntu/edupilot/services/.env | cut -d'=' -f2 | tr -d ' ')
fi

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "  Enter a PostgreSQL password for edupilot_user:"
    read -s POSTGRES_PASSWORD
    echo ""
fi

sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='edupilot_user'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER edupilot_user WITH PASSWORD '$POSTGRES_PASSWORD';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='edupilot'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE edupilot OWNER edupilot_user;"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE edupilot TO edupilot_user;"
echo "✓ PostgreSQL ready (user: edupilot_user, db: edupilot)"

# ── 3. Redis setup ────────────────────────────────────────────────────────────
echo ""
echo "→ Setting up Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server
echo "✓ Redis running"

# ── 4. Code check ────────────────────────────────────────────────────────────
echo ""
echo "→ Checking project directory..."
if [ ! -d "/home/ubuntu/edupilot/services" ]; then
    echo "  ✗ No services/ directory found at /home/ubuntu/edupilot/services"
    echo "  Upload your code first, then re-run:"
    echo "    scp -i edupilot-prod-key.pem -r ./services ubuntu@13.212.58.39:/home/ubuntu/edupilot/"
    exit 1
fi
echo "✓ Code directory found"

# ── 5. Python venv + pip dependencies ────────────────────────────────────────
echo ""
echo "→ Creating Python virtual environment..."
cd /home/ubuntu/edupilot/services
python3.12 -m venv venv
source venv/bin/activate

echo "→ Installing Python dependencies (3-6 minutes)..."
pip install --upgrade pip -q
pip install -r requirements-prod.txt -q
echo "✓ Python dependencies installed"

# ── 6. Playwright Chromium install ───────────────────────────────────────────
echo ""
echo "→ Installing Playwright Chromium (for scrapers)..."
# --with-deps installs the OS-level libs Chromium needs on Ubuntu
playwright install chromium --with-deps
echo "✓ Playwright Chromium installed"

# ── 7. Environment file check ─────────────────────────────────────────────────
echo ""
if [ ! -f "/home/ubuntu/edupilot/services/.env" ]; then
    echo "  ✗ No .env file found at services/.env"
    echo "  Upload it first:"
    echo "    scp -i edupilot-prod-key.pem .env.production ubuntu@13.212.58.39:/home/ubuntu/edupilot/services/.env"
    exit 1
fi
# Inject the postgres password we just set
sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$POSTGRES_PASSWORD/" /home/ubuntu/edupilot/services/.env
echo "✓ .env file present"

# ── 8. Database init ─────────────────────────────────────────────────────────
echo ""
echo "→ Initializing database tables..."
cd /home/ubuntu/edupilot/services
source venv/bin/activate
python3 -c "
from app.db.session import init_db
init_db()
print('  ✓ Tables created / verified')
"

# ── 9. Initial data seed ─────────────────────────────────────────────────────
echo ""
echo "→ Seeding initial opportunity data..."
python3 reseed.py && echo "✓ Data seeded" || echo "  ⚠ Seeding had errors — check logs, continuing..."

# ── 10. ChromaDB data dir ─────────────────────────────────────────────────────
mkdir -p /home/ubuntu/edupilot/services/chroma_data
echo "✓ ChromaDB data directory ready"

# ── 11. systemd: FastAPI ─────────────────────────────────────────────────────
echo ""
echo "→ Installing EduPilot API systemd service..."
sudo cp /home/ubuntu/edupilot/services/edupilot.service /etc/systemd/system/edupilot.service
sudo systemctl daemon-reload
sudo systemctl enable edupilot
sudo systemctl restart edupilot
sleep 3

if sudo systemctl is-active --quiet edupilot; then
    echo "✓ EduPilot API service running"
else
    echo "✗ EduPilot API failed to start"
    echo "  Logs: journalctl -u edupilot -n 50"
    exit 1
fi

# ── 12. systemd: Celery Worker ────────────────────────────────────────────────
echo ""
echo "→ Installing Celery Worker systemd service..."
sudo cp /home/ubuntu/edupilot/services/edupilot-worker.service /etc/systemd/system/edupilot-worker.service
sudo systemctl daemon-reload
sudo systemctl enable edupilot-worker
sudo systemctl restart edupilot-worker
sleep 3

if sudo systemctl is-active --quiet edupilot-worker; then
    echo "✓ Celery Worker running"
else
    echo "✗ Celery Worker failed to start"
    echo "  Logs: journalctl -u edupilot-worker -n 50"
    exit 1
fi

# ── 13. systemd: Celery Beat ──────────────────────────────────────────────────
echo ""
echo "→ Installing Celery Beat systemd service..."
sudo cp /home/ubuntu/edupilot/services/edupilot-beat.service /etc/systemd/system/edupilot-beat.service
sudo systemctl daemon-reload
sudo systemctl enable edupilot-beat
sudo systemctl restart edupilot-beat
sleep 2

if sudo systemctl is-active --quiet edupilot-beat; then
    echo "✓ Celery Beat running"
else
    echo "✗ Celery Beat failed to start"
    echo "  Logs: journalctl -u edupilot-beat -n 50"
    exit 1
fi

# ── 14. nginx ─────────────────────────────────────────────────────────────────
echo ""
echo "→ Configuring nginx..."
sudo cp /home/ubuntu/edupilot/services/nginx.conf /etc/nginx/nginx.conf
sudo nginx -t && echo "✓ nginx config valid"
sudo systemctl enable nginx
sudo systemctl restart nginx
echo "✓ nginx running"

# ── 15. Firewall ──────────────────────────────────────────────────────────────
echo ""
echo "→ Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 8000/tcp
sudo ufw --force enable
echo "✓ Firewall configured (80, 443 open; 8000 blocked externally)"

# ── 16. Health check ─────────────────────────────────────────────────────────
echo ""
echo "→ Running health check..."
sleep 2
HEALTH=$(curl -s http://localhost:8000/health || echo "FAILED")
echo "  Response: $HEALTH"

if echo "$HEALTH" | grep -q "ok"; then
    echo "✓ Backend is healthy"
else
    echo "✗ Health check failed"
    echo "  Logs: journalctl -u edupilot -n 50"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════"
echo " Deploy complete!"
echo "════════════════════════════════════════════"
echo ""
echo "SERVICES RUNNING:"
echo "  edupilot          → FastAPI on localhost:8000"
echo "  edupilot-worker   → Celery workers (scrapers run here)"
echo "  edupilot-beat     → Scheduler (2AM daily scrape, hourly deadline scan)"
echo "  nginx             → Reverse proxy on port 80"
echo ""
echo "MANUAL STEPS:"
echo ""
echo "1. CLOUDFLARE DNS:"
echo "   → devedupilot.xyz → DNS → Add record:"
echo "       Type:   CNAME"
echo "       Name:   api"
echo "       Target: 13.212.58.39"
echo "       Proxy:  ENABLED (orange cloud) ← required for free HTTPS"
echo ""
echo "2. CLOUDFLARE SSL MODE:"
echo "   → SSL/TLS → Overview → set to 'Flexible'"
echo ""
echo "3. EC2 SECURITY GROUP (AWS Console):"
echo "   → Edit inbound rules — ensure open:"
echo "       Port 22   SSH    — your IP only"
echo "       Port 80   HTTP   — 0.0.0.0/0"
echo "       Port 443  HTTPS  — 0.0.0.0/0"
echo "   → Port 8000 must NOT be open"
echo ""
echo "4. TEST:"
echo "   curl https://api.devedupilot.xyz/health"
echo "   Expected: {\"status\":\"ok\",\"mvp_agent\":\"scholarship\",\"version\":\"1.0.0\"}"
echo ""
echo "USEFUL COMMANDS:"
echo "  API logs:     journalctl -u edupilot -f"
echo "  Worker logs:  journalctl -u edupilot-worker -f"
echo "  Beat logs:    journalctl -u edupilot-beat -f"
echo "  Restart all:  sudo systemctl restart edupilot edupilot-worker edupilot-beat"
echo "  Run scrape now (don't wait for 2AM):"
echo "    cd /home/ubuntu/edupilot/services && source venv/bin/activate"
echo "    celery -A app.tasks call app.tasks.run_daily_ingestion"
echo ""
