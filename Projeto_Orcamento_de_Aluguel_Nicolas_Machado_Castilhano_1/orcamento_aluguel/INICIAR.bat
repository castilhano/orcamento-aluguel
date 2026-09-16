@echo off
title Orcamento de Aluguel - Imobiliaria R.M.
cd /d "%~dp0"

echo.
echo  ============================================
echo   ORCAMENTO DE ALUGUEL - IMOBILIARIA R.M.
echo  ============================================
echo.

set PY=
where py >nul 2>&1 && set PY=py
if not defined PY where python >nul 2>&1 && set PY=python

if not defined PY (
  echo  [X] O Python nao foi encontrado neste computador.
  echo.
  echo  Vou abrir a pagina de download para voce.
  echo  IMPORTANTE: marque a caixa "Add python.exe to PATH".
  echo.
  pause
  start "" https://www.python.org/downloads/
  exit /b
)

echo  [1/3] Python encontrado.
echo.
echo  [2/3] Preparando as bibliotecas, aguarde...
%PY% -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
  echo.
  echo  [X] Nao consegui instalar as bibliotecas.
  echo  Verifique sua conexao com a internet e tente de novo.
  echo.
  pause
  exit /b
)
echo       Tudo pronto.
echo.
echo  [3/3] Abrindo no navegador...
echo.
echo  ============================================
echo   Endereco: http://localhost:5000
echo  ============================================
echo.
echo  NAO FECHE ESTA JANELA enquanto estiver usando.
echo  Para encerrar, aperte Ctrl + C aqui.
echo.

start "" http://localhost:5000
%PY% app.py

echo.
echo  O sistema foi encerrado.
pause
