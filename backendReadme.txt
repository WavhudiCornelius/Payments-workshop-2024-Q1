To start this bad boy up

1. pip install virtualenv

2. python3 -m venv venv

3. source venv/bin/activate ( not always required, putting it here anyway)

4. pip install -r backendRequirements.txt

Everytime you add a new dependency please:

1. Make sure you installed all the requirements as mentioned in step 4 above

2. Then: pip freeze > backendRequirements.txt
