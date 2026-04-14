PYTHON := /home/megardes/2048/.venv/bin/python
CPP_SRC := src/cpp/main.cpp
CPP_BIN := bin/2048_cpp
PYTHONPATH := src/python

.PHONY: help build run autoplay train eval test clean

help:
	@echo "Targets:"
	@echo "  make build      - Build the C++ 2048 binary"
	@echo "  make run        - Run the C++ 2048 game"
	@echo "  make autoplay   - Run Python controller against C++ binary"
	@echo "  make train      - Run training stub"
	@echo "  make eval       - Run evaluation stub"
	@echo "  make test       - Run unit tests"
	@echo "  make clean      - Remove build artifacts"

build:
	@mkdir -p bin
	g++ -std=c++17 -O2 -Wall -Wextra -pedantic $(CPP_SRC) -o $(CPP_BIN)

run: build
	./$(CPP_BIN)

autoplay: build
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/autoplay.py --binary ./$(CPP_BIN) --max-steps 500

train:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/train.py --config configs/train.yaml

eval: build
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/eval.py --binary ./$(CPP_BIN) --episodes 50

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -p 'test_*.py'

clean:
	rm -rf bin
