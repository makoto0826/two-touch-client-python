#!/bin/bash

function install() {
   sudo apt update
   sudo apt upgrade -y
   sudo apt install libsdl2-dev \
      libsdl2-image-dev \
      libsdl2-mixer-dev \
      libsdl2-ttf-dev \
      pkg-config \
      libgl1-mesa-dev \
      libgles2-mesa-dev \
      python-setuptools \
      libgstreamer1.0-dev \
      git-core \
      gstreamer1.0-plugins-{bad,base,good,ugly} \
      gstreamer1.0-{omx,alsa} \
      python-dev \
      libmtdev-dev \
      xclip \
      xsel \
      libjpeg-dev -y

   sudo python3 -m pip install --upgrade pip setuptools
   sudo python3 -m pip install --upgrade Cython==0.29.10 pillow
   sudo python3 -m pip install kivy tzlocal japanize_kivy nfcpy

   sudo apt autoremove -y
   sudo apt clean -y
}

function set_rc_s380(){
   sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"054c\", ATTRS{idProduct}==\"06c3\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
   sudo udevadm control -R
}

function set_api_json() {
   readonly API_PATH="./data"
   readonly API_FILE_PATH="${API_PATH}/api.json"

   if [ ! -d $API_PATH ]; then
      mkdir $API_PATH
   fi

   if [ -f $API_FILE_PATH ]; then
      rm -f $API_FILE_PATH
   fi

   cat <<EOL >> $API_FILE_PATH
{
 "api_key"             : "${1}",
 "get_information_url" : "https://${2}-${3}.cloudfunctions.net/getInformation",
 "get_users_url"       : "https://${2}-${3}.cloudfunctions.net/getUsers",
 "add_time_record_url" : "https://${2}-${3}.cloudfunctions.net/addTimeRecord"
}

EOL

}

function set_auto_start() {
   readonly SERVICE_FILE_PATH="/etc/systemd/system/two-touch.service"
   readonly TEMP_FILE="./.two-touch.service"

   if [ -f $SERVICE_FILE_PATH ]; then
      sudo systemctl disable two-touch
      sudo rm -f $SERVICE_FILE_PATH
   fi

   cat <<EOL >> $TEMP_FILE
[Unit]
Description=two-touch
After=network-online.target

[Service]
User=pi
Environment=DISPLAY=:0
WorkingDirectory=${1}
ExecStart=/usr/bin/python3 -m main
Restart=always

[Install]
WantedBy=graphical.target

EOL

   sudo mv $TEMP_FILE $SERVICE_FILE_PATH
   rm -f $TEMP_FILE

   sudo systemctl enable two-touch
}


function help() {
   cat <<EOL
Usage: api
 Web APIのjsonを作成します。

 引数1 API KEY
 引数2 Firebase リージョン
 引数3 Firebase プロジェクトID   

Usage: auto-start
 自動起動の設定をします。

Usage: install
 動作に必要なソフトウェアをインストールと
 SONY RC-S380の設定をします。
EOL

   exit 0
}

case $1 in
   "api" )
      if [ $# -ne 4 ]; then
         echo "引数に誤りがあります"
         exit 99
      fi

      set_api_json $2 $3 $4
      ;;

   "auto-start" )
      path=$(pwd)
      set_auto_start $path
      ;;

   "install" )
      install
      set_rc_s380
      ;;   

   *)
      help
      ;;
esac