# MNB Yokoy FX Sync

A simple Python project to fetch foreign exchange rates from the Hungarian National Bank (MNB) and eventually upload them to Yokoy.

## Current Status

**Phase 1: Basic Setup** ✅ COMPLETED

We have a minimal working script that fetches exchange rates from MNB using the public `mnb` library.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Script

```bash
python main.py
```

This will fetch and display the current exchange rates from MNB.

## Project Structure

```
mnb-yokoy-fx-sync/
├── main.py           # Simple script to fetch MNB rates
├── requirements.txt  # Python dependencies (just mnb library)
├── todos.txt        # Project progress tracker
└── README.md        # This file
```

## What It Does Now

- Connects to MNB API using the `mnb` library
- Fetches current exchange rates
- Displays all currency rates in a formatted table

## Next Steps

See `todos.txt` for the complete roadmap. Next phase will add:
- Ability to fetch rates for specific dates
- Command line arguments
- Better error handling

## Requirements

- Python 3.7+
- `mnb` library (from https://github.com/belidzs/mnb)

## About MNB

MNB (Magyar Nemzeti Bank) is the Central Bank of Hungary. They provide a public SOAP API with daily foreign exchange rates. The `mnb` library wraps this API in a clean, Pythonic interface.

A robust, production-ready service that automatically fetches daily foreign exchange rates from the Hungarian National Bank (MNB) SOAP API and uploads them to Yokoy's expense management platform. Features comprehensive error handling, retry logic, and multi-channel notifications.

## 🚀 Features

- **Automated Daily Sync**: Scheduled to run daily after MNB publishes new rates
- **Robust Error Handling**: Exponential backoff, retries, and comprehensive logging
- **Multi-Channel Notifications**: Microsoft Teams webhooks and SMTP email alerts
- **Business Day Logic**: Automatically handles weekends and holidays
- **Idempotency Support**: Prevents duplicate uploads with unique request IDs
- **Security First**: Non-root containers, secrets management, RBAC
- **Production Ready**: Structured logging, health checks, monitoring hooks
- **CI/CD Pipeline**: Automated testing, security scanning, and deployment

## 📋 Prerequisites

- **MNB SOAP API**: No authentication required (public API)
- **Yokoy API Access**: API key and endpoint URL required
- **OpenShift/Kubernetes**: For container deployment
- **Notification Channels** (Optional):
  - Microsoft Teams incoming webhook
  - SMTP server for email notifications

## 🏗️ Architecture

```
┌─────────────┐    SOAP     ┌─────────────┐    REST     ┌─────────────┐
│     MNB     │◄──────────► │  FX Sync    │◄──────────► │    Yokoy    │
│   (SOAP)    │             │   Service   │             │    (API)    │
└─────────────┘             └─────────────┘             └─────────────┘
                                    │
                            ┌───────┴───────┐
                            │ Notifications │
                            ├───────────────┤
                            │ • Teams       │
                            │ • Email       │
                            │ • Logs        │
                            └───────────────┘
```

## 📦 Installation & Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd mnb-yokoy-fx-sync

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy and customize environment configuration:

```bash
cp .env.example .env
# Edit .env with your actual values
```

#### Required Environment Variables

```bash
# Yokoy API (REQUIRED)
YOKOY_API_URL=https://api.yokoy.com/v1
YOKOY_API_KEY=your_yokoy_api_key_here
```

#### Optional Environment Variables

```bash
# Microsoft Teams Notifications
TEAMS_WEBHOOK_URL=https://your-tenant.webhook.office.com/webhookb2/...

# Email Notifications (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
EMAIL_FROM=fx-sync@yourcompany.com
EMAIL_TO=admin@yourcompany.com

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY=2
LOG_LEVEL=INFO
```

### 3. Local Testing

```bash
# Run smoke tests
python run_tests.py smoke

# Run full test suite
python run_tests.py

# Manual execution (with date)
python main.py 2025-11-07

# Manual execution (today/last business day)
python main.py
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t mnb-yokoy-fx-sync:latest .
```

### Run Container

```bash
# Run once
docker run --env-file .env mnb-yokoy-fx-sync:latest

# Run with specific date
docker run --env-file .env mnb-yokoy-fx-sync:latest python main.py 2025-11-07
```

## ☁️ OpenShift Deployment

### Quick Deploy

```bash
# Update configuration
vi openshift/secret.yaml  # Add your API keys and webhook URLs

# Deploy to OpenShift
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment Steps

```bash
# 1. Create namespace and RBAC
oc apply -f openshift/namespace.yaml
oc apply -f openshift/rbac.yaml

# 2. Create configuration
oc apply -f openshift/configmap.yaml
oc apply -f openshift/secret.yaml  # Update values first!

# 3. Deploy CronJob
oc apply -f openshift/cronjob.yaml

# 4. Verify deployment
oc get cronjob -n fx-sync
oc get pods -n fx-sync
```

### Manual Execution

```bash
# Create manual job from CronJob
oc create job manual-sync --from=cronjob/mnb-yokoy-fx-sync -n fx-sync

# Check logs
oc logs -f job/manual-sync -n fx-sync

# Delete manual job
oc delete job manual-sync -n fx-sync
```

## 📊 Monitoring & Observability

### Health Checks

```bash
# Check CronJob status
oc get cronjob mnb-yokoy-fx-sync -n fx-sync

# View recent jobs
oc get jobs -n fx-sync

# Check logs
oc logs -l app=mnb-yokoy-fx-sync -n fx-sync --tail=100
```

### Log Structure

The service uses structured JSON logging:

```json
{
  "timestamp": "2025-11-08T09:00:00Z",
  "level": "info",
  "event": "Fetching exchange rates from MNB",
  "date": "2025-11-07",
  "request_id": "mnb-yokoy-2025-11-07-20251108090000"
}
```

### Metrics & Alerts

Key metrics to monitor:

- **Success Rate**: Percentage of successful daily syncs
- **Execution Time**: Time taken for complete sync
- **Rate Count**: Number of rates fetched and uploaded
- **Error Patterns**: Types and frequency of failures

Recommended alerts:

- Sync failure for >1 day
- Execution time >5 minutes
- Zero rates returned from MNB
- Yokoy API errors

## 🔧 Troubleshooting

### Common Issues

#### 1. MNB SOAP API Errors

```bash
# Check MNB service availability
curl -I http://www.mnb.hu/arfolyamok.asmx?WSDL

# Test SOAP endpoint manually
python -c "from zeep import Client; print(Client('http://www.mnb.hu/arfolyamok.asmx?WSDL').service)"
```

#### 2. Yokoy API Authentication

```bash
# Test API key
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.yokoy.com/v1/health
```

#### 3. Weekend/Holiday Issues

The service automatically handles weekends by fetching the previous business day (Friday). For holidays, you may need to:

- Check MNB holiday calendar
- Run manual sync for the last business day
- Monitor logs for "No exchange rates found" messages

#### 4. Notification Failures

```bash
# Test Teams webhook
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "Test message"}' \
  YOUR_TEAMS_WEBHOOK_URL

