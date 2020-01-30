frctest:
    @(source venv/bin/activate && python robot.py test)
    
deploy:
    (source venv/bin/activate && python robot.py deploy)

update:
    (source venv/bin/activate && pip install --user --upgrade -r requirements.txt)
