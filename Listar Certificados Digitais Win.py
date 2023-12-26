import csv
import subprocess
import os

# Definição do caminho do arquivo de saída
output_file = os.path.join(os.path.dirname(__file__), 'lista_certificados.txt')

# Comando PowerShell para listar certificados
powershell_script = '''
Get-ChildItem -Path Cert:\\CurrentUser\\My | 
    Select-Object Subject, FriendlyName, NotAfter | 
    ConvertTo-Csv -NoTypeInformation
'''

def get_certificates():
    # Executar o comando PowerShell e obter a saída
    process = subprocess.Popen(["powershell", "-Command", powershell_script], stdout=subprocess.PIPE, text=True)
    output, errors = process.communicate()

    # Converter a saída para uma lista de dicionários
    certificates = []
    reader = csv.DictReader(output.strip().split('\n'))
    for row in reader:
        certificates.append({
            'Nome do Certificado': row['Subject'],
            'Nome Amigável': row['FriendlyName'],
            'Data de Vencimento': row['NotAfter']
        })
    return certificates

def save_certificates(certificates):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Nome do Certificado', 'Nome Amigável', 'Data de Vencimento'], delimiter=',')
        writer.writeheader()
        for cert in certificates:
            writer.writerow(cert)

def main():
    certs = get_certificates()
    save_certificates(certs)
    print(f"Certificados salvos em {output_file}")

if __name__ == '__main__':
    main()
