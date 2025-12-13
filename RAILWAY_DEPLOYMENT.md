# Railway Deployment for AgentBeats Integration

This repository is configured for separate deployments of green agent, white agent, and controller on Railway to integrate with AgentBeats.

## Quick Deployment

### 1. Deploy Green Agent

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select `xinkaizh/LeetSquad` repository
4. **Configure Service**:
   - **Name**: `leetsquad-green`
   - **Branch**: `clee3` (or `main` after merge)
   - **Start Command**: `uv run local_launcher.py launch green --port $PORT --host 0.0.0.0`
   
5. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=<your-openai-api-key>
   PORT=${{RAILWAY_PUBLIC_PORT}}
   ```

6. **Generate Domain**: Railway Settings → Networking → Generate Domain
   - Your green agent URL: `https://leetsquad-green.up.railway.app`

---

### 2. Deploy White Agent

1. In Railway Dashboard, click **"New Service"** in the same project
2. Select the same `xinkaizh/LeetSquad` repository
3. **Configure Service**:
   - **Name**: `leetsquad-white`
   - **Branch**: `clee3` (or `main` after merge)
   - **Start Command**: `uv run local_launcher.py launch white --port $PORT --host 0.0.0.0`
   
4. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=<your-openai-api-key>
   GREEN_AGENT_URL=https://leetsquad-green.up.railway.app
   PORT=${{RAILWAY_PUBLIC_PORT}}
   ```

5. **Generate Domain**: Railway Settings → Networking → Generate Domain
   - Your white agent URL: `https://leetsquad-white.up.railway.app`

---

### 3. Deploy Controller (for AgentBeats)

1. In Railway Dashboard, click **"New Service"** in the same project
2. Select the same `xinkaizh/LeetSquad` repository
3. **Configure Service**:
   - **Name**: `leetsquad-controller`
   - **Branch**: `clee3` (or `main` after merge)
   - **Start Command**: `uv run local_launcher.py launch controller --port $PORT --host 0.0.0.0 --green-url $GREEN_AGENT_URL --white-url $WHITE_AGENT_URL`
   
4. **Set Environment Variables**:
   ```
   GREEN_AGENT_URL=https://leetsquad-green.up.railway.app
   WHITE_AGENT_URL=https://leetsquad-white.up.railway.app
   PORT=${{RAILWAY_PUBLIC_PORT}}
   ```

5. **Generate Domain**: Railway Settings → Networking → Generate Domain
   - Your controller URL: `https://leetsquad-controller.up.railway.app`

---

## AgentBeats Integration

Once all three services are deployed on Railway:

1. **Go to [AgentBeats](https://v2.agentbeats.org/main)**
2. **Click "Add Agent"** or **"Create Agent"**
3. **Enter Controller URL**: `https://leetsquad-controller.up.railway.app`
4. **Submit**

AgentBeats will:
- Discover agents via `/agents` endpoint
- Access green agent at `/to_agent/<green-id>`
- Access white agent at `/to_agent/<white-id>`

---

## Architecture

```
┌─────────────────────────────────────┐
│  AgentBeats Platform                │
│  Uses: Controller URL               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Controller Service                 │
│  leetsquad-controller.railway.app   │
│  Routes /to_agent/<id> requests     │
└──────────┬────────────┬─────────────┘
           │            │
           ▼            ▼
┌──────────────────┐  ┌──────────────────┐
│  Green Agent     │  │  White Agent     │
│  (Evaluator)     │  │  (Solver)        │
│  Port: Railway   │  │  Port: Railway   │
└──────────────────┘  └──────────────────┘
```

---

## Configuration Files

- **`Procfile.green`**: Process definition for green agent
- **`Procfile.white`**: Process definition for white agent
- **`Procfile.controller`**: Process definition for controller
- **`railway.green.json`**: Railway config for green agent
- **`railway.white.json`**: Railway config for white agent
- **`railway.controller.json`**: Railway config for controller
- **`runtime.txt`**: Python version specification (3.11)
- **`.railwayignore`**: Files to exclude from deployment

---

## Troubleshooting

### Service Not Starting
- Check Railway logs for errors
- Verify environment variables are set correctly
- Ensure `uv` is installed (should be automatic with nixpacks)

### CORS Issues
- CORS middleware is already configured in both agent servers
- Controller also has CORS enabled

### AgentBeats Can't Discover Agents
- Verify controller URL is accessible: `https://your-controller.railway.app/`
- Check `/agents` endpoint returns agent list
- Ensure green/white agent URLs are correct in controller env vars

### Connection Timeouts
- Increase Railway timeout in Settings if needed
- Check if agent backends are running (green/white services)

---

## Local Testing

Before deploying to Railway, test locally:

```bash
# Terminal 1: Green Agent
uv run local_launcher.py launch green

# Terminal 2: White Agent  
uv run local_launcher.py launch white

# Terminal 3: Controller
uv run local_launcher.py launch controller
```

Visit `http://localhost:8000/agents` to verify controller discovers agents.