# Test SMTP (if configured)
python -c "
import smtplib
server = smtplib.SMTP('YOUR_SMTP_HOST', 587)
server.starttls()
server.login('USER', 'PASS')
print('SMTP OK')
server.quit()
"
```

### Recovery Procedures

#### Missed Daily Sync

```bash
# Run for specific date
oc create job recover-2025-11-07 --from=cronjob/mnb-yokoy-fx-sync -n fx-sync
# Or locally:
python main.py 2025-11-07
```

#### Multiple Day Recovery

```bash
# Script to recover multiple days
for date in 2025-11-05 2025-11-06 2025-11-07; do
  python main.py $date
  sleep 30  # Wait between runs
done
```

## 🔒 Security Considerations

### Secrets Management

- **Never commit secrets** to version control
- Use OpenShift/Kubernetes secrets for sensitive data
- Rotate API keys regularly
- Use principle of least privilege for RBAC

### Network Security

- Service makes outbound HTTPS calls only
- No inbound network access required
- Consider network policies for additional isolation

### Container Security

- Runs as non-root user (UID 1000)
- Read-only root filesystem
- Minimal base image (Python slim)
- Regular security scanning via CI/CD

## 📈 Performance & Scaling

### Resource Requirements

| Environment | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-------------|-------------|-----------|----------------|--------------|
| Development | 50m         | 200m      | 64Mi           | 256Mi        |
| Production  | 100m        | 500m      | 128Mi          | 512Mi        |

### Scaling Considerations

- **Concurrency**: Set to `Forbid` to prevent overlapping runs
- **Timeout**: Jobs timeout after 10 minutes by default
- **History**: Keeps last 3 successful and 5 failed job records
- **Scheduling**: Runs daily at 9:00 AM UTC (adjust for MNB publishing schedule)

## 🧪 Testing

### Unit Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage
python -m pytest test_main.py -v --cov=main --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Integration Tests

```bash
# Run integration tests (requires environment setup)
python run_tests.py

# Run smoke tests only
python run_tests.py smoke
```

### Load Testing

```bash
# Simulate multiple date requests
for i in {1..10}; do
  python main.py 2025-11-0$i &
done
wait
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards

- **Formatting**: Black (`black main.py`)
- **Linting**: Flake8 (`flake8 main.py --max-line-length=100`)
- **Type Hints**: MyPy (`mypy main.py`)
- **Testing**: Pytest with >90% coverage

## 📄 API Reference

### MNB SOAP API

- **Endpoint**: `http://www.mnb.hu/arfolyamok.asmx?WSDL`
- **Method**: `GetExchangeRates(startDate, endDate)`
- **Format**: Date in `YYYY-MM-DD` format
- **Response**: XML with currency rates

### Yokoy API (Expected Format)

```json
POST /exchange-rates
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "rates": [
    {
      "currency": "EUR",
      "rate": 395.50,
      "unit": 1,
      "date": "2025-11-07",
      "baseCurrency": "HUF"
    }
  ],
  "date": "2025-11-07",
  "base_currency": "HUF"
}
```

## 🆘 Support

### Logs and Diagnostics

```bash
# Get recent logs
oc logs -l app=mnb-yokoy-fx-sync -n fx-sync --since=24h

# Debug mode (set LOG_LEVEL=DEBUG)
oc set env cronjob/mnb-yokoy-fx-sync LOG_LEVEL=DEBUG -n fx-sync
```

### Contact Information

- **Technical Issues**: Create GitHub issue
- **Security Concerns**: Email security@yourcompany.com
- **Operational Support**: Check runbook procedures above

## 📚 Additional Resources

- [MNB Web Services Documentation](https://www.mnb.hu/en/web-services)
- [Yokoy API Documentation](https://api-docs.yokoy.com)
- [OpenShift CronJob Documentation](https://docs.openshift.com/container-platform/4.12/nodes/jobs/nodes-nodes-jobs.html)
- [Microsoft Teams Webhook Guide](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/)

---

**Version**: 1.0.0  
**Last Updated**: November 8, 2025  
**License**: MIT