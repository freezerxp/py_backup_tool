import boto3
import config


# Выгрузка файла в объктное хранилище яндекс.клауд
def upload_file(file_path):
    try:
        cfg = config.get_config()

        backup_folder = cfg['backupFolder']

        ya_cfg = cfg['yandexCloud']

        object_name = backup_folder.replace(backup_folder, ya_cfg['parentPath'])

        if not ya_cfg['enable']:
            return {'result':True,
                    'message':'Выгрузка в объектное хранилище отключена'}

        # Инициализация клиента S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=ya_cfg['accessKey'],
            aws_secret_access_key=ya_cfg['accessKey'],
            endpoint_url='https://storage.yandexcloud.net'
        )

        response = s3_client.upload_file(file_path, ya_cfg['bucketName'], object_name)
        print(f'Файл {object_name} успешно загружен.')

        return {'result': True,
                'message': f'Файл {file_path} загружен в {object_name}'}
    except Exception as e:
        return {'result': False,
                'message': f'Ошибка при загрузке файла: {e}'
                }
