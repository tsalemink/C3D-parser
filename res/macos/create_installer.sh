#!/bin/sh
version=$1

app_name=C3D-Parser
app_name_with_version=C3D-Parser-$version
dmg_name=$app_name_with_version.dmg
test -f $dmg_name && rm $dmg_name
create-dmg \
  --volname "$app_name_with_version" \
  --volicon "ABI.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "$app_name.app" 200 190 \
  --hide-extension "$app_name.app" \
  --app-drop-link 600 185 \
  "$dmg_name" \
  "../pyinstaller/dist/"
