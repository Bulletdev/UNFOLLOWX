# TWITTER UNFOLLOW TOOL (NO MUTUALS)

Descrição

Twitter Unfollow Tool (No Mutuals) é uma ferramenta simples que utiliza a API do Twitter para automatizar o processo de deixar de seguir usuários que não seguem você de volta. É ideal para manter uma lista de seguidores limpa e gerenciar melhor suas conexões no Twitter.

## Instalação

Clone o repositório:

````bash
git clone https://github.com/bulletdev/UNFOLLOWX.git
cd UNFOLLOWX
`````

Instale as dependências: Certifique-se de ter o pip instalado. Em seguida, execute:

````bash
pip install tweepy
````
Configure suas credenciais do Twitter:

Obtenha suas credenciais de desenvolvedor do Twitter (API Key, API Secret, Access Token, Access Secret).
https://developer.x.com/ 

Substitua as credenciais no arquivo do script:

````python
API_KEY = 'sua_api_key'
API_SECRET = 'seu_api_secret'
ACCESS_TOKEN = 'seu_access_token'
ACCESS_SECRET = 'seu_access_secret'
````

## Uso
Execute o script:

````bash
python UNFOLLOWX.py
````

Limite por minuto:

O script possui um limite de ações por minuto para evitar bloqueios pela API do Twitter. O valor padrão é 10, mas você pode ajustá-lo conforme necessário:

````python
unfollow_nonfollowers(limit_per_minute=10)
````

## Funções Principais
Autenticação na API do Twitter:

Utiliza o tweepy.OAuthHandler para autenticar e acessar a API do Twitter.

Identificação de não-seguidores:

Compara as listas de seguidores e seguidos para identificar usuários que não seguem você de volta.

Desseguir usuários:

Automatiza o processo de deixar de seguir usuários que não seguem você de volta, respeitando o limite de ações por minuto.

Erros e Soluções
Tweepy.TweepError:

O script possui tratamento de exceções para capturar e exibir erros relacionados à API do Twitter.

Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença
Este projeto é licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
