bin=$PREFIX/bin
etc=$PREFIX/etc
bashrc=$etc/bash.bashrc
# ser files
shared=/data/data/com.termux/files/home/storage/shared
dl=$shared/Download

# load VidHop
. vidhop  # sources $PREFIX/bin/vidhop which

# cd & ls
alias ll='ls -lhtr'
alias la='ls -lAhtr'

alias cdetc='cd $etc'
alias cdbin='cd $bin'
alias cddownloads='cd $dl'
alias cdshared='cd $shared'

alias lldownloads='ls -lhtr $dl'
alias nanobashrc='nano $bashrc; source $bashrc'
alias killtor='kill $(pgrep tor)'

function python_packages_location() {
    echo "user packages" && python -m site --user-site
    echo
    echo "system packages" && python -m site
}

##############
### TERMUX ###
##############

# Command history tweaks:
# - Append history instead of overwriting
#   when shell exits.
# - When using history substitution, do not
#   exec command immediately.
# - Do not save to history commands starting
#   with space.
# - Do not save duplicated commands.
shopt -s histappend
shopt -s histverify
export HISTCONTROL=ignoreboth

# Default command line prompt.
PROMPT_DIRTRIM=2
PS1='\[\e[0;32m\]\w\[\e[0m\] \[\e[0;97m\]\$\[\e[0m\] '

# Handles nonexistent commands.
# If user has entered command which invokes non-available
# utility, command-not-found will give a package suggestions.
if [ -x $PREFIX/libexec/termux/command-not-found ]; then
  command_not_found_handle() {
    $PREFIX/libexec/termux/command-not-found
  }
fi
