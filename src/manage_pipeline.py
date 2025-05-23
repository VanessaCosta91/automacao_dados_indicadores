import subprocess
import sys
import os


def ativar_venv():
    """Ativa o ambiente virtual (.venv)."""
    if os.name == 'nt':  # Windows
        activate_script = '.venv\\Scripts\\activate.bat'
    else:  # Linux/Mac
        activate_script = '.venv/bin/activate'
    return activate_script


def instalar_dependencias():
    """Instala as dependências."""
    print("Instalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def executar_pipeline():
    """Executa o pipeline principal."""
    print("Executando pipeline...")
    subprocess.run([sys.executable, "pipeline.py"])


def main():
    print("Ativando ambiente virtual...")
    ativar = ativar_venv()
    print(f"Execute manualmente se der erro: {ativar}")

    instalar_dependencias()
    executar_pipeline()
    print("Pipeline finalizada com sucesso!")


if __name__ == "__main__":
    main()
