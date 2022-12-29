#!/bin/bash

export TERMINATOR_SESSION=${1:-$TERMINATOR_SESSION}

if [ -z "$TERMINATOR_SESSION" ]; then
    echo "Give a session name" >&2
else

LAST_CMD=$(history | tail -2 | cut -d" " -f4- | head -1)

mkdir -p ~/.config/terminals/$TERMINATOR_SESSION/

TERMINATOR_ID=${TERMINATOR_ID:-$$}

cat <<EOF > ~/.config/terminals/$TERMINATOR_SESSION/$TERMINATOR_ID
export TERMINATOR_CMD='$LAST_CMD'
export TERMINATOR_PWD='$PWD'
export TERMINATOR_ID='$TERMINATOR_ID'
echo ">> Restore session [$TERMINATOR_SESSION] - terminal [$TERMINATOR_ID]"
cd $PWD
echo $$TERMINATOR_CMD
history -s $$TERMINATOR_CMD
$$TERMINATOR_CMD
EOF

n=$(ls -1 ~/.config/terminals/$TERMINATOR_SESSION/ 2>/dev/null | grep -v '^\.' | wc -l)

echo "Saved  session [$TERMINATOR_SESSION], terminal [$TERMINATOR_ID]"
echo "  CMD: $LAST_CMD"
echo "  PWD: $PWD"
echo "(session has now $n terminals)"

fi