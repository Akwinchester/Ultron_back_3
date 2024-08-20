from datetime import datetime, timedelta

def make_dataset(data):
    dataset = {
        "date": [],
        "amount": {},
        "entry_id": {},
        "description": {},
        "user_id": [],
        "name": {}
    }

    real_date = []

    # Преобразование строк в datetime объекты
    date_objects = [datetime.strptime(row['date_added'], "%Y-%m-%d") for row in data]

    start_date = min(date_objects)
    end_date = max(date_objects)

    delta = end_date - start_date
    dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    dataset["date"] = [d.strftime("%m-%d") for d in dates]

    for row in data:
        row_date = datetime.strptime(row['date_added'], "%Y-%m-%d")
        real_date.append(row_date)

        user_id = row['id_user']
        if user_id not in dataset["entry_id"]:
            dataset["entry_id"][user_id] = [None for _ in dates]
            dataset["description"][user_id] = [None for _ in dates]
        if user_id not in dataset["user_id"]:
            dataset["user_id"].append(user_id)
            dataset["name"][user_id] = row['name']
        dataset['amount'][user_id] = [0 for _ in dates]

    dataset = enter_data(dataset, data, real_date, dates)
    dataset['user_id'].sort()
    return dataset


def make_dataset_only_you(data):
    dataset = {
        "date": [],
        "amount": {},
        "entry_id": {},
        "description": {},
        "user_id": [],
        "name": {}
    }

    real_date = []

    # Преобразование строк в datetime объекты
    date_objects = [datetime.strptime(row[4], "%Y-%m-%d") for row in data]

    start_date = min(date_objects)
    end_date = max(date_objects)

    delta = end_date - start_date
    dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    dataset["date"] = [d.strftime("%m-%d") for d in dates]

    for row in data:
        row_date = datetime.strptime(row[4], "%Y-%m-%d")
        real_date.append(row_date)

        user_id = row[2]
        if user_id not in dataset["entry_id"]:
            dataset["entry_id"][user_id] = [None for _ in dates]
            dataset["description"][user_id] = [None for _ in dates]
        if user_id not in dataset["user_id"]:
            dataset["user_id"].append(user_id)
            dataset["name"][user_id] = row[1]
        dataset['amount'][user_id] = [0 for _ in dates]

    dataset = enter_data_only_you(dataset, data, real_date, dates)
    dataset['user_id'].sort()
    return dataset


def enter_data(dataset, data, real_date, date_line):
    for date in date_line:
        if date in real_date:
            for row in data:
                row_date = datetime.strptime(row['date_added'], "%Y-%m-%d")
                if row_date == date:
                    user_id = row['id_user']
                    dataset['amount'][user_id][date_line.index(date)] = row['amount']
                    dataset['description'][user_id][date_line.index(date)] = row['description'] if row['description'] else None
                    dataset['entry_id'][user_id][date_line.index(date)] = row['id_entry'] if row['id_entry'] else None
    return dataset

def enter_data_only_you(dataset, data, real_date, date_line):
    for date in date_line:
        if date in real_date:
            for row in data:
                row_date = datetime.strptime(row[4], "%Y-%m-%d")  # Индекс 4 соответствует 'date_added'
                if row_date == date:
                    user_id = row[2]  # Индекс 2 соответствует 'user_id'
                    dataset['amount'][user_id][date_line.index(date)] = row[3]  # Индекс 3 соответствует 'amount'
                    dataset['description'][user_id][date_line.index(date)] = row[5] if row[5] else None  # Индекс 5 соответствует 'description'
                    dataset['entry_id'][user_id][date_line.index(date)] = row[0] if row[0] else None  # Индекс 0 соответствует 'id_entry'
    return dataset
