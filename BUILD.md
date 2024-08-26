# Build doc

```bash
# Install requirement:
pip install antsibull-docs; sudo apt install acl

# install the collection locally
ansible-galaxy collection install ./stormshield-sns-XXX.tar.gz

# lint the doc
antsibull-docs lint-collection-docs --plugin-docs /home/user/.ansible/collections/ansible_collections/stormshield/sns

# generate html
mkdir build-docs
chmod 700 build-docs
# copy the modified conf.py
cp ~/sources/conf.py build-docs
antsibull-docs sphinx-init --use-current --squash-hierarchy --dest-dir build-docs stormshield.sns
cd build-docs
pip install -r requirements.txt
./build.sh
```

And then copy back the build/html files to the docs folder.