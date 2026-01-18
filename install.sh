#!/bin/bash

BLUE='\e[34m'
GREEN='\e[32m'
NC='\e[0m'

echo -e "Hi, This is the VidHop install script.\n"
echo -e "It will install all required packages and libraries to run VidHop."
echo -e "An overview of what this script does:"
echo -e "    1. Update and upgrade Termux."
echo -e "    2. Install required packages from Termux repositories."
echo -e "    3. Install Python."
echo -e "    4. Install yt-dlp (written in Python)."
echo -e "    5. Install VidHop, includes JQ (library for managing JSON metadata) and Python libs for scraping channel avatar images."
echo -e "    6. Allow Termux access to shared storage."
echo -e "\n${BLUE}Requirements:${NC}"
echo -e "    1. A working internet connection.\n"
echo -n "Finished reading? Press enter: " && read

# 1. Set up Termux after fresh install.
# Source: https://www.facebook.com/117725316811075/posts/apt-update-apt-upgradepkg-update-pkg-upgradepkg-install-gitpkg-install-pythonpkg/148645363719070/
echo -e "Updating and upgrading Termux..."
yes | apt update
yes | apt upgrade
yes | pkg update
yes | pkg upgrade

echo "Installing required packages from termux repositories..." && sleep 1
# mediainfo nano openssh git ncurses moreutils python python-pip ffmpeg jq
yes | pkg install git                # pull in code and updates
yes | pkg install openssh            # install ssh client and server (sshd command)
yes | pkg install rsync              # enables `termux-open` command, used by `play` command
yes | pkg install mediainfo          # required for `specs`
yes | pkg install imagemagick        # convert images
yes | pkg install nano               # for editing code with nanodlv, nanofvid,...
yes | pkg install ncurses-utils      # for installing tput, used in fvid
yes | pkg install iproute2           # for fetching the current IP address
yes | pkg install moreutils          # better for fetching the current IP address
yes | pkg install python ffmpeg      # required for yt-dlp, ffprobe is included in ffmpeg
yes | pkg install jq                 # json processor
yes | pkg install tor proxychains-ng # tools for dealing with censored videos
yes | pkg install termux-services    # enables management of services, used in the Tor workflow
yes | pkg install libxml2 libxslt    # dependencies for facebook-scraper (installed by pip a little lower)
yes | pkg install deno               # install Deno to solve JavaScript challenges presented by YouTube with EJS


echo "Installing python packages..."  # python packages at /data/data/com.termux/files/usr/lib/python3.10/site-packages
pip install -U pip
pip install -U wheel
pip install -U yt-dlp
#pip install -U requests
#pip install -U image
#pip install -U pillow
#pip install -U selenium
#pip install -U beautifulsoup4
#pip install -U facebook-scraper
#pip install -U snscrape
#pip install -U pywebcopy

echo "Installing VidHop..."
vidhop_app_dir="$PREFIX/opt/vidhop" # $PREFIX points to /data/data/com.termux/files/usr
loader="$vidhop_app_dir/bin/loader" # loader in /opt
loader_bin="$PREFIX/bin/vidhop"     # loader in /bin

if [ -d "$vidhop_app_dir" ]; then
  echo -n "$vidhop_app_dir already existis, remove it? Y/n: " && read answer
  answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')
  [ "$answer" = "y" ] || [ -z "$answer" ] &&
    rm -rf "$vidhop_app_dir" && unset answer && sleep 3 &&
    git clone https://github.com/wtechgo/vidhop-android.git "$vidhop_app_dir"
else
  git clone https://github.com/wtechgo/vidhop-android.git "$vidhop_app_dir"
fi
chmod +x "$vidhop_app_dir/install.sh"
chmod +x "$loader"

# backup up current bash.bashrc
cp "$PREFIX/etc/bash.bashrc" "$PREFIX/etc/bash.bashrc.backup"

# Enabling the '. vidhop' command.
echo '#!/bin/bash' >"$loader_bin"
echo >>"$loader_bin"
echo ". $loader" >>"$loader_bin"
chmod +x "$loader_bin"
echo -e "\n. vidhop" >>"$PREFIX/etc/bash.bashrc"

echo "Configuring Termux for a streamlined VidHop experience..." && sleep 1
echo "Removing Termux welcome message as it interferes with rsync (VidHop Sync)..." && sleep 1
touch "$HOME/.hushlogin"

echo "Allowing Termux to open files in sd card (user storage space on Android) at $HOME/storage/shared..." && sleep 1
! [ -d "$HOME/.termux" ] && mkdir "$HOME/.termux"
echo 'allow-external-apps=true' >>"$HOME/.termux/termux.properties"

echo "Configuring nano as Termux default text editor..." && sleep 1
! [ -d "$HOME/bin" ] && mkdir "$HOME/bin"
! [ -f "$HOME/bin/termux-file-editor" ] && ln -s "$PREFIX/bin/nano" "$HOME/bin/termux-file-editor"

#echo -e "Info: '. vidhop' in bash.bashrc is the VidHop entry p"   #this line represents the width of Termux
echo -e "${BLUE}installation added '. vidhop' to bash.bashrc${NC}"
echo -e "Info: '. vidhop' in bash.bashrc is the VidHop"
echo -e "      entry point or loader."
echo -e "Info: Loading VidHop is extremely lightweight."
echo -e "Info: The app only defines functions and variables."
echo -e "      Work only happens when YOU"
echo -e "      run a VidHop command."
echo -e "Info: You can remove '. vidhop' from bash.bashrc"
echo -e "      and load VidHop manually with '. vidhop'"
echo -e "      or 'source vidhop'."
sleep 2

. "$loader"
echo -e "\n${GREEN}VidHop installed"'!'"${NC}\n" && sleep 1

vidhop_bashrc="$vidhop_app_dir/bash.bashrc"
bashrc=$PREFIX/etc/bash.bashrc
echo -e "'Install VidHop bash.bashrc' keeps Termux"
echo -e "default bash.bashrc and adds useful aliases."
echo -e "We recommend this on fresh installs"
echo -e "and for new Termux users." && unset answer
echo -n 'Install VidHop bash.bashrc? Yes/No/Show: ' && read answer
answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')
[ -z "$answer" ] || [ "$answer" = "y" ] || [ "$answer" = "yes" ] && unset answer &&
  cp "$vidhop_bashrc" "$bashrc"
[ "$answer" = "s" ] || [ "$answer" = "show" ] && unset answer &&
  echo "file: $vidhop_bashrc" && cat "$vidhop_bashrc" && unset answer &&
  echo -n 'Install VidHop bash.bashrc? Yes/No/Show: ' && read answer &&
  answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]') &&
  [ -z "$answer" ] || [ "$answer" = "y" ] || [ "$answer" = "yes" ] && unset answer &&
  cp "$vidhop_bashrc" "$bashrc"

echo
echo "You can try a VidHop command now e.g.:"
echo "  dlv https://www.youtube.com/watch?v=-DT7bX-B1Mg" && echo
echo "Alternatively, you can read the docs by executing:"
echo "  vidhophelp"
echo
echo -e "${GREEN}Happy downloading and building of your metadata library"'!'"${NC}\n" && sleep 1
echo -e "Requesting Termux access to sd card..."

yes | termux-setup-storage
