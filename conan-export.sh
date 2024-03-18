#!/usr/bin/env bash
cd conan-recipe/amf/all
conan export .  --name amf --version v1.4.30 --channel stable --user self-muradyan
cd ../../ffmpeg/all
conan export .  --name ffmpeg --version 5.1 --channel stable --user self-muradyan
cd ../../ffnvcodec/all
conan export .  --name ffnvcodec --version 12.0.16.0 --channel stable --user self-muradyan
cd ../../media-driver/all
conan export .  --name media-driver --version 22.3.1 --channel stable --user self-muradyan
cd ../../libva/all
conan export .  --name libva --version 2.14 --channel stable --user self-muradyan
cd ../../igdgmm/all
conan export .  --name igdgmm --version 22.1.2 --channel stable --user self-muradyan
