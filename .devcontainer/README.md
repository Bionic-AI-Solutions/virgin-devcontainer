# DevContainer Setup

This devcontainer provides a complete development environment for Node.js and Python projects with Docker and Kubernetes support.

## Best Practices Applied

This devcontainer follows industry best practices:
- ✅ Docker build context set to `.devcontainer/` directory (not parent)
- ✅ Version-pinned dependencies for reproducibility
- ✅ `.dockerignore` file to optimize build performance
- ✅ No `--privileged` flag (using host Docker daemon instead)
- ✅ Security-focused configuration with read-only mounts

## Features

- **Python 3.11** with Poetry for dependency management
- **Node.js 20.x** with npm and common development tools
- **Docker CLI** - Installed in container; connects to host Docker engine via mounted socket
- **GitHub CLI (gh)** - Installed for repo management and auth
- **Claude Code CLI** - Installed on first start via post-create script (`~/.local/bin`)
- **agent-browser** - Installed globally via npm; Chromium downloaded by post-create
- **kubectl** - Installed in container; uses mounted `~/.kube/config` for cluster access
- **Development Tools**:
  - Python: black, flake8, pylint, pytest, pytest-asyncio, mypy
  - Node.js: TypeScript, ts-node, ESLint, Prettier, nodemon

## Prerequisites

- Docker Desktop or Docker Engine running on your host
- VS Code (or Cursor) with the "Dev Containers" extension installed
- Docker socket accessible (default: `/var/run/docker.sock`)

**Required for mounts (container will fail to start if these are missing):**

The devcontainer uses **`USERPROFILE`** (Windows) / **`HOME`** for these paths. Ensure the following exist on the host:

- **`<USERPROFILE or HOME>/.kube`** – Folder. Create an empty folder if you don’t use Kubernetes yet.  
  - Windows: `C:\Users\<You>\.kube` (uses `USERPROFILE`)  
  - macOS/Linux: `~/.kube` (set `USERPROFILE=$HOME` in your shell profile if mounts fail)
- **`<USERPROFILE or HOME>/.cursor/mcp.json`** – File. Use `{}` if you don’t use MCP.  
  - Windows: `C:\Users\<You>\.cursor\mcp.json`  
  - macOS/Linux: `~/.cursor/mcp.json`

**One-time setup (Windows PowerShell)** – run before first open if those paths don’t exist:

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.kube; New-Item -ItemType Directory -Force $env:USERPROFILE\.cursor; if (!(Test-Path $env:USERPROFILE\.cursor\mcp.json)) { '{}' | Set-Content $env:USERPROFILE\.cursor\mcp.json }
```

## What Gets Mounted

The devcontainer automatically mounts:

1. **Docker Socket** (`/var/run/docker.sock`) - Container Docker CLI talks to host Docker engine
2. **Kubernetes Config** (`~/.kube`) - Your Kubernetes cluster configuration
3. **MCP Config** (`~/.cursor/mcp.json`) - MCP server configuration for Cursor

## Usage

1. Open the project in VS Code
2. When prompted, click "Reopen in Container" or use Command Palette: `Dev Containers: Reopen in Container`
3. Wait for the container to build and start (first time may take a few minutes)
4. The post-create script will automatically:
   - Install Claude Code CLI (if not present)
   - Install agent-browser and download Chromium
   - Verify Docker (host engine), kubectl, and gh
   - Create Python virtual environment if needed
   - Install Node.js dependencies if `package.json` exists
   - Install Python dependencies with Poetry if `pyproject.toml` exists

## Verifying Setup

Once the container is running, verify everything works:

```bash
# Check Python
python3 --version  # Should show Python 3.11.13

# Check Node.js
node --version  # Should show v20.19.6

# Check Poetry
poetry --version  # Should show Poetry version

# Check Docker (uses host daemon)
docker ps

# Check kubectl
kubectl version --client
kubectl cluster-info  # Should show your cluster info

# Check GitHub CLI
gh --version

# Check Claude Code CLI (after first post-create)
claude --version
```

## Adding .cursorrules

If you have a `.cursorrules` file in your workspace root, you can add it to the mounts in `devcontainer.json`:

```json
"source=${localWorkspaceFolder}/.cursorrules,target=/workspace/.cursorrules,type=bind,readonly"
```

## Troubleshooting

### "Rebuild and open" or "Failed to create container" / mount errors

1. **Create mount paths on the host** (most common cause on Windows):
   - Create folder: `%USERPROFILE%\.kube` (e.g. `C:\Users\YourName\.kube`)
   - Create file: `%USERPROFILE%\.cursor\mcp.json` with content `{}` (create `.cursor` folder if needed)
   - Then try **Dev Containers: Rebuild and Reopen in Container** again.

2. **Docker Desktop** must be running before opening the dev container.

3. **Post-create script failed**: Optional installs (Claude CLI, agent-browser) no longer fail the container; you’ll see warnings but the container should still open. If it still fails, check the **Dev Containers** output panel for the exact error.

### Docker not accessible
- Ensure Docker Desktop/Engine is running on your host
- Check that `/var/run/docker.sock` exists and is accessible

### kubectl not working
- Verify `~/.kube` exists on your host and contains `config` (or an empty folder is fine)
- kubectl is installed inside the container; the mount only provides your cluster config

### Permission issues
- The container runs as user `vscode` (UID 1000)
- Docker and kubectl mounts are set up automatically via the post-create script

## Customization

You can customize the devcontainer by:

- Modifying `.devcontainer/Dockerfile` to add additional tools
- Updating `.devcontainer/devcontainer.json` to change VS Code settings or extensions
- Editing `.devcontainer/post-create.sh` to add custom setup steps




