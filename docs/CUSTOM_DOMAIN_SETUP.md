# Custom Domain Setup Guide - ThreatLens Platform

This guide outlines how to bind your custom production domain (e.g., `security.yourcompany.com` or `threatlens.io`) to the ThreatLens Firebase platform.

---

## 1. Firebase Hosting Custom Domain Configuration

ThreatLens is pre-configured with Google Cloud Firebase Hosting (`phishy-app-f5891`). Google automatically provisions and renews SSL certificates (TLS 1.3) at zero cost via Let's Encrypt once your DNS records propagate.

### Option A: Firebase Console (Fastest)

1. Open the [Firebase Console](https://console.firebase.google.com/project/phishy-app-f5891/hosting/sites).
2. Navigate to **Hosting** in the left sidebar.
3. Click **Add custom domain** (or **Connect domain**).
4. Enter your custom domain name:
   - For a root domain: `yourcompany-security.com`
   - For a subdomain: `security.yourcompany.com`
5. Select whether to redirect `www` to root (or vice versa).
6. Firebase will display your required DNS records.

---

## 2. DNS Record Configuration

Log in to your DNS provider (Cloudflare, AWS Route 53, Namecheap, GoDaddy, etc.) and add the following records:

### For Subdomains (e.g., `security.yourcompany.com`):

| Type | Host / Name | Target / Value | TTL |
| :--- | :--- | :--- | :--- |
| **CNAME** | `security` | `phishy-app-f5891.web.app` | Automatic / 300 |

### For Apex / Root Domains (e.g., `yourcompany-security.com`):

| Type | Host / Name | Value / Destination IP | TTL |
| :--- | :--- | :--- | :--- |
| **A** | `@` | `199.36.158.100` | Automatic / 300 |
| **A** | `@` | `199.36.158.100` | Automatic / 300 |
| **TXT** | `@` | `firebase=phishy-app-f5891` *(Verification)* | Automatic / 300 |

---

## 3. SSL / TLS Verification

- DNS propagation usually completes within 5 to 60 minutes.
- Firebase will automatically verify domain ownership and issue an RSA / ECDSA SSL certificate within 24 hours.
- While the certificate is provisioning, your site remains accessible.

---

## 4. Production Environment Configuration

Once your custom domain is connected, update the `BASE_URL` and `ALLOWED_ORIGINS` in your `.env`:

```env
# .env
BASE_URL=https://security.yourcompany.com
ALLOWED_ORIGINS=https://security.yourcompany.com
DEBUG=False
```

This ensures tracking pixel URLs generated in simulated phishing emails resolve through your enterprise custom domain with active HTTPS.
