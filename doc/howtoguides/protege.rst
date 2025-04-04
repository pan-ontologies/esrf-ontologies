Install Protégé
===============

Protégé is a tool used to create and modify ontologies.

Download the latest release

.. code:: bash

    repo="protegeproject/protege-distribution"
    release_info=$(curl -s "https://api.github.com/repos/$repo/releases/latest")
    download_url=$(echo "$release_info" | jq -r '.assets[] | select(.name | endswith ("linux.tar.gz")) | .browser_download_url')
    # -> https://github.com/protegeproject/protege-distribution/releases/download/protege-5.6.3/Protege-5.6.3-linux.tar.gz

    mkdir ./protege
    wget -qO- "$download_url" | tar xvz -C ./protege --strip-components=1

Create desktop file

.. code:: bash

    filename=~/.local/share/applications/protege.desktop
    echo "[Desktop Entry]" > $filename
    echo "Type=Application" >> $filename
    echo "Terminal=true" >> $filename
    echo "Name=Protégé" >> $filename
    echo "Icon=$(pwd)/protege/app/Protege.icns" >> $filename
    echo "Exec=$(pwd)/protege/run.sh" >> $filename
