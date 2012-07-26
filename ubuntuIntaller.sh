# run this file with sudo sh ubuntuIntegration.sh

# auto-integration (launchers, menus, etc.) under ubuntu with python 2.7
# still some issue with mim-type integration (so .pyslices and .sympyslices files associate and get little icons)

# install wx_py with setuptools; it's fine if this has been run already
sudo python setup.py install

# Make sure the script files are executable
chmod +x ./wx_py/PyCrust.py
chmod +x ./wx_py/PyShell.py
chmod +x ./wx_py/SymPySlices.py
chmod +x ./wx_py/PySlices.py
chmod +x ./wx_py/PySlicesShell.py
chmod +x ./wx_py/SymPySlices.py

# Make any OS directories that don't already exist
sudo mkdir /usr/local
sudo mkdir /usr/local/share
sudo mkdir /usr/local/share/pixmaps
sudo mkdir /usr/local/share/applications
sudo mkdir /usr/local/share/icons
sudo mkdir /usr/local/share/icons/gnome
sudo mkdir /usr/local/share/icons/gnome/scalable
sudo mkdir /usr/local/share/icons/gnome/scalable/mimetypes
sudo mkdir /usr/local/share/mime
sudo mkdir /usr/local/share/mime/packages


# Link executables
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/PyCrust.py /usr/local/bin/pycrust
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/PyCrust.py /usr/local/bin/pyshell
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/PySlices.py /usr/local/bin/pyslices
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/PySlices.py /usr/local/bin/pysliceshell
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/SymPySlices.py /usr/local/bin/sympyslices

# Link icons
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/icons/PyCrust.svg /usr/local/share/pixmaps/PyCrust.svg
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/icons/PySlices.svg /usr/local/share/pixmaps/PySlices.svg
sudo ln -s /usr/local/lib/python2.7/dist-packages/wx_py/icons/SymPySlices.svg /usr/local/share/pixmaps/SymPySlices.svg

# Link the .desktop launchers
sudo cp ./desktop/* > /usr/local/share/applications/

### MIME type integration ###

# Copy the icons
sudo cp /usr/local/lib/python2.7/dist-packages/wx_py/icons/PySlices.svg /usr/local/share/icons/gnome/scalable/mimetypes/application-pyslices.svg
sudo cp /usr/local/lib/python2.7/dist-packages/wx_py/icons/SymPySlices.svg /usr/local/share/icons/gnome/scalable/mimetypes/application-sympyslices.svg

# Copy the .xml MIME data
sudo cp ./mime/* /usr/local/share/mime/packages/

# Try to associate the applications with xgd-mime
xdg-mime default /usr/local/share/applications/PySlices.desktop application/pyslices
xdg-mime default /usr/local/share/applications/SymPySlices.desktop application/sympyslices

# Update the MIME database
sudo update-mime-database /usr/local/share/mime

# Sadly, you still need to manually associate the files in nautilus
# I'm still working on this
