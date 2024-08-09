import os
import webbrowser
import toml
# TODO: Update README


def run_streamlit_app():
    #os.chdir('src/ui')
    #os.system('streamlit run dashboard.py')
    os.system('streamlit run src/ui/dashboard.py')


if __name__ == "__main__":
    run_streamlit_app()
