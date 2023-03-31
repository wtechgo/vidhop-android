bin=$PREFIX/bin # $PREFIX is /data/data/com.termux/files/usr
etc=$PREFIX/etc
# User files.
bashrc=$etc/bash.bashrc
shared=$HOME/storage/shared # $HOME is /data/data/com.termux/files/home
dl=$shared/Download

# VidHop
. vidhop

alias cls='clear' # clear screen
# cd.
alias cdetc='cd $etc'
alias cdbin='cd $bin'
alias cddownloads='cd $dl'
alias cdshared='cd $shared'
alias cdmovies='cd $shared/Movies'
alias cdpictures='cd $shared/Pictures'
alias cdmusic='cd $shared/Music'
# ls.
alias ll='ls -lhtr'
alias la='ls -lAhtr'
alias lldownloads='ls -lAhtr $dl'
alias llmovies='ls -lAhtr $shared/Movies'
alias llpictures='ls -lAhtr $shared/Pictures'
alias llmusic='ls -lAhtr $shared/Music'

alias nanobashrc='nano $bashrc; source $bashrc'
alias reloadbashrc='source $bashrc'

which() {
  command -v "$1"
}

cd "$vidhop_dir" # $vidhop_dir was loaded during . vidhop

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
