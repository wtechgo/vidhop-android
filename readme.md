# VidHop Android

## Description

Download videos, channels, playlists, music...with metadata or only metadata and query the metadata with one simple command
to search your favorite videos and channels on Android.

## Installation

1. Install [Termux from F-droid](https://f-droid.org/en/packages/com.termux/) on Android.
2. Open Termux and paste this command.

    ```   
       curl -sL https://raw.githubusercontent.com/wtechgo/vidhop-android/master/install.sh > install.sh && 
       chmod +x install.sh && ./install.sh && rm install.sh && . $PREFIX/etc/bash.bashrc && . vidhop
    ```   

3. Check if it works: download a video and play it !

    ```
       dlv https://www.youtube.com/watch?v=-DT7bX-B1Mg && ls -l && sleep 3 && play
     ```

## Functional Information

VidHop enables Android users to download videos, songs, thumbnails, complete channels and playlists from popular video
platforms to their phones.

Each download also saves the video **metadata** and its thumbnail (video banner image). When users download a channel or
playlist, the same happens for each video while also saving channel metadat. It's also possible to fetch **only** the
metadata of a video, channel or playlist.

**The metadata is what makes VidHop powerful** as it provides functions for users to query their collected metadata
using search words or sentences. Effectively, VidHop will look for the search word in video titles and descriptions
though the metadata contains other useful data like video, channel and thumbnail urls. File extensions incude mp4 (
video), json (metadata) and jpg (thumbnails).

Finally, VidHop provides many utilities for day-to-day use such as keeping a history, renaming of downloaded files,
inspect video specs for files and urls, remove the last download or play it...

## Technical Information

VidHop is in essence a collection of bash scripts users load in terminal via `bash.bashrc` or by calling the loader
`. vidhop` or `source vidhop`. `bash.bashrc is the Termux equivalent of `.bashrc` in Linux.

We enable a terminal in Android by installing [Termux from F-droid](https://f-droid.org/en/packages/com.termux/).
Installing Termux from Google Play is not recommended as this is an old version.

VidHop uses [YT-DLP](https://github.com/yt-dlp/yt-dlp) (written in Python) for downloading videos and metadata.
`install.sh` also installs FFmpeg for converting YT-DLP download when necessary.

Handling metadata JSON files happens with [JQ](https://github.com/stedolan/jq).

Finally, VidHop (`install.sh`) installs a bunch of useful packages
like `openssh, rsync, mediainfo, selenium and beautifulsoup4 (for scraping channel avatar images) and tor, proxychains-ng (for dealing with censored videos)`
.

`install.sh` resolved several issues, listed [here](#issues-installsh-resolved)

## VidHop Sync

Phones have limited storage so users will want to transfer their downloads from their phone to their computer.

Moreover, metadata collected on the computer has to be copied to the phone so users can query their video library 
while on the move.

VidHop provides command `syncvidhop` for this scenario though SSH has to be configured such that laptop and phone can 
establish an SSH connection.

Note: Configuring VidHop Sync is not required for downloading videos, channels, metadata etc. to work.

### Configuration

For explanation purposes, we'll use the scenario of syncing between laptop and phone (bi-directional).

If you ran `install.sh`, `openssh` (SSH) and rsync have already been installed in Termux. However, you might not have 
installed these packages on your laptop. If not, install them.

The easiest way to go about this, is to establish an SSH connection from laptop to phone first, to avoid typing on the phone. 
**Termux SSH requires RSA keys**.

#### Overview

Let's first consider an overview of how to configure SSH. The next chapter goes into detail.

- Generate SSH keys on laptop.
- Copy laptop public SSH key onto phone.
- Establish an initial SSH connection from laptop to phone and **accept the device fingerprint**.
- On phone, repeat the 3 previous steps.
- Inform VidHop on laptop of the IP-address and user of phone.
- Inform VidHop on phone of the IP-address and user of laptop.

#### SSH Configuration Laptop

If you don't have SSH installed on laptop, install package `openssh`.  
You can check if it's installed with `which sshd`, `type sshd` or by trying to start it with `systemctl start sshd`.

```
PHONE_USER="FILL_IN_PHONE_USER"
PHONE_IP="FILL_IN_PHONE_IP"

# Generate RSA keys. To dodge password prompts, leave password empty, just hit enter for each question.
ssh-keygen -t rsa -b 4096 -f id_vidhop

# Copy you public key to phone.
# Make sure `sshd` is running on phone first. Open Termux and run `sshd`.
ssh-copy-id -i ~/.ssh/id_vidhop -p 22 $PHONE_USER@$PHONE_IP

# Make an initial SSH connection and accept the the device fingerprint of laptop.
ssh -4 -p 8022 $PHONE_USER@$PHONE_IP 
```

#### SSH Configuration Phone

We recommend you use the SSH connection from the previous part to do this configuration on phone so you can type 
on your keyboard instead of finger-typing on your droid.

```
LAPTOP_USER="FILL_IN_LAPTOP_USER"
LAPTOP_IP="FILL_IN_LAPTOP_IP"

# Generate RSA keys. To dodge password prompts, leave password empty, just hit enter for each question.
ssh-keygen -t rsa -b 4096 -f id_vidhop

# Copy you public key to laptop.
# Make sure `sshd` is running on laptop first. Open a terminal and run `systemctl start sshd` (or distro equivalent).
ssh-copy-id -i ~/.ssh/id_vidhop -p 8022 $LAPTOP_USER@LAPTOP_IP

# Make an initial SSH connection and accept the the device fingerprint of phone.
ssh $LAPTOP_USER@LAPTOP_IP
```

#### Inform VidHop of your SSH connection

1. Make sure you have a working SSH connection between your phone **and** the laptop (SSH instructions above).
2. On the phone in Termux, tell VidHop the IP-address and the user of **laptop**.
   ```
   # opens the sync script in nano editor
   nanosync
   
   # replace these placeholders and **save** the file with CTRL+x, type 'y', press 'enter'
   # WS stands for workstation, in our case it represents laptop.
   IP_WS="REPLACE_WITH_YOUR_LAPTOP_IP_ADDRESS"
   USER_WS="REPLACE_WITH_YOUR_LAPTOP_USER"
   ```
   To get hold of the **user** on your **laptop**, open a terminal on laptop and run `whoami`.

   To find out your **IP-address** on your **laptop**, run one of these (whichever works):

   ```
   ip addr              # install package `iproute2` if command is missing
   ifconfig -a          # install package `net-tools` if command is missing
   ipaddr -pa wlan0     # install package `moreutils` if command is missing
   hostname -I       
   ```
3. Make sure `sshd` is running on the other device.
    - Start `sshd` on **laptop** with `systemctl start sshd`.  
      If you don't have `sshd`, install `openssh` package.
    - start `sshd` on **phone** with `sshd`

Here are the [Termux docs for configuring SSH](https://wiki.termux.com/wiki/Remote_Access) just in case.


#### Inform VidHop of your SSH connection

1. On **Phone**
   - 1.1. Open the sync script in nano editor.
        > nanosync
   
   - 1.2. Replace the placeholders (REPLACE_WITH...) with the IP-address and user of laptop.
      > IP_WS="REPLACE_WITH_YOUR_LAPTOP_IP_ADDRESS"  
        USER_WS="REPLACE_WITH_YOUR_LAPTOP_USER"

      To get hold of the **user** on **laptop**, open a terminal on laptop and run `whoami`.
      
      To find out your **IP-address** on **laptop**, run one of these (whichever works):
   
      ```
      ip addr              # install package `iproute2` if command is missing
      ifconfig -a          # install package `net-tools` if command is missing
      ipaddr -pa wlan0     # install package `moreutils` if command is missing
      hostname -I       
      ```
   - 1.3. **Save** the file with CTRL+x, type 'y', press 'enter'
2. On **Laptop** (similar to 1.) 
   - 1.1. Open the sync script in nano editor.
        > nanosync
   
   - 1.2. Replace the placeholders (REPLACE_WITH...) with the IP-address and user of **phone**.
      > IP_WS="REPLACE_WITH_YOUR_LAPTOP_IP_ADDRESS"  
        USER_WS="REPLACE_WITH_YOUR_LAPTOP_USER"

      To get hold of the **user** and **IP-address** of **phone**,  
      open Termux and run `sshconfig` (sshconfig is a VidHop function).
   - 1.3. **Save** the file with CTRL+x, type 'y', press 'enter'
3. Make sure `sshd` is running on the other device.
    - Start `sshd` on **laptop** with `systemctl start sshd`.  
    - Start `sshd` on **phone** with `sshd`.
4. Run `syncvidhop`
5. Alternatively, you can run `sendvidhop` or `fetchvidhop` for one-directional file sync.

Here are the [Termux docs for configuring SSH](https://wiki.termux.com/wiki/Remote_Access) just in case.

## Censored videos

Censored videos are often still accessible via [Tor browser](https://www.torproject.org/download/). You can still use
VidHop in such scenarios with this workaround.

1. Install tor. `pkg install tor`
2. Install proxychains-ng. `pkg install proxychains-ng`
3. [**Optional**: [Configure proxychains-ng SOCKs5](https://www.youtube.com/watch?v=ebxUrLIoesE)]
    - 3.1. `nano $prefix/etc/proxychains.conf`. 
    - 3.2. Comment `strict_chain`. 
    - 3.3. Uncomment `dynamic_chain`. 
    - 3.4. Add `socks5 127.0.0.1 9050` under `socks5 127.0.0.1 9050`. 
    - 3.5. I bumped on error for SOCKs5 `WARN: Rejecting SOCKS request for anonymous connection to private address [scrubbed]`.
4. Start Tor. two options.
    - 4.1. Run Tor in the background. `tor &`. Press enter to regain your keyboard after Tor has
   finished loading.
     - 4.2. Run `tor` and switch to another session: inside Termux, swipe from left to right and
   press 'new session'.
     - 4.3. Explanation: when you run Tor it occupies the terminal as a running process which blocks
   interaction with the terminal.
5. Start a new shell session under proxychains-ng. `proxychains4 bash`.
6. Inside the new shell, verify you have another IP-address. `curl ifconfig.me`.
7. Execute a VidHop command e.g. `dlv https://www.youtube.com/watch?v=-DT7bX-B1Mg`.

## Issues `install.sh` resolved

These issues have been resolved in the installation script.

### Allow Termux to open files in 'shared'

- open or create ~/.termux/termux.properties
- add line `allow-external-apps=true`

### Configure a default text editor

[Create a symbolic link in `~/bin`](https://wiki.termux.com/wiki/Intents_and_Hooks) to
your [favorite editor](https://wiki.termux.com/wiki/Text_Editors).  
`ln -s $PREFIX/bin/nano ~/bin/termux-file-editor`

### Rsync error caused by Termux welcome message

> rsync error: protocol incompatibility (code 2) at compat.c(608) [sender=v3.2.4]

Remove the Termux welcome message.  
`touch ~/.hushlogin`

## Credits

Special thanks to the incredibly awesome projects [YT-DLP](https://github.com/yt-dlp/yt-dlp),
[JQ](https://github.com/stedolan/jq) and [Termux](https://f-droid.org/en/packages/com.termux/).

## Support

<h3>Buy Me A Coffee</h3>
<a href="https://www.buymeacoffee.com/wtechgo">
<img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee - WTechGO" width="150" />
</a>
<h3>Bitcoin</h3>
<a href="https://github.com/wtechgo/vidhop-android/blob/master/img/qr_bitcoin_wtechgo.png?raw=true">
<img src="https://github.com/wtechgo/vidhop-android/blob/master/img/qr_bitcoin_wtechgo.png?raw=true" alt="Bitcoin" width="100"/>
</a>
<pre>bc1qkxqz0frjhx6gshm0uc668zx6686xtfsxdm67u3</pre>
<h3>Monero</h3>
<a href="https://github.com/wtechgo/vidhop-android/blob/master/img/qr_monero_wtechgo.png?raw=true">
<img src="https://github.com/wtechgo/vidhop-android/blob/master/img/qr_monero_wtechgo.png?raw=true" alt="Monero" width="100" />
</a>
<pre>8BNDojnvwYkacFwztY3XsjefCr28zTDraTgzdFLH8JiL5W4eMjTuHCu57LkCy9UHKHZfGzWDo6ErDYDP4jBK814aG2T8z8c</pre>
