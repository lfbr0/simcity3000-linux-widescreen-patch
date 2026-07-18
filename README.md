# SimCity 3000 Unlimited native Linux HD patch

A reversible binary patch for the native Linux `sc3u.dynamic` executable shipped with the LIFLG SimCity 3000 Unlimited installer.

You need the Loki version of this game.

The original Linux binary accepts only a small hardcoded set of startup resolutions and rewrites unsupported values to fallback modes. This patch bypasses those two validation routines, allowing widescreen and HD resolutions. **Please take care that not all resolutions will work. It's trial and error on your part.**

# IMPORTANT NOTE - DO NOT DO ANYTHING BEFORE READING THIS!

This was built on the shoulders of giants!

You must first apply the patch available in: https://github.com/tetration/Simcity_3000_Linux_Installer

Please check out the great work of Rafael Oliveira: https://github.com/tetration

## Supported binary

The patcher currently supports exactly this build:

```text
SHA-256: d2c94405b1fbfd2ddbf6ffbdefa255587f86d19420f751e64b78d34278fce6d5
File: sc3u.dynamic
```

The hash check is intentional. The script refuses to patch unknown binaries.

## What it changes

The patcher modifies copies of two functions in the executable:

- `FixStartupResolutionValuesIfNeeded(...)`: returns immediately, preventing resolution fallback rewriting.
- `IsStartupResolutionOK(...)`: returns true, accepting the requested startup resolution.

It creates a new file named `sc3u.dynamic.hd`; the original executable is not modified.

## Usage

Copy the original executable somewhere writable:

```bash
mkdir -p ~/Downloads/sc3u-hd-patch
cp /usr/local/games/simcity3000/sc3u.dynamic ~/Downloads/sc3u-hd-patch/
cd ~/Downloads/sc3u-hd-patch
```

Download `patch_sc3u_dynamic_linux_hd.py` into that directory and run:

```bash
chmod +x patch_sc3u_dynamic_linux_hd.py
./patch_sc3u_dynamic_linux_hd.py sc3u.dynamic sc3u.dynamic.hd
```

Install the patched executable alongside the original:

```bash
sudo cp sc3u.dynamic.hd /usr/local/games/simcity3000/
```

Create a separate launcher script:

```bash
sudo cp /usr/local/games/simcity3000/sc3u.dynamic.sh \
  /usr/local/games/simcity3000/sc3u.dynamic.hd.sh

sudo sed -i \
  's/GAME_BINARY="sc3u.dynamic"/GAME_BINARY="sc3u.dynamic.hd"/' \
  /usr/local/games/simcity3000/sc3u.dynamic.hd.sh
```

Test a 16:9 window:

```bash
/usr/local/games/simcity3000/sc3u.dynamic.hd.sh -w -r1360x768
```

Full HD:

```bash
/usr/local/games/simcity3000/sc3u.dynamic.hd.sh -w -r1920x1080
```

## Desktop shortcut example

Create `~/.local/share/applications/liflg_org-simcity3000_hd.desktop`:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Sim City 3000 Unlimited HD Widescreen
GenericName=Sim City 3000 Unlimited HD Widescreen
Comment=Play Sim City 3000 Unlimited in HD widescreen
Icon=/usr/local/games/simcity3000/icon.xpm
Exec=/usr/local/games/simcity3000/sc3u.dynamic.hd.sh -w -r1360x768
Categories=Game;
```

Then refresh the desktop database if necessary:

```bash
update-desktop-database ~/.local/share/applications
```

## Reverting

The original files are untouched. Remove the additional files to revert:

```bash
sudo rm /usr/local/games/simcity3000/sc3u.dynamic.hd
sudo rm /usr/local/games/simcity3000/sc3u.dynamic.hd.sh
```

## Stability

Some resolutions may be unstable because the game was not originally tested with modern display modes. Save frequently and test your chosen resolution before relying on it.

`1360x768` windowed has been tested successfully on a 1920x1080 XFCE desktop.

## Legal

This repository contains no game binaries or proprietary game assets. It only contains a patching utility that operates on a legally obtained local installation.

SimCity and related names are trademarks of their respective owners. This project is unofficial and unaffiliated with Electronic Arts, Maxis, Loki Entertainment Software, or LIFLG.

## Credits

Inspired by Rafael/Tetration's SimCity 3000 HD patch for the Windows executable. The native Linux offsets and patch were independently identified from the LIFLG `sc3u.dynamic` executable.
