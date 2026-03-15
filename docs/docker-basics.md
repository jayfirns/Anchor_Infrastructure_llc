# Docker Basics

## What Is Docker?

Docker packages software into **containers** — self-contained bundles that include everything a service needs to run: the code, the libraries, the configuration. No "works on my machine" problems. No dependency conflicts. No installing 47 packages just to run a password manager.

You tell Docker "run this container" and it runs. Same way. Every time.

## What Is Docker Compose?

Docker Compose lets you define **multiple containers** in one file and start them all together. Instead of running three separate `docker run` commands with 15 flags each, you write a `docker-compose.yml` file and run:

```bash
docker compose up -d
```

That's it. Everything starts. The `-d` means "in the background" so you get your terminal back.

## Reading a docker-compose.yml

Here's what a real one looks like (this is from the [Seed Stack](../seed-stack/)):

```yaml
services:
  pihole:                          # Name of the service
    image: pihole/pihole:latest    # Which container image to use
    container_name: pihole         # What to call the running container
    restart: unless-stopped        # Restart automatically if it crashes
    ports:
      - "53:53/tcp"                # Map host port 53 to container port 53
      - "53:53/udp"                # DNS uses both TCP and UDP
      - "80:80/tcp"                # Web admin interface
    environment:
      TZ: "America/Chicago"        # Timezone for logs
      WEBPASSWORD: "your-password" # Admin panel password
    volumes:
      - pihole_data:/etc/pihole    # Persist data across restarts
```

Line by line:

| Line | What It Means |
|------|--------------|
| `image: pihole/pihole:latest` | Download this container image from Docker Hub (like an app store for containers) |
| `restart: unless-stopped` | If the container crashes or the machine reboots, Docker restarts it automatically |
| `ports: "53:53/tcp"` | Traffic hitting port 53 on your machine gets forwarded to port 53 inside the container |
| `environment:` | Configuration values passed into the container (like settings) |
| `volumes:` | Data that persists even if you delete and recreate the container |

## Essential Commands

You only need about six commands:

```bash
# Start everything defined in docker-compose.yml
docker compose up -d

# See what's running
docker compose ps

# See logs (follow mode, Ctrl+C to stop watching)
docker compose logs -f

# Stop everything
docker compose down

# Pull updated images and restart
docker compose pull && docker compose up -d

# See resource usage
docker stats
```

## Installing Docker

### Ubuntu / Debian / Raspberry Pi OS

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and back in for the group change to take effect
```

### Verify It Works

```bash
docker run hello-world
```

If you see "Hello from Docker!" — you're good.

## Key Concepts

### Images vs. Containers

An **image** is the blueprint. A **container** is a running instance of that image. You can run multiple containers from the same image. Think of it like a recipe (image) vs. the actual dish (container).

### Volumes

Containers are ephemeral — if you delete one, its data is gone. **Volumes** store data outside the container so it survives restarts, updates, and recreations. Always use volumes for anything you care about keeping.

### Ports

Containers are isolated. They can't talk to the outside world unless you map ports. `"8080:80"` means "traffic on port 8080 on my machine goes to port 80 inside the container." That's how you access the web UIs.

### Networks

Docker creates a virtual network for your containers. They can talk to each other by name (e.g., the monitoring container can reach the DNS container by calling it `pihole`). You generally don't need to configure this — Docker Compose handles it.

## What Can Go Wrong

| Problem | Fix |
|---------|-----|
| `permission denied` when running docker | Run `sudo usermod -aG docker $USER` and log out/back in |
| Port already in use | Something else is using that port. Find it: `sudo lsof -i :PORT_NUMBER` |
| Container keeps restarting | Check logs: `docker compose logs SERVICE_NAME` |
| Ran out of disk space | Clean up: `docker system prune -a` (removes unused images) |
| Forgot what's running | `docker compose ps` or `docker ps` to see all containers |

## Next Steps

- **[Johnny's Favorite Containers](johnnys-favorites.md)** — Real services worth running
- **[Try the Seed Stack](../seed-stack/)** — Put this knowledge to use
