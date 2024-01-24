# Dockerized rclone with Automount

This originally started as a learning experience for me to get rclone configured that I wanted to document... but as I was going through the motions I found it surprisingly difficult to find something that was plug and play. After getting rclone installed directly on a host I decided I wanted to make this as easy as possible to manage and redeploy which led me to my three requirements:

1. Use the rclone WebGUI
2. Enable automatic mounting of remotes on host restart
3. Have everything in Docker

As a bonus, I also wanted this to optionally integrate with an nginx reverse proxy.

My main reason for wanting the WebUI was for the simplicity of controlling or toggling global upload/download speed limits manually... though arguably the API is robust enough this could be automated. An added benefit was being able to control the (base) config settings for clone.

Having everything in Docker aligns with the goal of having everything as containerized and ready to deploy as possible. It also integrated nicely with my existing reverse proxy configuration.

## Requirements

For easy of deployment, this will use [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/). Ensure you have both installed.

rclone uses fuse for some mounts, run `sudo apt update && sudo apt install fuse3 -y` or whatever the appropriate flavor for your distro is.

## Installation

### Pre-work

Navigate to the directory you are planning on using for your Docker bind mounts for the rclone configuration files. This is not necessarily where you will have rclone mount remotes. If using the base compose file, we'll create the folders rclone will store its WebUI, config file, and logs in.

```
mkdir cache && mkdir config && mkdir logs
```

Then we can create or download the [docker-compose.yml](docker-compose.yml) in this repo

```
wget https://github.com/coanghel/rclone-docker-automount/blob/master/docker-compose.yml
```

The same goes for the [mounts.json](mounts.json)

```
wget https://github.com/coanghel/rclone-docker-automount/blob/master/mounts.json
```

### Compose Configuration

The key points to populate in the compose file are the rc port, user and password. Note that these need to be supplied for both containers and that we are passing `:PORT` for --rc-addr, not just `PORT`

```
...
    command:
...
      - --rc-addr=:5572
      - --rc-user=AGOODUSERNAME
      - --rc-pass=AGOODPASSWORD
...
  rclone_initializer:
...
    environment:
      - RCLONE_USERNAME=AGOODUSERNAME
      - RCLONE_PASSWORD=AGOODPASSWORD
      - RCLONE_PORT=5572
...
```

### rclone configuration

Before the auto-mount container will work, we need to first generate an rclone.conf file. This can be done from the WebUI **however** this will fail for any remote that uses an OAuth 2.0 auto-code flow. Even doing it from the command line on a direct install of rclone can hit a dead end with some providers if you are running on a headless machine. See [Limitations](##Limitations) for more details.

By far the easiest way to generate an rclone.conf is to download the rclone binary directly (ensure you are using the same version as packaged in their Docker image unless you specify a specific version tag in your compose) and use the interactive `rclone config` command. Follow [their documentation](https://rclone.org/commands/rclone_config/) for configuring a remote. Once complete, you can just copy this.conf to the ./config directory we created in [Pre-work](###Pre-work)

### Initializer configuration

The initializer is a simple script that waits for the remote service in the rclone container to be active (even with the `depends_on:` parameter in the compose, sometimes rclone hasn't finished standing up the rc endpoint) and then creates mounts for everything you supply in your [mounts.json](mounts.json).

You can provide specific parameters as detailed in [rclone Config Options](/rclone%20Config%20Options/) to have multiple remotes mounted. In the example below, we mount a OneDrive and a Google Drive remote

```
[
  {
    "fs": "OneDrive:",
    "mountPoint": "/hostfs/onedrive/onedrive_0",
    "mountOpt": {
      "AllowOther": true
    },
    "vfsOpt": {
      "CacheMode": "full"
    }
  },
  {
    "fs": "GoogleDrive:",
    "mountPoint": "/hostfs/gdrive/grive_0",
    "mountOpt": {
      "AllowOther": true
    },
    "vfsOpt": {
      "CacheMode": "full"
    }
  }
]
```

The container is configured to only run once per host boot unless manually restarted. If mounts don't show up, inspect the container logs of rclone_initializer or of rclone in the `./logs` folder. Remember you can modify the `--log-level` flag on the rclone container to see more verbose information.

### Startup

Navigate to the directory with your docker-compose.yml and run

```
docker compose up -d
```

That's it!

If you generated new remote configs and want to test that your mounts.json is valid/functional, simply unmount them through the UI and then run

```
docker compose down && docker compose up -d
```

### Alternate installation

If you would rather build your own docker image instead of using the one hosted here you will need to copy this repo and then use the docker build command

```
git clone https://github.com/coanghel/rclone-docker-automount.git
cd rclone-docker-automount
docker build -t rclone-init:latest .
```

You will also need to update the docker-compose.yml to point to your local image

```
version: "3.7"
services:
...
  rclone_initializer:
    image: docker.io/library/rclone-init:latest
...
```

## Limitations

There are two main limitations of this configuration; one is inherent to the rclone WebGUI and the other is related to how the "parent" RC remote handles mounts through the UI.

1. As mentioned during our [rclone configuration](###rclone-configuration), OAuth 2.0 remotes with auth-code flows don't work in the UI. This is related to how the WebGUI handles the authorization code redirect.
2. Adding remotes directly through the UI is fully functional, but they will not auto-mount on a system boot because the mounts.json is not updated during this action. As far as I am aware, the rc mount/listmounts endpoint provides the filesystem and mount point, but not the mountOpt and vfsOpt blocks submitted when the mount was created.

## Acknowledgements

The [rclone team](https://github.com/rclone) and [community](https://forum.rclone.org/) are amazing. Support them!
