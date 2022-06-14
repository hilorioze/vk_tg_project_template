if __package__ is None:
    import sys
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.runner import run

if __name__ == "__main__":
    run()
