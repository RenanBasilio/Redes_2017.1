# Trabalho de Redes I - EEL878
Este repositório contém o trabalho consistindo de cliente e servidor de sala de bate papo implementados para a disciplina Redes de Computadores 1 da UFRJ no período de 2017/1 ministrada pelo professor Diogo Menezes.
<br>
<br>
Grupo: Renan Basilio, Luis Eduardo Pessoa, Caio Alves
<br>
<br>
<br>
Relatório: [Link do Relatório no Google Drive](https://docs.google.com/document/d/1E5kbypW2U2MEW2rIclzTPN6D4J2eHRoYZ6nP7quBMVY/edit?usp=sharing)

Apresentação: [Link da Apresentação no Google Drive](https://docs.google.com/presentation/d/10r1hcKxzYVjSaIdQgyaVE6xeA6spCOvcp8m8-z91EZc/edit?usp=sharing)

----------


## Instruções para Emissão e Instalação de Certificado SSL no Windows

### Emissão de Certificado no Windows 10 (Pós Anniversary Update)

1. Habilitar função *Bash on Ubuntu on Windows*. [Link com instruções de como fazer.](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) 

2. Na shell de bash, navegar até o diretório de saída desejado (de preferência o mesmo diretório onde se encontra o servidor).
3. Executar o comando a seguir e preencher os dados necessários. O "COMMON NAME" deve ser o endereço que o certificado representa (por exemplo, para localhost, 127.0.0.1).

    `openssl req -new -x509 -days 365 -nodes -out cert_chatRedes.pem -keyout key_chatRedes.pem`

4. Executar o comando a seguir para verificar se o certificado foi gerado corretamente.

    `openssl x509 -text -noout -in cert_chatRedes.pem`
<br><br>

### Emissão de Certificado em Outras Versões do Windows

1. Baixar versão apropriada do [OpenSSL para Windows](https://slproweb.com/products/Win32OpenSSL.html).

2. Do diretório de instalação, copiar arquivo `bin\cnf\openssl.cnf` para `C:\Program Files\Common Files\SSL`.

3. Abrir Prompt de Comando na pasta `bin` do diretório de instalação.

4. Executar o comando a seguir e preencher os dados necessários. O "COMMON NAME" deve ser o endereço que o certificado representa (por exemplo, para localhost, 127.0.0.1).

    `openssl req -new -x509 -days 365 -nodes -out cert_chatRedes.pem -keyout key_chatRedes.pem`

5. Executar o comando a seguir para verificar se o certificado foi gerado corretamente.

    `openssl x509 -text -noout -in cert_chatRedes.pem`

6. Os arquivos criados estarão no diretório de instalação. Mover ambos para a pasta onde se encontra o servidor.
<br><br>

### Instalação de Certificado

1. Executar `certmgr.msc` e navegar até Trusted Root Certification.

2. Clicando com o botão direito, selecionar `Todas as Tarefas > Importar...`

3. Seguir as intruções na tela para importar o certificado criado como entidade certificadora local.



