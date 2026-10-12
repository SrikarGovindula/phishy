# Deploying ThreatLens Backend to Render

This guide walks you through deploying the FastAPI backend of ThreatLens to [Render](https://render.com).

---

## Method 1: Automatic Deployment with Render Blueprint (Recommended)

A `render.yaml` specification is included in the root of the repository.

1. **Commit and Push your repository to GitHub**:
   ```bash
   git add .
   git commit -m "Configure Render deployment for ThreatLens backend"
   git push origin main
   ```

2. **Log into Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com).
   - Click **New +** > **Blueprint**.
   - Select your GitHub repository (`SrikarGovindula/phishy`).
   - Render will automatically read `render.yaml` and configure the **Web Service**.

3. **Set Environment Variables**:
   In the Render Dashboard for your service, navigate to **Environment** and verify/add:
   | Key | Recommended Value | Notes |
   |---|---|---|
   | `PYTHON_VERSION` | `3.11.11` | Python runtime |
   | `ENVIRONMENT` | `production` | Production mode |
   | `DEBUG` | `False` | Disable debug logs |
   | `FIREBASE_PROJECT_ID` | `phishy-app-f5891` | Firebase Project ID |
   | `FIREBASE_DATABASE_URL` | `https://phishy-app-f5891-default-rtdb.firebaseio.com/` | Realtime Database URL |
   | `FIREBASE_SERVICE_ACCOUNT_JSON` | `{"type":"service_account",...}` | Paste full content of `service-account.json` |
   | `JWT_SECRET` | *(auto-generated or secret key)* | Key for signing JWTs |
   | `ALLOWED_ORIGINS` | `*` or your frontend URL | Cross-Origin access |

4. Click **Apply** or **Deploy**. Render will build and deploy the service.

---

## Method 2: Manual Web Service Setup (Render Dashboard)

If deploying manually via the dashboard:

1. In [Render Dashboard](https://dashboard.render.com), click **New +** > **Web Service**.
2. Connect your GitHub repository: `SrikarGovindula/phishy`.
3. Configure the service:
   - **Name**: `threatlens-backend`
   - **Region**: `Oregon (US West)` or closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn app:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: `Free`

4. Add **Environment Variables**:
   Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.11`
   - `FIREBASE_PROJECT_ID`: `phishy-app-f5891`
   - `FIREBASE_DATABASE_URL`: `https://phishy-app-f5891-default-rtdb.firebaseio.com/`
   - `FIREBASE_SERVICE_ACCOUNT_JSON`: *(Paste the JSON text from `service-account.json`)*
   - `JWT_SECRET`: `phishy-jwt-secret-key-threatlens-2024-secure`
   - `ALLOWED_ORIGINS`: `*`
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `False`

5. **Health Check Path**:
   Under **Advanced Settings**, set **Health Check Path** to `/health`.

6. Click **Create Web Service**.

---

## Method 3: Docker Deployment on Render

Render can also build and run using Docker:
- **Runtime**: `Docker`
- **Docker Command**: uses existing `backend/Dockerfile`
- **Health Check**: `/health`

---

## Verifying Deployment

Once deployed, Render provides a URL (e.g., `https://threatlens-backend.onrender.com`).
Test it in your browser or with curl:

```bash
# Health check
curl https://threatlens-backend.onrender.com/health

# Output should be:
# {"status":"healthy","database":{"firebase_connected":true,...}}
```
