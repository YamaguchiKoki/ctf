#!/bin/bash
set -eu

sed 's/^Alpaca//' flag.txt | base64 -w0 | tr -d '=' > flag.b64.txt

IMAGE_NAME=output-image
docker image build -t "$IMAGE_NAME" .
docker image save "$IMAGE_NAME" > "$IMAGE_NAME.tar"
docker image rm "$IMAGE_NAME"

rm flag.b64.txt
mv "$IMAGE_NAME.tar" ..
