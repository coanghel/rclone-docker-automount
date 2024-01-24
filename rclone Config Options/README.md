# Available Options

There are several rclone options, and running with a remote that spawns mounts can complicate this a bit. When supplying mounts in your [mounts.json](../mounts.json), refer to the [rcloneoptions.json](rcloneoptions.json) to see what you are able to pass for mountOpt and vfsOpt.

The defaults used by rclone if you do not specify are below. For details on what these paramters do, consult [rclone's documentation on mounts](https://rclone.org/commands/rclone_mount/#options)

## vfsOpt

```
{
    "CacheMaxAge": 3600000000000,
    "CacheMaxSize": -1,
    "CacheMinFreeSpace": -1,
    "CacheMode": "off",
    "CachePollInterval": 60000000000,
    "CaseInsensitive": false,
    "ChunkSize": 134217728,
    "ChunkSizeLimit": -1,
    "DirCacheTime": 300000000000,
    "DirPerms": 511,
    "DiskSpaceTotalSize": -1,
    "FastFingerprint": false,
    "FilePerms": 438,
    "GID": 0,
    "NoChecksum": false,
    "NoModTime": false,
    "NoSeek": false,
    "PollInterval": 60000000000,
    "ReadAhead": 0,
    "ReadOnly": false,
    "ReadWait": 20000000,
    "Refresh": false,
    "UID": 0,
    "Umask": 18,
    "UsedIsSize": false,
    "WriteBack": 5000000000,
    "WriteWait": 1000000000
}
```

## mountOpt

```
{
    "AllowNonEmpty": false,
    "AllowOther": false,
    "AllowRoot": false,
    "AsyncRead": true,
    "AttrTimeout": 1000000000,
    "CaseInsensitive": null,
    "Daemon": false,
    "DaemonTimeout": 0,
    "DaemonWait": 60000000000,
    "DebugFUSE": false,
    "DefaultPermissions": false,
    "DeviceName": "",
    "ExtraFlags": [],
    "ExtraOptions": [],
    "MaxReadAhead": 131072,
    "NetworkMode": false,
    "NoAppleDouble": true,
    "NoAppleXattr": false,
    "VolumeName": "",
    "WritebackCache": false
}
```
