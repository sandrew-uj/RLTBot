from datetime import datetime, timedelta

from pymongo import MongoClient

from dateutil.relativedelta import relativedelta


def aggregate_values(dt_from_iso, dt_upto_iso, group_type):
    # Подключение к MongoDB
    client = MongoClient('localhost', 27017)

    # Выбор базы данных
    db = client['sampleDB']

    # Выбор коллекции
    collection = db['sample_collection']

    # Преобразование дат из ISO формата
    dt_from = datetime.fromisoformat(dt_from_iso)
    dt_upto = datetime.fromisoformat(dt_upto_iso)

    # Определение параметров агрегации
    group_field = "$dt"  # Подставьте поле с датой и временем в вашей коллекции
    group_format = f"%Y-%m-%dT%H:{dt_from_iso[-5:]}"  # Формат группировки, также проставляем из первой даты минуты и секунды, которых не будет в группировке
    dt_step = timedelta(hours=1)
    if group_type == "day":
        group_format = f"%Y-%m-%dT{dt_from_iso[-8:]}"
        dt_step = timedelta(days=1)
    elif group_type == "month":
        group_format = f"%Y-%m-{dt_from_iso[-11:]}"
        dt_step = relativedelta(months=1)

    # Формирование pipeline для агрегации
    pipeline = [
        {
            "$match": {
                "dt": {"$gte": dt_from, "$lte": dt_upto}
            }
        },
        {
            "$group": {
                "_id": {"$dateToString": {"format": group_format, "date": group_field}},
                "value_sum": {"$sum": "$value"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": "$_id",
                "value_sum": 1
            }
        },
        {
            "$sort": {"date": 1}
        }
    ]

    # Выполнение агрегации
    result = list(collection.aggregate(pipeline))

    # Добавление нулей для пропущенных дней
    current_date = dt_from
    index = 0
    filled_result = []
    while current_date <= dt_upto:
        if index < len(result) and result[index]["date"] == current_date.strftime(group_format):
            filled_result.append(result[index])
            index += 1
        else:
            filled_result.append({"date": current_date.strftime(group_format), "value_sum": 0})
        current_date += dt_step

    # Формирование ответа
    dataset = [item["value_sum"] for item in filled_result]
    labels = [item["date"] for item in filled_result]

    return {"dataset": dataset, "labels": labels}
