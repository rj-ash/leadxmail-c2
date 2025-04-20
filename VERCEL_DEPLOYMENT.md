# Vercel Deployment Guide

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub account
- Vercel CLI (optional)

## Step 1: Prepare Your Repository

1. Make sure your repository has:
   - `app.py` (main FastAPI application)
   - `vercel.json` (Vercel configuration)
   - `requirements.txt` (Python dependencies)
   - `.env.example` (template for environment variables)

2. Push your code to GitHub:
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

## Step 2: Deploy to Vercel

### Option 1: Using Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Configure the project:
   - Framework Preset: Python
   - Root Directory: ./
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: pip install -r requirements.txt

5. Add Environment Variables:
   - Click "Environment Variables"
   - Add your API keys and other sensitive information
   - Make sure to add all variables from your `.env` file

6. Click "Deploy"

### Option 2: Using Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy your project:
```bash
vercel
```

4. Follow the prompts to configure your deployment

## Step 3: Verify Deployment

1. Check the deployment status in your Vercel dashboard
2. Test your API endpoints:
```bash
curl https://your-project-name.vercel.app/health
```

## Step 4: Set Up Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Click "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Environment Variables

Add these environment variables in your Vercel project settings:
```
API_KEY=your_custom_api_key
ZEROBOUNCE_API_KEY=your_zerobounce_api_key
```

## Troubleshooting

1. If deployment fails:
   - Check the build logs in Vercel dashboard
   - Verify all dependencies are in requirements.txt
   - Ensure environment variables are properly set

2. If API endpoints return 500 errors:
   - Check the function logs in Vercel dashboard
   - Verify environment variables are correctly set
   - Test locally with the same environment variables

3. If you need to redeploy:
   - Push new changes to GitHub
   - Vercel will automatically redeploy
   - Or use `vercel --prod` if using CLI

## Important Notes

1. Vercel has a serverless environment, so:
   - Long-running processes may timeout
   - File system is read-only
   - Environment variables are required for sensitive data

2. Keep your `.env` file in `.gitignore`
3. Use Vercel's environment variables for sensitive data
4. Monitor your API usage and limits 