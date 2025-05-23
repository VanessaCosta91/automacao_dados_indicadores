import subprocess
import sys
import os


def ativar_venv():
    """Ativa o ambiente virtual (.venv)"""
    if os.name == 'nt':  # Windows
        activate_script = '.venv\\Scripts\\activate.bat'
    else:  # Linux ou Mac
        activate_script = '.venv/bin/activate'

    return activate_script


def instalar_dependencias():
    """Instala as dependências do requirements.txt"""
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def executar_pipeline():
    """Executa a pipeline principal"""
    print("Executando pipeline...")
    subprocess.check_call([sys.executable, "pipeline.py"])


if __name__ == "__main__":
    ativar_venv()
    instalar_dependencias()
    executar_pipeline()
    print("Pipeline concluída com sucesso!")
