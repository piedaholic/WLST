while getopts 'srd:f:' c
do
  case $c in
    s) ACTION=SAVE ;;
    r) ACTION=RESTORE ;;
    d) DB_DUMP=$OPTARG ;;
    f) TARBALL=$OPTARG ;;
  esac
done
