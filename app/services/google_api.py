from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
TITLE = 'Отчёт от {date}'
ROWCOUNT = 100
COLUMNCOUNT = 11
EMAIL = settings.email
SPREADSHEET_BODY = {
    'properties': {
        'title': TITLE.format(date=NOW_DATE_TIME),
        'locale': 'ru_RU'
    },
    'sheets': [{'properties': {
        'sheetType': 'GRID',
        'sheetId': 0,
        'title': 'Лист1',
        'gridProperties': {'rowCount': ROWCOUNT,
                           'columnCount': COLUMNCOUNT}
    }}]
}

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': EMAIL
}


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=None) -> str:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(SPREADSHEET_BODY)
        spreadsheet_body['properties']['title'] = TITLE.format(date=NOW_DATE_TIME)
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY['emailAddress'] = EMAIL
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    # Здесь формируется тело таблицы
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [str(project['name']),
                   str(project['close_date'] - project['create_date']),
                   str(project['description'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
