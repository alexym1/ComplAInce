#!/bin/bash
ROOT_DIR=`git rev-parse --show-toplevel`
IMAGE_NAME="complaince_image"
CONTAINER_NAME="complaince_container"
VERSION=1.0.0
PORT=8000
GITHUB_REPOSITORY=alexym1/Complaince
OPENAI_API_KEY=`grep '^OPENAI_API_KEY=' .env | cut -d '=' -f2-`

while true; do
  case "$1" in
     -b|--build)
      docker build -t $IMAGE_NAME:$VERSION \
                  -f "$ROOT_DIR/docker/Dockerfile" \
                  --build-arg PKG_VERSION=$VERSION \
                  "$ROOT_DIR" || exit 1
      shift;;
     -r|--run)
      docker stop $CONTAINER_NAME &> /dev/null
      docker rm $CONTAINER_NAME &> /dev/null
      docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -dti --name $CONTAINER_NAME -p $PORT:8000 $IMAGE_NAME:$VERSION
      shift;;
     -p|--publish)
      echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
      docker tag $IMAGE_NAME:$VERSION ghcr.io/$GITHUB_REPOSITORY/$IMAGE_NAME:$VERSION
      docker push ghcr.io/$GITHUB_REPOSITORY/$IMAGE_NAME:$VERSION
      shift;;
    *)
      echo "End of Script"
      break;;
  esac
done
