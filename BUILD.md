# Build doc

Install requirement: `pip install antsibull-docs; sudo apt install acl`

```bash
# install locally
ansible-galaxy collection install ./stormshield-sns-1.0.0.tar.gz

# lint the doc
antsibull-docs lint-collection-docs --plugin-docs /home/user/.ansible/collections/ansible_collections/stormshield/sns

# generate html
mkdir build-docs
chmod 700 build-docs
# --squash-hierarchy
antsibull-docs sphinx-init --use-current --dest-dir build-docs stormshield.sns
# copy the modified conf.py
cp ~/sources/conf.py build-docs

cd build-docs
pip install -r requirements.txt
./build.sh
```
