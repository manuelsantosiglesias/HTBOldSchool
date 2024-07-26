import struct
import base64

def create_kirbi_file(output_path, ticket_data_base64, key_base64, principal_name, realm):
    # Decodifica los datos Base64 a bytes
    ticket_data = base64.b64decode(ticket_data_base64)
    key_data = base64.b64decode(key_base64)

    # El formato del archivo `.kirbi` puede variar dependiendo de la implementación,
    # pero para fines de demostración, asumiremos un formato básico.

    # Define el encabezado del archivo y los datos
    file_format_version = 1284  # Version del formato
    header_length = 12          # Longitud del encabezado

    # Crear el archivo `.kirbi`
    with open(output_path, 'wb') as f:
        # Escribir versión del formato
        f.write(struct.pack('!I', file_format_version))
        # Escribir longitud del encabezado
        f.write(struct.pack('!I', header_length))
        # Escribir datos del ticket
        f.write(ticket_data)
        # Escribir datos de la clave
        f.write(key_data)
        # Escribir principal y realm (simplificado para la demostración)
        f.write(principal_name.encode('utf-8'))
        f.write(realm.encode('utf-8'))

    print(f"Archivo {output_path} creado con éxito.")

# Datos del ticket (proporcionados en la pregunta)
ticket_data_base64 = "YYIFuzCCBbegAwIBBaEQGw5GUkVFTEFOQ0VSLkhUQqIkMCKgAwIBAqEbMBkbBGNpZnMbEURDLmZyZWVsYW5jZXIuaHRio4IFdjCCBXKgAwIBEqEDAgELooIFZASCBWCizixp2D1k3DKbosEtA8L23e8WiAEyyt9kk2+PZymON40gIisCM9mpZFZkJ7cnPhPTNAaD1HfvwwUfA2t1u0VsC9eFppjOvSaQtJe0/r4/n/FNSGSH0OcE+dYDtT+KWgG+HuI+D8zjeOFNIqkG4AF1iifrvzR9e/Q74m38QOGRVrTlsZn1nfKTPn6dmDWkyctcNr3MiKL7+cfU4lgA7fXDcj6+jGhZPNp84EUTZmO8E1/Ez/okhONYAbKOImj2+PImEhhul8Udx2Bq77+C03NarRrtHOCgFkkdgPJ0fw7+CQHNTT2c3kpKmf3WcBvAmhv7oVN+uKTPTmHjapiZ7ZSzmVoFqCrTsev8LNp305nYUg/ynznv+fqksyJAqrV7wWiDdFljN0WcLg+1/KRYZUVD7IK6KTrnzvYjA1TkyJC1VoB7oEvv83SRtpugPoqneFg0QHNp4kStLjPscSRww0o58NprtXQLVd8KNnW6j3gZ79uHS1RbuyBTR1S+FK6BCYz2fyuOuJgOfgIEfvxk6AioT2T0QEfqmif2pDHiXFeNzsZ0vIt2agTqed2bdARxqcSQMA9OgM5qxk3nTzUno522E0+b8sP9+ouLp5GeMggsn+gHHwuBVD+um4ZuEnmMTjOiutHqKJVaZt8XR89uVBB/SZLBc5N2vyuFbmwVILE2R/KW78b8HGfjtx1iMudw3ATmrz0v8L3u0rRO5LbcRztFyzUuVEMwCdgsjX+dXcbFxajEc73db1LyoCcDlIQ2L1oBeAg8cp83I7Q7YzO2i+/1CN0nt7FRujcXsyaUfR8a0//CrwR4eX05hwjk0mZ2MQ6QcjsSaKrKhGxvoi/EMZdg5brQIiGiMDlcwqrDEamve7641X/pp/N70C9le5V7KVovK8SC14WJZrj7SyxhR4cDyO0TUxT28MsExyIq3AiCyHq9DGoJkzkBGKmhuJcRW5AWDXhnlU7zUhhhfAjCyNzJGNmgYKJTVaq3Y+z33I06YTgA+GRZ8AtFRovcLw2Ey68y2X1p6gJqV6GK1vvvKPApX5l8+02/47+Df7Z+Y84XD3xwn3x+LbPTyr2RB1HXIvwdrso8+n8aox8cesvIhitCgjcoiidrwPTwiqLHkwGe84mVTeRcbY120jyp8bZxeRDm7SCTUkzangAw5ttMFtwW1U+1H2CNDO0e41BQ4yUNLMciwYMt9PzDbL1RBZA8TWnCrB9B6HRQGeoxjpPBw8UjLHJO2xU9bHczFytOAZSlVj6Eg3xbI12rYwpzPzNJpb7Jr1aIkIfZ1SsUihxXrFZknY6pQS99wiYd9Xn1M509dVVqzzZ9E1DUzP6erVtH02fuUapsNvDodT+UuElo8onzPXbBaaQrsEqtmx5FWgE1BD06MMW9FYdmDesiV09TVJOxR48bParzq3JyNoBF4DSw/xCGX7JzxTE8pmh7f5wijWbKklkxWAUyk45K1eV4QyBofXSWRsKLdHJzA1K1ftYyzWQlsBrcwmEhSaroCUMN7EOuF4N+i/ZNTNfMLOzEvUIkXeIyf4lLXzTRr1pmVoy6+q/u/RSWRjjzaqYIVOZjUFgQljDuGcX/xiHUyMSCwuD6eMaEhxWI/Tp2hFFpT6c101qpNxlFpM0rX4ba0azkVzLF+3tlcO6422ZKU6g/na8+47+VXCqF1guCOPRuN8aWCbfOWH72WzTwaOSSliItyLJnDOGD4NTM3PpNO9RZbiXNHcP2FiBCL9OzHEcLkfeYKAH1RZg76JvOlC3uCrocIL7wI/BKTeiEmabL51IxYDK7DZg5YCTaq0cEYC5EQ5J9bwGNF2kCESXjNxMS8kvvMA=="

# Datos de la clave (esto debe ser proporcionado; aquí se ha dejado vacío por defecto)
key_base64 = "B1UgE1TJKxokqe2gGjfhrw=="

principal_name = "Administrator"
realm = "freelancer.htb"

create_kirbi_file('ticket.kirbi', ticket_data_base64, key_base64, principal_name, realm)
