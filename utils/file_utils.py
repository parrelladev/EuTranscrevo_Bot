"""
📁 UTILITÁRIOS PARA OPERAÇÕES COM ARQUIVOS

Funções auxiliares para:
- Geração de nomes únicos
- Limpeza de arquivos temporários
- Validação de arquivos
- Verificação de permissões
- Criação de diretórios

Autor: parrelladev
Versão: 1.0.0
"""

import os
import time
import glob
import shutil
from config import AUDIO


def generate_unique_file_name(prefix=None, extension=''):
    """
    Gera um nome único para um arquivo.

    :param prefix: Prefixo do nome (opcional, usa config se None)
    :param extension: Extensão com ponto (ex: .mp3)
    :return: Nome do arquivo único
    """
    default_prefix = prefix or AUDIO['tempPrefix']
    timestamp = int(time.time() * 1000)
    return f"{default_prefix}_{timestamp}{extension}"


def clean_temp_files(directory=None, pattern='*'):
    """
    Limpa arquivos temporários de um diretório.

    :param directory: Caminho do diretório (usa config se None)
    :param pattern: Padrão de arquivos (ex: *.mp3)
    :return: Quantidade de arquivos deletados
    """
    target_dir = directory or os.path.join(os.getcwd(), AUDIO['tempDir'])
    deleted_count = 0

    if not os.path.exists(target_dir):
        return 0

    try:
        files = glob.glob(os.path.join(target_dir, pattern))
        for file_path in files:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1
                print(f"🗑️ Arquivo deletado: {file_path}")
        return deleted_count
    except Exception as e:
        print("❌ Erro ao limpar arquivos temporários:", e)
        return 0


def file_exists(file_path):
    """
    Verifica se o arquivo existe e é legível.

    :param file_path: Caminho completo
    :return: True se o arquivo existe e é acessível
    """
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def get_file_size(file_path):
    """
    Retorna o tamanho de um arquivo.

    :param file_path: Caminho do arquivo
    :return: Tamanho em bytes
    :raises FileNotFoundError: se não existir
    """
    if not file_exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return os.path.getsize(file_path)


def ensure_directory_exists(dir_path):
    """
    Cria o diretório, se não existir.

    :param dir_path: Caminho do diretório
    :return: True se criado ou já existente
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Diretório criado/confirmado: {dir_path}")
        return True
    except Exception as e:
        print("❌ Erro ao criar diretório:", e)
        return False
