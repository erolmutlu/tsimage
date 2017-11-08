#!/bin/sh
#DESCRIPTION=This script will delete all crash-logs from /media/hdd
echo "Removing enigma2 crashlogs..."
rm -f "/media/hdd/test*"
#rm -rf /media/hdd/enigma2_crash*
echo "done."
exit 0;
