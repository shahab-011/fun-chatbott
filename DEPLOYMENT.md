# 🚀 Deployment Guide: Render (Backend) & Netlify (Frontend)

This guide walks you through deploying your **Teacher AI Chatbot** (FastAPI Backend + React/Vite Frontend).

---

## 1. 📦 Prerequisites

1. Ensure your code is committed and pushed to a **GitHub** repository.
2. Sign up / Log in to:
   - [Render](https://render.com/) (For Python FastAPI Backend)
   - [Netlify](https://www.netlify.com/) (For React Vite Frontend)
   - [Groq Console](https://console.groq.com/) (To get your `GROQ_API_KEY`)

---

## 2. 🐍 Deploy Backend on Render

### Option A: Using `render.yaml` (Recommended - Automated Blueprint)

1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` file.
5. In the configuration setup, enter your **`GROQ_API_KEY`**.
6. Click **Apply**. Render will build and deploy your FastAPI server!

---

### Option B: Manual Web Service Setup

1. Click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the service settings:
   - **Name**: `fun-chat-bot` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Select closest to your users
   - **Branch**: `main` (or `master`)
   - **Root Directory**: Leave blank (or `.`)
   - **Build Command**:
     ```bash
     python -m pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     python -m uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
4. **Environment Variables** (Add under *Advanced* / *Environment Variables*):
   - `GROQ_API_KEY`: *(Your Groq API key)*
   - `GROQ_MODEL`: `llama-3.3-70b-versatile`
   - `CORS_ORIGINS`: `*` *(or your Netlify URL after deploying frontend)*
   - `PYTHONPATH`: `.`
5. Click **Create Web Service**.
6. Copy your deployed Backend URL (e.g., `https://fun-chat-bot.onrender.com`).

---

## 3. ⚛️ Deploy Frontend on Netlify

1. Log in to [Netlify Dashboard](https://app.netlify.com/).
2. Click **Add new site** -> **Import an existing project**.
3. Choose **GitHub** and select your repository.
4. Configure Build Settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist` (or `frontend/dist`)
5. Click **Environment variables** (or *Site settings* -> *Environment variables*):
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-render-backend.onrender.com` *(Replace with your actual Render backend URL)*
6. Click **Deploy site**.

---

## 4. 🔒 Post-Deployment (Security & CORS Check)

- Once Netlify gives you a live URL (e.g., `https://your-site.netlify.app`), update your Render Environment Variable:
  - `CORS_ORIGINS`: `https://your-site.netlify.app,http://localhost:5173`
- Test sending messages from your Netlify website to verify real-time AI responses!
