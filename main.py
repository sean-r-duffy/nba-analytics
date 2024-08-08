import os
import webbrowser
import toml


def run_streamlit_app():
    os.chdir('src/ui')
    os.system('streamlit run dashboard.py')


if __name__ == "__main__":
    run_streamlit_app()
