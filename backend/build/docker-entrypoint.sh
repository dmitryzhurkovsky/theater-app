#!/bin/bash

set -euo pipefail

ACTION=""
if [ $# -ge 1 ]; then
  ACTION=${1} ; shift
fi

case "${ACTION}" in

  ''|-*)
    exec uvicorn ${UVICORN_APP} ${ACTION} ${@}
    ;;

  uvicorn)
    exec uvicorn ${UVICORN_APP} ${@}
    ;;

  migration)
    exec alembic -c migrations/alembic.ini upgrade head
    ;;

  pytest)
    exec pytest ${@}
    ;;

  *)
    exec ${ACTION} ${@}
    ;;

esac
