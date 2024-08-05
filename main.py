import os
import webbrowser
import toml




def run_streamlit_app():
    os.chdir('src/ui')
    config = toml.load('.streamlit/config.toml')
    port = config.get('port', 8501)
    webbrowser.open(f'http://localhost:{port}')
    os.system('streamlit run dashboard.py')



if __name__ == "__main__":
    run_streamlit_app()

