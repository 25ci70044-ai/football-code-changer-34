# ⚽ Football Code Changer (ERP)

An AI-powered web platform for editing your football game tactics and files on the fly. Now fully optimized for **Vercel** and **Google Gemini**!

### 🤖 Features
- **Maverick AI Assistant**: Now powered by **Google Gemini 1.5 Flash** for high-speed, 100% free coding assistance.
- **In-Browser Editor**: Full Monaco Editor experience with syntax highlighting and live preview.
- **Self-Contained**: The game files are located right in the `/game` folder.
- **Secure AI Proxy**: Your AI keys are handled by the serverless function (never exposed to the browser).

### 🚀 Cloud Deployment (GitHub + Vercel)
This project is pre-configured for **0-cost hosting** on Vercel:

1.  **Push to GitHub**: Upload this entire folder to a new GitHub repository.
2.  **Connect Vercel**: Sign in to [Vercel.com](https://vercel.com) and import your repository.
3.  **Set AI Key**:
    *   In the Vercel Dashboard, go to **Settings > Environment Variables**.
    *   Add a new environment variable:
        *   **Key:** `GEMINI_API_KEY`
        *   **Value:** `AIzaSyAB1yiaZJGYsthdwqVezeWAP6pARvVLK04` (or your personal key from [aistudio.google.com](https://aistudio.google.com/app/apikey))
4.  **Deploy!**: Every update you push to GitHub will automatically update your live site.

### 🛡️ Local Quick Start
1.  Ensure you have Python installed.
2.  Run the local server:
    ```bash
    python server.py
    ```
3.  Open [http://localhost:8080](http://localhost:8080) in your browser.

### 👤 Default Logins
- Admin: `admin` / `321`
- Striker: `sarthak` / `admin123`

*Built for the Football Gang. ⚽💥*
