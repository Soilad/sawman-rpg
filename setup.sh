if [ -d venv ]; then
	venv/bin/pip install -r requirements.txt;
	venv/bin/pip uninstall pygame pygame-ce;
	venv/bin/pip install pygame-ce;
else
	python -m venv venv
	venv/bin/pip install -r requirements.txt;
	venv/bin/pip uninstall pygame pygame-ce;
	venv/bin/pip install pygame-ce;
fi
