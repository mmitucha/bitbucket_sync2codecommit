#!/usr/bin/env bash
set -xe

# Check if repos dir specified
if [ -z "$REPOS_DIR" ]
then
    BASEDIR=$(dirname "$0")
    REPOS_DIR="$BASEDIR/_repos"
fi

### Check $REPOS_DIR , if not found create it
[ ! -d "$REPOS_DIR" ] && mkdir -p -m 750 "$REPOS_DIR"


REPO_FULLNAME=$1
if [ -z "$1" ]
  then
    echo "No repository_fullname provided (<user>/<repository_name>) !"
    exit 2
fi

REPO_NAME=$(basename $REPO_FULLNAME)

echo "=== Starting repo $REPO_FULLNAME sync ==="
VERBOSE=''
#VERBOSE='-v'

SOURCE_REPO="git@bitbucket.org:$REPO_FULLNAME.git"
DEST_REPO="https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/$REPO_NAME"

# Disable host key checking
git config  --global core.sshCommand 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
# Setup AWS CodeCommit credentials helper (use AWS IAM role permissions)
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true

REPO_PATH="$REPOS_DIR/$REPO_NAME"
echo $REPO_PATH

# Clone or fetch from source repository
if [ -d "$REPO_PATH" ] ; then
    cd "$REPO_PATH"
    git fetch $VERBOSE
else
    git clone $VERBOSE --mirror "$SOURCE_REPO" "$REPO_PATH"
    cd "$REPO_PATH"
fi

# # Push to destination repository
git config remote.sync.url >&- || git remote add sync "$DEST_REPO"
git push sync --mirror
echo "=== End of repo $REPO_FULLNAME sync ==="
