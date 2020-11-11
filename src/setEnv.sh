#Oracle Middleware 12c
export SEARCH_ROOT=`pwd`
echo "Searching $1 with ${SEARCH_ROOT} directory as root"
export SEARCH_RESULTS="$(find ${SEARCH_ROOT} -type d -iname "${1}*")"
#echo "Search Completed"
export OS_SEPARATOR="/"
export NUM_DOMAINS_FOUND=0
#export MULTIPLE_DOMAIN_HOMES_FOUND=false

for DIRECTORY in $SEARCH_RESULTS
do
   #echo "Checking ${DIRECTORY}"
   export IFS=$OS_SEPARATOR
   read -ra DIRECTORY_TREE<<<$DIRECTORY
   TREE_LENGTH=${#DIRECTORY_TREE[@]}
   #echo "Tree length is ${TREE_LENGTH}"
   #echo "${DIRECTORY_TREE[${TREE_LENGTH}-2]}"
   #echo "${DIRECTORY_TREE[${TREE_LENGTH}-3]}"
   #echo "${DIRECTORY}/../../../wlserver/server"
   if [ "${DIRECTORY_TREE[${TREE_LENGTH}-2]}" == "domains" ] && [ "${DIRECTORY_TREE[${TREE_LENGTH}-3]}" == "user_projects" ]  && [ -d "${DIRECTORY}/../../../wlserver/server" ];then
     #echo "Setting Oracle Middleware Environment Variables"
     export MW_HOME=`readlink -f "${DIRECTORY}/../../../"`
     export WL_HOME="${MW_HOME}/wlserver"
     export WLS_HOME="${MW_HOME}/wlserver/server"
     export DOMAIN_HOME="${DIRECTORY}"
     ((NUM_DOMAINS_FOUND++))
   fi
done

if [ ${NUM_DOMAINS_FOUND} -gt 1 ];then
  echo "Multiple matching domains found"
  export MW_HOME=
  export WL_HOME=
  export WLS_HOME=
  export DOMAIN_HOME=
elif [ ${NUM_DOMAINS_FOUND} -eq 0 ];then
  echo 'No matching domains found'
else
  echo "Oracle Middleware Environment Variables Set Successfully"
fi

echo "MW_HOME=${MW_HOME}"
echo "WL_HOME=${WL_HOME}"
echo "WLS_HOME=${WLS_HOME}"
echo "DOMAIN_HOME=${DOMAIN_HOME}"

export SEARCH_ROOT=
export SEARCH_RESULTS=
export OS_SEPARATOR=
export NUM_DOMAINS_FOUND=
export DIRECTORY=
export TREE_LENGTH=
export DIRECTORY_TREE=
unset IFS
