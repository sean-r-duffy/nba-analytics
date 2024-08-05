import os
import webbrowser


def run_streamlit_app():
    os.chdir('src/ui')
    os.system('streamlit run dashboard.py')


if __name__ == "__main__":
    webbrowser.open('http://localhost:8501')
    run_streamlit_app()

